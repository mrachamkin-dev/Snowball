import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface Props {
  narration: string;
  audioDurationFrames: number;
  fps: number;
}

/**
 * Word-by-word caption overlay.
 *
 * Mirrors the playback logic in player.html:
 *   - Split narration into words
 *   - Each word gets equal time: audioDuration / wordCount
 *   - Minimum 400ms per word (12 frames at 30fps)
 *   - Each word pops in with captionPop animation
 *   - Style: sans, 22px bold white, text-shadow
 *
 * Positioned at bottom:170px in player.html viewport (390px tall)
 * -> scaled to 1920px canvas = bottom: ~838px -> top: ~1082px
 *
 * Future: replace uniform timing with Whisper word-level timestamps.
 */
export const Captions: React.FC<Props> = ({
  narration,
  audioDurationFrames,
  fps,
}) => {
  const frame = useCurrentFrame();
  const words = narration.split(/\s+/).filter(Boolean);
  if (words.length === 0) return null;

  // Minimum 400ms (12 frames) per word, matching: Math.max(400, duration/words*1000)
  const framesPerWord = Math.max(12, Math.floor(audioDurationFrames / words.length));

  // Determine which word is active
  const wordIndex = Math.min(
    Math.floor(frame / framesPerWord),
    words.length - 1
  );

  // Only show captions after frame 0 (audio starts playing)
  if (frame < 0 || frame >= audioDurationFrames) return null;

  const currentWord = words[wordIndex];
  const wordStartFrame = wordIndex * framesPerWord;
  const localFrame = frame - wordStartFrame;

  // Spring pop animation matching captionPop: scale(0.85)->1, opacity 0->1
  // Duration 0.12s = ~4 frames, with overshoot (cubic-bezier 0.34,1.56,0.64,1)
  const pop = spring({
    frame: localFrame,
    fps,
    config: {
      damping: 12,
      stiffness: 400,
      mass: 0.4,
    },
    durationInFrames: 6,
  });

  const scale = interpolate(pop, [0, 1], [0.85, 1]);
  const opacity = interpolate(pop, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: "absolute",
        // bottom: 170px in 844px viewport -> ~388px from bottom in 1920
        bottom: 388,
        left: 0,
        right: 0,
        zIndex: 4,
        padding: "0 60px",
        textAlign: "center",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          fontFamily: '"Plus Jakarta Sans", system-ui, sans-serif',
          fontSize: 54, // 22px * ~2.46 scale factor (1080/390 viewport)
          fontWeight: 700,
          color: "#ffffff",
          textShadow: "0 4px 16px rgba(0,0,0,0.9), 0 0 40px rgba(0,0,0,0.7)",
          letterSpacing: "0.02em",
          lineHeight: 1.2,
          transform: `scale(${scale})`,
          opacity,
        }}
      >
        {currentWord}
      </div>
    </div>
  );
};
