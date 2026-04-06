const { put, list } = require('@vercel/blob');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  try {
    const id = Math.random().toString(36).slice(2, 8);
    const data = JSON.stringify(req.body);
    const blob = await put(`stories/${id}.json`, data, {
      access: 'public',
      contentType: 'application/json',
      token: process.env.BLOB_READ_WRITE_TOKEN,
    });

    // If this story is a response to another, mark the original as responded
    if (req.body && req.body.respondingTo) {
      try {
        const origId = req.body.respondingTo;
        const origUrl = `https://4fhlr2aepdibhwh7.public.blob.vercel-storage.com/stories/${origId}.json`;
        const origRes = await fetch(origUrl);
        if (origRes.ok) {
          const origData = await origRes.json();
          origData.responded = true;
          origData.respondedAt = new Date().toISOString();
          await put(`stories/${origId}.json`, JSON.stringify(origData), {
            access: 'public',
            contentType: 'application/json',
            token: process.env.BLOB_READ_WRITE_TOKEN,
          });
        }
      } catch (_) { /* fail silently — don't break the save */ }
    }

    res.status(200).json({ id, url: blob.url });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

module.exports.config = { maxDuration: 30, api: { bodyParser: { sizeLimit: '10mb' } } };
