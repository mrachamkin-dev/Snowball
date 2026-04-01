export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-api-key, anthropic-version');
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
}
