const { put } = require('@vercel/blob');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  try {
    const { data, contentType } = req.body;
    if (!data) return res.status(400).json({ error: 'No data' });
    const base64 = data.replace(/^data:[^;]+;base64,/, '');
    const buffer = Buffer.from(base64, 'base64');
    const ext = (contentType || 'image/jpeg').split('/')[1] || 'jpg';
    const id = Math.random().toString(36).slice(2, 10);
    const blob = await put('photos/' + id + '.' + ext, buffer, {
      access: 'public',
      contentType: contentType || 'image/jpeg',
      token: process.env.BLOB_READ_WRITE_TOKEN,
    });
    res.status(200).json({ url: blob.url });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

module.exports.config = { maxDuration: 30, api: { bodyParser: { sizeLimit: '10mb' } } };
