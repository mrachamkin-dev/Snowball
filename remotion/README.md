# Snowball Remotion — Video Export Pipeline

Renders Snowball stories into real 1080x1920 MP4 files using Remotion Lambda.

## Local Development

```bash
cd remotion
npm install
npx remotion studio    # Opens browser preview
npx remotion render SnowballStory out/test.mp4 --props='{"images":["https://example.com/img.jpg"],"audioUrl":"","musicUrl":null,"narration":"Test caption words","segments":[{"text":"Test caption words","imagePrompt":""}],"hook":"Something happened","location":"New York","genre":"dramatic","from":"Matt","audioDurationInSeconds":10}'
```

## AWS Lambda Setup (One-Time)

### 1. Install Remotion Lambda CLI
```bash
npm i -g @remotion/lambda
```

### 2. Configure AWS credentials
Create an IAM user with the Remotion Lambda policy:
```bash
npx remotion lambda policies user
npx remotion lambda policies role
```

### 3. Deploy
```bash
# Deploy the Remotion bundle to S3
npx remotion lambda sites create remotion/src/index.ts --site-name=snowball

# Deploy the Lambda function
npx remotion lambda functions deploy --memory=2048 --timeout=120
```

### 4. Set Environment Variables in Vercel
```
REMOTION_LAMBDA_ENABLED=true
REMOTION_AWS_ACCESS_KEY_ID=<your-key>
REMOTION_AWS_SECRET_ACCESS_KEY=<your-secret>
REMOTION_S3_BUCKET=<bucket-from-deploy>
REMOTION_LAMBDA_FUNCTION=<function-name-from-deploy>
REMOTION_SERVE_URL=<serve-url-from-sites-create>
```

### 5. Test
```bash
curl -X POST https://snowball-ten.vercel.app/api/render \
  -H "Content-Type: application/json" \
  -d '{"storyId":"abc123"}'
```

## Architecture

```
User creates story
  -> saveStoryToBlob() saves to Vercel Blob
  -> triggerVideoRender() calls POST /api/render
  -> /api/render fetches story, calls Remotion Lambda
  -> Lambda renders SnowballStory composition to MP4
  -> MP4 URL saved back to story blob
  -> "Save for socials" downloads real MP4
```

## Composition Structure

- `SnowballStory` — Root. Layers all components, passes segment timing.
- `KenBurnsLayer` — Crossfading images with 4 Ken Burns patterns.
- `Captions` — Word-by-word caption overlay with spring pop.
- `HookOverlay` — Opening hook + location text, fades out after 3s.
- `Watermark` — Snowball logo, top-left.

All visual parameters (colors, gradients, fonts, timing) are matched exactly
to the live DOM playback in index.html and player.html.
