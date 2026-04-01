module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  const r = await fetch('https://api.elevenlabs.io/v1/text-to-speech/TX3LPaxmHKxFdv7VOQHJ', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'xi-api-key': 'sk_69ac076bcc4461c1756f9be2e2e1900dc8120a1b97256507' },
    body: JSON.stringify(req.body),
  });
  const buffer = await r.arrayBuffer();
  res.setHeader('Content-Type', 'audio/mpeg');
  res.status(r.status).send(Buffer.from(buffer));
};
