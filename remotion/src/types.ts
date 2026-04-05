/** Matches the story blob schema from saveStoryToBlob */
export interface Segment {
  text: string;
  imagePrompt: string;
}

export type Genre =
  | "funny"
  | "dramatic"
  | "romantic"
  | "action"
  | "tragic"
  | "triumphant"
  | "awkward";

export interface StoryProps {
  images: string[];       // CDN URLs from fal.ai
  audioUrl: string;       // base64 data URI or CDN URL
  musicUrl: string | null;// ElevenLabs MP3 URL or null
  narration: string;      // Full narration text for captions
  segments: Segment[];    // Per-beat text + imagePrompt
  hook: string;
  location: string;
  genre: Genre;
  from: string;           // Sender name (empty string if none)
  audioDurationInSeconds: number; // Pre-calculated on server
}

/** Ken Burns animation parameters — mirrors the 4 CSS keyframe patterns */
export interface KenBurnsPattern {
  startScale: number;
  endScale: number;
  startX: number;
  endX: number;
  startY: number;
  endY: number;
}

/**
 * The 4 Ken Burns patterns matching index.html/player.html CSS keyframes:
 * kenBurns1: scale(1.0) translate(0%,0%)    -> scale(1.14) translate(-2.5%,-2%)
 * kenBurns2: scale(1.1) translate(-1.5%,1%) -> scale(1.0)  translate(0%,0%)
 * kenBurns3: scale(1.0) translate(1%,-1%)   -> scale(1.12) translate(-1.5%,1.5%)
 * kenBurns4: scale(1.12) translate(0%,1.5%) -> scale(1.0)  translate(-2%,0%)
 */
export const KB_PATTERNS: KenBurnsPattern[] = [
  { startScale: 1.0,  endScale: 1.14, startX: 0,    endX: -2.5, startY: 0,   endY: -2   },
  { startScale: 1.1,  endScale: 1.0,  startX: -1.5, endX: 0,    startY: 1,   endY: 0    },
  { startScale: 1.0,  endScale: 1.12, startX: 1,    endX: -1.5, startY: -1,  endY: 1.5  },
  { startScale: 1.12, endScale: 1.0,  startX: 0,    endX: -2,   startY: 1.5, endY: 0    },
];

/** Genre background gradients — matches player.html genreBgs */
export const GENRE_BACKGROUNDS: Record<Genre, string> = {
  dramatic:   "linear-gradient(135deg, #060810 0%, #060402 100%)",
  romantic:   "linear-gradient(135deg, #120E06 0%, #060402 100%)",
  funny:      "linear-gradient(135deg, #0C0A06 0%, #060402 100%)",
  action:     "linear-gradient(135deg, #080A0C 0%, #060402 100%)",
  tragic:     "linear-gradient(135deg, #060A10 0%, #060402 100%)",
  triumphant: "linear-gradient(135deg, #100E04 0%, #060402 100%)",
  awkward:    "linear-gradient(135deg, #0E0A06 0%, #060402 100%)",
};
