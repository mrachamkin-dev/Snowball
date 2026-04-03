module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method === 'OPTIONS') return res.status(200).end();
  try {
    const { id } = req.query;
    if (!id) return res.status(400).json({ error: 'No id' });
    const url = `https://4fhlr2aepdibhwh7.public.blob.vercel-storage.com/stories/${id}.json`;
    const r = await fetch(url);
    if (!r.ok) return res.status(404).json({ error: 'Story not found' });
    const data = await r.json();
    res.status(200).json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
};

module.exports.config = { maxDuration: 30 };
