module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  try {
    const { prompt, duration_ms, output_format } = req.body;
    if (!prompt) return res.status(400).json({ error: 'Missing prompt' });
    const r = await fetch('https://api.elevenlabs.io/v1/music/compose', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'xi-api-key': process.env.ELEVENLABS_API_KEY,
      },
      body: JSON.stringify({
        prompt: prompt,
        duration_ms: duration_ms || 30000,
        force_instrumental: true,
        output_format: output_format || 'mp3_44100_128',
      }),
    });
    if (!r.ok) {
      const errText = await r.text();
      return res.status(r.status).json({ error: 'ElevenLabs Music error: ' + r.status, detail: errText });
    }
    const buffer = await r.arrayBuffer();
    res.setHeader('Content-Type', 'audio/mpeg');
    res.status(200).send(Buffer.from(buffer));
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

module.exports.config = { maxDuration: 120, api: { bodyParser: { sizeLimit: '1mb' } } };
