export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  const r = await fetch('https://fal.run/fal-ai/flux/schnell', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Key 8e2003f2-661b-4b86-8b92-fd5f86be8ab1:aa1eb177dc4e41736dbf18d212b0865f' },
    body: JSON.stringify(req.body),
  });
  const d = await r.json();
  res.status(r.status).json(d);
}
