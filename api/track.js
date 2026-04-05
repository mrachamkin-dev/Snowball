const { put, list, head } = require('@vercel/blob');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  try {
    const event = req.body;
    if (!event || !event.event) {
      return res.status(400).json({ error: 'Missing event name' });
    }
    const entry = {
      event: event.event,
      timestamp: new Date().toISOString(),
      genre: event.genre || null,
      flow: event.flow || null,
      storyId: event.storyId || null,
      segmentCount: event.segmentCount || null,
    };
    const key = 'analytics/events/' + Date.now() + '-' + Math.random().toString(36).slice(2, 6) + '.json';
    await put(key, JSON.stringify(entry), {
      access: 'public',
      contentType: 'application/json',
      token: process.env.BLOB_READ_WRITE_TOKEN,
    });
    res.status(200).json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

module.exports.config = { maxDuration: 10, api: { bodyParser: { sizeLimit: '1mb' } } };
