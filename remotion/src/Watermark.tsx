import React from "react";

/**
 * Snowball wordmark watermark.
 * Positioned top-left, matching the logo in player.html:
 *   top:44px left:16px, opacity 0.82, serif 16px cream
 *
 * Scaled to 1080x1920: top:217px left:40px, font 40px
 *
 * Uses a unicode circle (U+25CF) as the snowball dot,
 * matching the logo.innerHTML pattern in player.html.
 */
export const Watermark: React.FC = () => {
  return (
    <div
      style={{
        position: "absolute",
        top: 217,
        left: 40,
        zIndex: 10,
        display: "flex",
        alignItems: "center",
        gap: 8,
        opacity: 0.82,
      }}
    >
      <span
        style={{
          fontFamily: '"Cormorant Garamond", Georgia, serif',
          fontSize: 40,
          fontWeight: 600,
          color: "#EEE8DC",
        }}
      >
        snow
      </span>
      <div
        style={{
          width: 14,
          height: 14,
          borderRadius: "50%",
          flexShrink: 0,
          background:
            "radial-gradient(circle at 32% 28%, #FFF 0%, #EEF7FB 12%, #C0DDE9 36%, #82B0C2 60%, #527C8F 80%, #2F5E6E 100%)",
          boxShadow:
            "inset -2px -2px 4px rgba(0,0,0,0.3), inset 1px 1px 3px rgba(255,255,255,0.7), 0 2px 6px rgba(0,0,0,0.4)",
        }}
      />
      <span
        style={{
          fontFamily: '"Cormorant Garamond", Georgia, serif',
          fontSize: 40,
          fontWeight: 600,
          color: "#EEE8DC",
        }}
      >
        ball
      </span>
    </div>
  );
};
