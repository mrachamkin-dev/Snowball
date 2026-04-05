import React from "react";
import { AbsoluteFill, Img, interpolate, useCurrentFrame } from "remotion";
import { KB_PATTERNS } from "./types";
import type { KenBurnsPattern } from "./types";

interface Props {
  images: string[];
  frameRanges: Array<{ start: number; end: number }>;
  totalFrames: number;
}

/**
 * Renders Ken Burns animated images with crossfade transitions.
 *
 * Mirrors the playback logic:
 * - Each image gets one of 4 Ken Burns patterns (cycling via i % 4)
 * - Crossfade transition between images (0.8s = 24 frames)
 * - Images cover the full frame (object-fit: cover equivalent)
 *
 * The 4 patterns match the CSS keyframes in index.html:
 *   kenBurns1: scale 1.0->1.14, translate (0,0)->(-2.5%,-2%)
 *   kenBurns2: scale 1.1->1.0,  translate (-1.5%,1%)->(0,0)
 *   kenBurns3: scale 1.0->1.12, translate (1%,-1%)->(-1.5%,1.5%)
 *   kenBurns4: scale 1.12->1.0, translate (0,1.5%)->(-2%,0)
 */
export const KenBurnsLayer: React.FC<Props> = ({
  images,
  frameRanges,
  totalFrames,
}) => {
  const frame = useCurrentFrame();
  const CROSSFADE_FRAMES = 24; // 0.8s at 30fps

  return (
    <AbsoluteFill>
      {images.map((src, i) => {
        const range = frameRanges[i];
        if (!range) return null;

        // Determine opacity for crossfade
        let opacity = 0;
        if (frame >= range.start && frame <= range.end) {
          // Fade in during first CROSSFADE_FRAMES
          if (i > 0 && frame < range.start + CROSSFADE_FRAMES) {
            opacity = interpolate(
              frame,
              [range.start, range.start + CROSSFADE_FRAMES],
              [0, 1],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
            );
          } else {
            opacity = 1;
          }
          // Fade out during last CROSSFADE_FRAMES (except last image)
          if (i < images.length - 1 && frame > range.end - CROSSFADE_FRAMES) {
            opacity = interpolate(
              frame,
              [range.end - CROSSFADE_FRAMES, range.end],
              [1, 0],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
            );
          }
        } else if (frame < range.start) {
          opacity = 0;
        } else {
          // Past this image's range — only visible if it's the last image
          opacity = i === images.length - 1 ? 1 : 0;
        }

        if (opacity <= 0) return null;

        // Ken Burns animation
        const pattern: KenBurnsPattern = KB_PATTERNS[i % KB_PATTERNS.length];
        const segDuration = range.end - range.start;
        const progress = interpolate(
          frame,
          [range.start, range.start + segDuration],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        const scale = interpolate(progress, [0, 1], [pattern.startScale, pattern.endScale]);
        const tx = interpolate(progress, [0, 1], [pattern.startX, pattern.endX]);
        const ty = interpolate(progress, [0, 1], [pattern.startY, pattern.endY]);

        return (
          <AbsoluteFill key={i} style={{ opacity }}>
            <Img
              src={src}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                transform: `scale(${scale}) translate(${tx}%, ${ty}%)`,
              }}
            />
          </AbsoluteFill>
        );
      })}
    </AbsoluteFill>
  );
};
