---
name: 21st-dev
description: "**21st.dev Component Registry**: Browse, generate, and integrate production-ready React/Tailwind UI components from 21st.dev — the largest open-source component registry for design engineers. Use this skill ANY time you need a polished UI component, widget, section, or page layout in React. Triggers: component, UI component, shadcn, 21st.dev, design component, hero section, card component, navbar, sidebar, dashboard layout, landing page section, pricing table, testimonial, feature grid, modal, dialog, toast, dropdown, command palette, or any request for a specific pre-built React component."
---

# 21st.dev — AI Component Registry

21st.dev is the largest community React component registry (1.4M+ developers). Think of it as the npm for design — browse, copy, and customize production-ready components built on shadcn/ui + Tailwind CSS.

## What 21st.dev Is

A curated, searchable registry of open-source React components. Unlike traditional component libraries (npm install + import), 21st.dev works by **copying component source code directly into your project**. You own the code, can modify it freely, and have zero dependency on the registry at runtime.

Built on the same philosophy as shadcn/ui: components are not a package you install — they're code you own.

## How to Use 21st.dev

### MCP Server (AI-Native Integration)

21st.dev provides an MCP server that lets AI coding assistants (Claude, Cursor, Windsurf) search and fetch components directly:

```json
// In your MCP config (e.g., .cursor/mcp.json or claude_desktop_config.json)
{
  "mcpServers": {
    "21st_magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest"],
      "env": {
        "TWENTY_FIRST_API_KEY": "your-api-key"
      }
    }
  }
}
```

Once connected, you can ask Claude to search 21st.dev for components and it will fetch the source code directly.

### CLI

```bash
npx @21st-dev/cli add <component-url>
```

### Manual (Web)

1. Browse https://21st.dev
2. Find a component you like
3. Click "Copy code"
4. Paste into your project

---

## Component Stack

All 21st.dev components are built with:

- **React 18/19** — functional components with hooks
- **Tailwind CSS** — utility-first styling, no external CSS files
- **shadcn/ui primitives** — built on Radix UI for accessibility
- **TypeScript** — full type safety
- **Motion / Framer Motion** — many components include animations

### Required Dependencies

Most components need these in your project:

```bash
npm install tailwindcss @radix-ui/react-* class-variance-authority clsx tailwind-merge lucide-react
```

The `cn()` utility (from shadcn/ui) is used everywhere:
```ts
// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## Component Categories

### Layout & Navigation
- **Navbar** — responsive nav with mobile menu, sticky, transparent-on-scroll
- **Sidebar** — collapsible, with icons, nested groups, active states
- **Footer** — multi-column, with newsletter signup, social links
- **Breadcrumb** — auto-generated from path, with dropdown for deep nesting
- **Tabs** — animated underline, icon+text, vertical variants
- **Command Palette** — Cmd+K search modal with fuzzy search

### Data Display
- **Card** — basic, interactive, with image, stats card, pricing card
- **Table** — sortable, filterable, with pagination, row selection
- **Timeline** — vertical/horizontal, with icons and status
- **Stats** — animated counters, comparison, sparklines
- **Badge** — status indicators, tags, notification dots
- **Avatar** — single, group/stack, with status indicator

### Forms & Input
- **Input** — with label, error, icon, floating label
- **Select** — searchable, multi-select, creatable
- **Date Picker** — single, range, with presets
- **File Upload** — drag & drop, with preview, progress
- **Toggle** — switch, with label, grouped
- **Slider** — range, with marks, vertical

### Feedback & Overlay
- **Modal / Dialog** — sizes, with form, confirmation, nested
- **Toast** — positions, types (success/error/info), stackable
- **Alert** — inline, with actions, dismissible
- **Tooltip** — hover, click, rich content
- **Popover** — positioned, with arrow, interactive content
- **Drawer** — bottom sheet, side drawer, nested

### Marketing & Content
- **Hero** — full-screen, split, with video, animated text
- **Feature Grid** — icon grid, bento, alternating
- **Testimonial** — card, carousel, wall-of-love
- **Pricing** — toggle monthly/annual, comparison table, highlighted tier
- **CTA** — banner, floating, with countdown
- **Logo Cloud** — animated marquee, grid, grayscale-to-color
- **FAQ** — accordion, categorized, searchable

### Specialized
- **Chart** — bar, line, area, pie (usually Recharts-based)
- **Calendar** — month view, with events
- **Kanban** — drag & drop columns
- **Code Block** — syntax highlighted, with copy button
- **Markdown Renderer** — with custom components
- **Image Gallery** — masonry, lightbox, with zoom

---

## Using 21st.dev Components in Your Project

### Setup shadcn/ui (if not already)

```bash
npx shadcn@latest init
```

This creates:
- `components/ui/` directory
- `lib/utils.ts` with `cn()` helper
- Tailwind config with CSS variables for theming

### Adding a Component

1. **Search** for what you need on 21st.dev or via MCP
2. **Copy** the component source code
3. **Save** to your `components/` directory
4. **Install** any missing dependencies listed in the component
5. **Customize** — it's your code now

### Customization Pattern

Components use Tailwind CSS variables for theming:

```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    /* ... */
  }
  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    /* ... */
  }
}
```

To match Snowball's design system:
```css
:root {
  --background: 20 50% 1%;         /* #060402 */
  --foreground: 34 33% 88%;        /* --cream #EEE8DC */
  --primary: 42 76% 53%;           /* --gold #E5B444 */
  --secondary: 195 53% 82%;        /* --ice #C2E4EE */
  --muted: 30 8% 35%;              /* muted text */
}
```

---

## Integration with Motion/Framer Motion

Many 21st.dev components ship with animations. When customizing animations, use the framer-motion skill's patterns. Common animation points in 21st.dev components:

- **Page section entrances** — `whileInView` with stagger
- **Card hovers** — `whileHover` scale + shadow
- **Modal open/close** — `AnimatePresence` + `exit`
- **Tab switches** — `layoutId` for the active indicator
- **Number stats** — `useMotionValue` + `useTransform` for counting

---

## Quality Checklist

When using or recommending 21st.dev components:

1. **Accessibility** — shadcn/ui primitives handle keyboard navigation + ARIA. Don't break it during customization.
2. **Responsive** — most components are mobile-ready. Test at 375px width.
3. **Dark mode** — components use CSS variables, so dark mode works if your Tailwind config supports it.
4. **Bundle size** — since you own the code, tree-shaking happens naturally. Remove unused variants.
5. **TypeScript** — keep the types. They catch integration bugs early.
