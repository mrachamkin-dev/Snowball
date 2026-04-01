module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': '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',
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify(req.body),
  });
  const text = await r.text();
  res.status(r.status).send(text);
};
