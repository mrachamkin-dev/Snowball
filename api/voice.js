const { put } = require('@vercel/blob');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  const voiceId = req.query.voice || 'pNInz6obpgDQGcFmaJgB';
  const r = await fetch('https://api.elevenlabs.io/v1/text-to-speech/' + voiceId, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'xi-api-key': process.env.ELEVENLABS_API_KEY
    },
    body: JSON.stringify(req.body),
  });
  if (!r.ok) return res.status(r.status).json({ error: 'ElevenLabs error' });
  const buffer = await r.arrayBuffer();
  const id = Math.random().toString(36).slice(2, 10);
  const blob = await put('audio/' + id + '.mp3', Buffer.from(buffer), {
    access: 'public',
    contentType: 'audio/mpeg',
    token: process.env.BLOB_READ_WRITE_TOKEN,
  });
  res.status(200).json({ url: blob.url, wordTimings: [] });
};
