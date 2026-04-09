const fs = require('fs');
const path = require('path');

module.exports = async function handler(req, res) {
  try {
    const { id } = req.query;
    // Read the static player.html
    const htmlPath = path.join(process.cwd(), 'player.html');
    let html = fs.readFileSync(htmlPath, 'utf8');

    if (id) {
      // Fetch story data for OG tags
      try {
        const storyUrl = `https://4fhlr2aepdibhwh7.public.blob.vercel-storage.com/stories/${id}.json`;
        const r = await fetch(storyUrl);
        if (r.ok) {
          const story = await r.json();
          const title = story.hook || 'A Snowball Story';
          const desc = story.from
            ? `${story.from} threw you a snowball`
            : 'Someone threw you a snowball';
          const image = (story.images && story.images[0]) || '';
          const url = `https://snowball-ten.vercel.app/s/${id}`;

          // Escape for HTML attributes
          const esc = (s) => (s || '').replace(/"/g, '&quot;').replace(/</g, '&lt;');

          // Replace empty OG tags with real data
          const inlineStory = JSON.stringify(story).replace(/<\/script>/g,'<\/script>');html=html.replace('</head>',`<script>window.__STORY__=${inlineStory};</script></head>`);html = html
            .replace(
              '<meta property="og:title" content="">',
              `<meta property="og:title" content="${esc(title)}">`
            )
            .replace(
              '<meta property="og:description" content="">',
              `<meta property="og:description" content="${esc(desc)}">`
            )
            .replace(
              '<meta property="og:image" content="">',
              `<meta property="og:image" content="${esc(image)}">`
            )
            .replace(
              '<meta property="og:url" content="">',
              `<meta property="og:url" content="${esc(url)}">`
            )
            .replace(
              '<title>Snowball</title>',
              `<title>${esc(title)} | Snowball</title>`
            )
            .replace(
              '<meta name="twitter:title" content="">',
              `<meta name="twitter:title" content="${esc(title)}">`
            )
            .replace(
              '<meta name="twitter:description" content="">',
              `<meta name="twitter:description" content="${esc(desc)}">`
            )
            .replace(
              '<meta name="twitter:image" content="">',
              `<meta name="twitter:image" content="${esc(image)}">`
            );
        }
      } catch (_) {
        // If story fetch fails, serve page with empty OG tags (same as before)
      }
    }

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=3600, stale-while-revalidate=86400');
    res.status(200).send(html);
  } catch (e) {
    // Fallback: redirect to static player.html
    res.writeHead(302, { Location: '/player.html' });
    res.end();
  }
};

module.exports.config = { maxDuration: 15 };
