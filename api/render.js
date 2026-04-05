/**
 * /api/render — Triggers Remotion Lambda to render a story into MP4.
 *
 * POST { storyId } or POST { storyId, ...storyData }
 *
 * Flow:
 *   1. Fetch story data from Vercel Blob (or accept it directly)
 *   2. Calculate audio duration from base64 data URI
 *   3. Call Remotion Lambda renderMediaOnLambda()
 *   4. Wait for render to complete
 *   5. Return { videoUrl } (S3 URL of rendered MP4)
 *
 * Environment variables required:
 *   REMOTION_AWS_ACCESS_KEY_ID     — AWS IAM key with Lambda invoke + S3 access
 *   REMOTION_AWS_SECRET_ACCESS_KEY — Corresponding secret
 *   REMOTION_S3_BUCKET             — S3 bucket where Remotion bundle is deployed
 *   REMOTION_LAMBDA_FUNCTION       — Name of the deployed Remotion Lambda function
 *   REMOTION_SERVE_URL             — URL of the deployed Remotion bundle on S3
 *   BLOB_READ_WRITE_TOKEN          — Vercel Blob token (existing)
 *
 * Note: Until Lambda is deployed, this endpoint returns a mock response
 * with instructions for setup. Enable REMOTION_LAMBDA_ENABLED=true when ready.
 */

const { put } = require('@vercel/blob');

const BLOB_BASE = 'https://4fhlr2aepdibhwh7.public.blob.vercel-storage.com';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    const { storyId } = req.body;
    if (!storyId) {
      return res.status(400).json({ error: 'storyId is required' });
    }

    // Fetch story data from blob storage
    const storyUrl = `${BLOB_BASE}/stories/${storyId}.json`;
    const storyRes = await fetch(storyUrl);
    if (!storyRes.ok) {
      return res.status(404).json({ error: 'Story not found' });
    }
    const story = await storyRes.json();

    // Calculate audio duration from base64 data URI
    // The audioUrl in the blob is a base64 data URI
    const audioDurationInSeconds = estimateAudioDuration(story);

    // Build Remotion input props
    const inputProps = {
      images: story.images || [],
      audioUrl: story.audioUrl || '',
      musicUrl: story.musicUrl || null,
      narration: story.narration || '',
      segments: story.segments || story._segments || [],
      hook: story.hook || '',
      location: story.location || '',
      genre: story.genre || 'dramatic',
      from: story.from || '',
      audioDurationInSeconds,
    };

    // Check if Lambda is configured
    if (process.env.REMOTION_LAMBDA_ENABLED !== 'true') {
      // Return setup instructions when Lambda isn't configured yet
      return res.status(200).json({
        status: 'pending_setup',
        message: 'Remotion Lambda not yet configured. See /remotion/README.md for setup.',
        inputProps, // Return props so you can test locally with `remotion render`
        localRenderCommand: `cd remotion && npx remotion render SnowballStory out/${storyId}.mp4 --props='${JSON.stringify({ ...inputProps, audioUrl: '[truncated]' })}'`,
      });
    }

    // --- Lambda render path ---
    // Dynamic import since @remotion/lambda may not be installed in Vercel
    const { renderMediaOnLambda, getRenderProgress } = await import('@remotion/lambda/client');

    const { renderId, bucketName } = await renderMediaOnLambda({
      region: 'us-east-1',
      functionName: process.env.REMOTION_LAMBDA_FUNCTION,
      serveUrl: process.env.REMOTION_SERVE_URL,
      composition: 'SnowballStory',
      inputProps,
      codec: 'h264',
      imageFormat: 'jpeg',
      maxRetries: 1,
      privacy: 'public',
      framesPerLambda: 120, // ~4s chunks for parallel rendering
    });

    // Poll for completion (Lambda renders are fast — typically 3-8 seconds)
    let videoUrl = null;
    const maxWait = 60000; // 60s timeout
    const pollInterval = 1500;
    const start = Date.now();

    while (Date.now() - start < maxWait) {
      const progress = await getRenderProgress({
        renderId,
        bucketName,
        region: 'us-east-1',
        functionName: process.env.REMOTION_LAMBDA_FUNCTION,
      });

      if (progress.done) {
        videoUrl = progress.outputFile;
        break;
      }

      if (progress.fatalErrorEncountered) {
        return res.status(500).json({
          error: 'Render failed',
          details: progress.errors?.[0]?.message || 'Unknown error',
        });
      }

      await new Promise((r) => setTimeout(r, pollInterval));
    }

    if (!videoUrl) {
      return res.status(504).json({ error: 'Render timed out' });
    }

    // Update the story blob with the video URL
    try {
      const updatedStory = { ...story, videoUrl };
      await put(`stories/${storyId}.json`, JSON.stringify(updatedStory), {
        access: 'public',
        contentType: 'application/json',
        token: process.env.BLOB_READ_WRITE_TOKEN,
      });
    } catch (e) {
      // Non-fatal — video is still accessible via direct URL
      console.error('Failed to update story blob with videoUrl:', e.message);
    }

    return res.status(200).json({ videoUrl, renderId });
  } catch (e) {
    console.error('Render error:', e);
    return res.status(500).json({ error: e.message });
  }
};

/**
 * Estimate audio duration from story data.
 * Uses segment word counts and average speaking rate (~2.5 words/sec)
 * as a fallback when we can't decode the audio server-side.
 *
 * More accurate: parse the base64 audio to get actual duration.
 * For now, word-count estimation is sufficient since the composition
 * uses calculateMetadata to set the correct frame count.
 */
function estimateAudioDuration(story) {
  // If segments have word counts, estimate from speaking rate
  const segments = story.segments || story._segments || [];
  const narration = story.narration || '';
  const wordCount = narration.split(/\s+/).filter(Boolean).length;

  if (wordCount > 0) {
    // Average TTS rate for ElevenLabs is ~2.5 words/second
    return Math.max(10, Math.ceil(wordCount / 2.5));
  }

  // Fallback: estimate from segment count
  const segCount = segments.length || 4;
  return segCount * 5; // ~5 seconds per segment
}

module.exports.config = {
  maxDuration: 120,
  api: { bodyParser: { sizeLimit: '1mb' } },
};
