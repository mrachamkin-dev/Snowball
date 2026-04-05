import { Composition } from "remotion";
import { SnowballStory } from "./SnowballStory";
import type { StoryProps } from "./types";

/**
 * Root component registers all Remotion compositions.
 * SnowballStory is the main (and currently only) composition.
 *
 * Duration is calculated dynamically from audioDurationInSeconds.
 * Default 900 frames = 30s at 30fps (overridden by inputProps at render time).
 */
export const Root: React.FC = () => {
  return (
    <Composition
      id="SnowballStory"
      component={SnowballStory}
      width={1080}
      height={1920}
      fps={30}
      // Default duration; overridden at render time via calculateMetadata
      durationInFrames={900}
      defaultProps={{
        images: [],
        audioUrl: "",
        musicUrl: null,
        narration: "",
        segments: [],
        hook: "Your story awaits",
        location: "",
        genre: "dramatic" as const,
        from: "",
        audioDurationInSeconds: 30,
      } satisfies StoryProps}
      calculateMetadata={({ props }) => {
        // Duration = audio length + 2s buffer for fade out
        const durationInFrames = Math.ceil((props.audioDurationInSeconds + 2) * 30);
        return { durationInFrames, props };
      }}
    />
  );
};
