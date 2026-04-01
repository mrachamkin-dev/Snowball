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
    },
    body: JSON.stringify(req.body),
  });
  const text = await r.text();
  res.status(r.status).send(text);
}
