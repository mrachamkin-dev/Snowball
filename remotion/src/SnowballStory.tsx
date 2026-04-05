import { AbsoluteFill, Audio, Sequence, useVideoConfig } from "remotion";
import type { StoryProps } from "./types";
import { GENRE_BACKGROUNDS } from "./types";
import { KenBurnsLayer } from "./KenBurnsLayer";
import { Captions } from "./Captions";
import { HookOverlay } from "./HookOverlay";
import { Watermark } from "./Watermark";

/**
 * Root composition — mirrors the visual stack from player.html/index.html.
 *
 * Layer order (bottom to top):
 *   0. Genre background gradient
 *   1. Ken Burns images (crossfade, segment-timed)
 *   2. Dark overlay (0.45 opacity)
 *   3. Top gradient (hook readability)
 *   4. Bottom gradient (caption readability)
 *   5. Hook + location overlay (fades out after 3s)
 *   6. Sender identity (if present)
 *   7. Word-by-word captions
 *   8. Snowball watermark
 *   Audio: narration (vol 1.0) + music (vol 0.25)
 */
export const SnowballStory: React.FC<StoryProps> = ({
  images,
  audioUrl,
  musicUrl,
  narration,
  segments,
  hook,
  location,
  genre,
  from,
  audioDurationInSeconds,
}) => {
  const { fps, durationInFrames } = useVideoConfig();
  const audioDurationFrames = Math.ceil(audioDurationInSeconds * fps);

  // Calculate segment boundaries for image timing
  // Mirrors: segWords -> segBoundaries in index.html playback
  const segmentWordCounts = segments.map(
    (s) => (s.text || "").split(/\s+/).filter(Boolean).length
  );
  const totalWords = segmentWordCounts.reduce((a, b) => a + b, 0) || 1;

  // Each segment boundary = cumulative fraction of total words
  const segmentBoundaries: number[] = [];
  let cumulative = 0;
  for (const count of segmentWordCounts) {
    cumulative += count;
    segmentBoundaries.push(cumulative / totalWords);
  }

  // Convert boundaries to frame ranges for each image
  const imageFrameRanges: Array<{ start: number; end: number }> = [];
  for (let i = 0; i < images.length; i++) {
    const start = i === 0 ? 0 : Math.floor(segmentBoundaries[i - 1] * audioDurationFrames);
    const end =
      i < segmentBoundaries.length
        ? Math.floor(segmentBoundaries[i] * audioDurationFrames)
        : audioDurationFrames;
    imageFrameRanges.push({ start, end });
  }

  const bg = GENRE_BACKGROUNDS[genre] || GENRE_BACKGROUNDS.dramatic;

  return (
    <AbsoluteFill>
      {/* Layer 0: Genre background */}
      <AbsoluteFill style={{ background: bg }} />

      {/* Layer 1: Ken Burns images */}
      <KenBurnsLayer
        images={images}
        frameRanges={imageFrameRanges}
        totalFrames={audioDurationFrames}
      />

      {/* Layer 2: Dark overlay — matches rgba(0,0,0,0.45) */}
      <AbsoluteFill style={{ backgroundColor: "rgba(0,0,0,0.45)" }} />

      {/* Layer 3: Top gradient — matches height:120px in player.html */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          // Scale 120px from 390px viewport to 1920px canvas = ~592px
          height: 592,
          background: "linear-gradient(to bottom, rgba(0,0,0,0.85), transparent)",
          zIndex: 2,
        }}
      />

      {/* Layer 4: Bottom gradient — matches height:280px -> ~1382px scaled */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 1382,
          background: "linear-gradient(to top, rgba(0,0,0,0.97), transparent)",
          zIndex: 2,
        }}
      />

      {/* Layer 5: Hook overlay — visible first 3s, fades out over 1.2s */}
      <Sequence from={0} durationInFrames={Math.ceil(4.2 * fps)}>
        <HookOverlay hook={hook} location={location} fps={fps} />
      </Sequence>

      {/* Layer 6: Sender identity */}
      {from ? (
        <div
          style={{
            position: "absolute",
            top: 236,
            left: 0,
            right: 0,
            textAlign: "center",
            zIndex: 10,
            fontFamily:
              '"Plus Jakarta Sans", system-ui, sans-serif',
            fontSize: 24,
            fontWeight: 500,
            color: "#EEE8DC",
            opacity: 0.7,
            letterSpacing: "0.04em",
          }}
        >
          {from} threw this to you
        </div>
      ) : null}

      {/* Layer 7: Word-by-word captions */}
      <Captions
        narration={narration}
        audioDurationFrames={audioDurationFrames}
        fps={fps}
      />

      {/* Layer 8: Watermark */}
      <Watermark />

      {/* Audio: Narration */}
      {audioUrl ? (
        <Audio src={audioUrl} volume={1} />
      ) : null}

      {/* Audio: Background music at 0.25 volume */}
      {musicUrl ? (
        <Audio src={musicUrl} volume={0.25} loop />
      ) : null}
    </AbsoluteFill>
  );
};
