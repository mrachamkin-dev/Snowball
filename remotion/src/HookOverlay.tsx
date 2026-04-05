import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface Props {
  hook: string;
  location: string;
  fps: number;
}

/**
 * Hook + location text overlay.
 *
 * Mirrors player.html hookOverlay:
 *   - Location: sans 10px uppercase gold, letter-spacing 0.24em, fades up at 0.4s
 *   - Hook: serif 32px cream, fades up at 0.7s
 *   - Both centered vertically with padding 80px top, 220px bottom
 *   - Entire overlay fades out starting at 3s over 1.2s
 *
 * Scaled to 1080x1920 canvas:
 *   - Location font: ~25px, Hook font: ~79px
 *   - Padding top: ~394px, bottom: ~1084px
 */
export const HookOverlay: React.FC<Props> = ({ hook, location, fps }) => {
  const frame = useCurrentFrame();
  const fadeOutStart = 3 * fps; // 90 frames
  const fadeOutEnd = fadeOutStart + Math.ceil(1.2 * fps); // ~126 frames

  // Overall container opacity: full until 3s, then fades out
  const containerOpacity = interpolate(
    frame,
    [fadeOutStart, fadeOutEnd],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Location: fades up starting at 0.4s (12 frames), over 0.8s (24 frames)
  const locOpacity = interpolate(frame, [12, 36], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const locY = interpolate(frame, [12, 36], [18, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Hook: fades up starting at 0.7s (21 frames), over 0.8s (24 frames)
  const hookOpacity = interpolate(frame, [21, 45], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const hookY = interpolate(frame, [21, 45], [18, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 3,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        // padding: 80px 32px 220px in 844px viewport -> scaled
        padding: "394px 80px 1084px",
        textAlign: "center",
        opacity: containerOpacity,
      }}
    >
      {/* Location label */}
      {location ? (
        <div
          style={{
            fontFamily: '"Plus Jakarta Sans", system-ui, sans-serif',
            fontSize: 25,
            fontWeight: 500,
            color: "#E5B444",
            letterSpacing: "0.24em",
            textTransform: "uppercase" as const,
            marginBottom: 44,
            opacity: locOpacity,
            transform: `translateY(${locY}px)`,
          }}
        >
          {location}
        </div>
      ) : null}

      {/* Hook text */}
      <div
        style={{
          fontFamily: '"Cormorant Garamond", Georgia, serif',
          fontSize: 79,
          fontWeight: 400,
          color: "#EEE8DC",
          lineHeight: 1.25,
          opacity: hookOpacity,
          transform: `translateY(${hookY}px)`,
        }}
      >
        {hook}
      </div>
    </div>
  );
};
