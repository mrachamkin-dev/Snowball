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
      'xi-api-key': process.env.ELEVENLABS_API_KEY||'sk_77836996a6fc455c23c5ece694f311e4d6331f2058b65e09'
    },
    body: JSON.stringify(req.body),
  });
  const buffer = await r.arrayBuffer();
  res.setHeader('Content-Type', 'audio/mpeg');
  res.status(r.status).send(Buffer.from(buffer));
};
// updated Sat Apr  4 23:12:45 EDT 2026
