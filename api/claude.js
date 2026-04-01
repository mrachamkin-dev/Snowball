export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-api-key, anthropic-version');
  if (req.method === 'OPTIONS') return res.status(200).end();
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      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
    body: JSON.stringify(req.body),
  });
  const text = await r.text();
  res.status(r.status).send(text);
}
