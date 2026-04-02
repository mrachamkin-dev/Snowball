module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const model = req.query.model || 'fal-ai/flux/schnell';
  const FAL_KEY = '8e2003f2-661b-4b86-8b92-fd5f86be8ab1:aa1eb177dc4e41736dbf18d212b0865f';

  const r = await fetch('https://fal.run/' + model, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Key ' + FAL_KEY
    },
    body: JSON.stringify(req.body),
  });

  if (!r.ok) {
    const err = await r.text();
    return res.status(r.status).json({ error: err });
  }
  const data = await r.json();
  res.setHeader('Content-Type', 'application/json');
  res.status(200).json(data);
};
