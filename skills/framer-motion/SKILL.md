---
name: framer-motion
description: "**Motion for React (Framer Motion) Animation Expert**: Build production-grade animations with Motion (formerly Framer Motion). Use this skill ANY time animations, transitions, gestures, scroll effects, layout animations, page transitions, or micro-interactions are needed in React/Next.js. Triggers: animation, animate, transition, motion, framer, gesture, hover effect, scroll animation, page transition, stagger, spring, parallax, entrance animation, exit animation, loading animation, micro-interaction, whileHover, whileTap, AnimatePresence, variants, drag, layout animation, morph, or any request to make UI feel alive/smooth/polished."
---

# Motion for React (Framer Motion) — Animation Pro Max

Build cinematic, 60fps animations in React. This skill covers the full Motion API (v12+), from basic enter/exit to complex orchestrated sequences, scroll-linked parallax, drag physics, and layout morphing.

## Package & Import

```bash
npm install motion
```

```tsx
// Motion v12+ (current)
import { motion, AnimatePresence } from "motion/react"

// Legacy (framer-motion v11 and below)
import { motion, AnimatePresence } from "framer-motion"
```

If the project uses `framer-motion` imports, keep them — both work. For new projects, use `motion/react`.

---

## Core API

### The `motion` Component

Every HTML/SVG element has a `motion` equivalent that accepts animation props:

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.5, ease: "easeOut" }}
/>
```

**Animatable properties:** All CSS transforms (x, y, z, rotate, rotateX, rotateY, scale, scaleX, scaleY, skew), opacity, colors (background, color, borderColor, fill, stroke), dimensions (width, height), border-radius, box-shadow, filter (blur, brightness, contrast, grayscale, saturate), clip-path, and CSS variables.

**Transform shorthand:** Use `x`, `y`, `scale`, `rotate` directly — NOT `transform: "translateX(100px)"`.

### Animation Props

| Prop | Purpose |
|------|---------|
| `initial` | State on mount (or `false` to skip) |
| `animate` | Target state — animates here on mount and when value changes |
| `exit` | State when removed (requires `AnimatePresence` parent) |
| `transition` | Duration, ease, spring config, delay |
| `whileHover` | State while pointer hovers |
| `whileTap` | State while pressed/tapped |
| `whileFocus` | State while focused |
| `whileInView` | State while in viewport |
| `whileDrag` | State while being dragged |
| `layout` | Animate layout changes automatically |
| `layoutId` | Shared layout animation between components |
| `drag` | Enable dragging (`true`, `"x"`, `"y"`) |
| `dragConstraints` | Boundaries for drag (ref or {top,right,bottom,left}) |
| `dragElastic` | Elasticity at boundaries (0-1) |
| `onAnimationStart` | Callback when animation begins |
| `onAnimationComplete` | Callback when animation finishes |
| `viewport` | Config for `whileInView` (once, margin, amount) |
| `style` | Can include MotionValues for reactive styles |

---

## Transition Types

### Spring (default for physical properties)

```tsx
transition={{
  type: "spring",
  stiffness: 300,    // Higher = snappier (default: 100)
  damping: 20,       // Higher = less bounce (default: 10)
  mass: 1,           // Higher = more inertia
  bounce: 0.25,      // Alternative: 0=no bounce, 1=max bounce
  duration: 0.8,     // Alternative to stiffness (estimated duration)
  velocity: 2,       // Initial velocity
}}
```

**Quick presets for springs:**
- Snappy button: `{ type: "spring", stiffness: 400, damping: 25 }`
- Bouncy entrance: `{ type: "spring", stiffness: 200, damping: 15 }`
- Smooth settle: `{ type: "spring", stiffness: 100, damping: 20 }`
- Heavy/dramatic: `{ type: "spring", stiffness: 80, damping: 12, mass: 2 }`

### Tween (default for non-physical properties like color)

```tsx
transition={{
  type: "tween",
  duration: 0.4,
  ease: "easeInOut",        // string preset
  ease: [0.25, 0.1, 0.25, 1], // cubic bezier
  repeat: Infinity,
  repeatType: "reverse",    // "loop" | "reverse" | "mirror"
  repeatDelay: 0.5,
}}
```

**Ease presets:** `"linear"`, `"easeIn"`, `"easeOut"`, `"easeInOut"`, `"circIn"`, `"circOut"`, `"circInOut"`, `"backIn"`, `"backOut"`, `"backInOut"`, `"anticipate"`

### Inertia (for drag/scroll momentum)

```tsx
transition={{
  type: "inertia",
  velocity: 100,
  power: 0.8,
  min: 0,
  max: 200,
}}
```

### Per-Property Transitions

```tsx
transition={{
  default: { duration: 0.3 },
  opacity: { duration: 0.2, ease: "linear" },
  x: { type: "spring", stiffness: 300 },
}}
```

---

## Variants — Orchestration Pattern

Variants define named animation states and propagate through children:

```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,      // Delay between each child
      delayChildren: 0.3,        // Delay before first child
      staggerDirection: 1,       // 1=forward, -1=reverse
      when: "beforeChildren",    // "beforeChildren" | "afterChildren"
    }
  },
  exit: {
    opacity: 0,
    transition: { staggerChildren: 0.05, staggerDirection: -1 }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -10 }
}

function StaggeredList({ items }) {
  return (
    <motion.ul variants={container} initial="hidden" animate="show" exit="exit">
      {items.map(i => (
        <motion.li key={i.id} variants={item}>{i.text}</motion.li>
      ))}
    </motion.ul>
  )
}
```

Children inherit `animate`/`initial`/`exit` from parents automatically. You only set `variants` on children — no need to repeat `animate="show"`.

---

## AnimatePresence — Exit Animations

Enables animations when components are removed from the tree:

```tsx
import { AnimatePresence } from "motion/react"

function App({ items }) {
  return (
    <AnimatePresence mode="wait">
      {items.map(item => (
        <motion.div
          key={item.id}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
        />
      ))}
    </AnimatePresence>
  )
}
```

**Modes:**
- `"sync"` (default) — enter and exit animate simultaneously
- `"wait"` — current exits fully before new enters
- `"popLayout"` — removes exiting from layout flow immediately

**Page transitions pattern (Next.js App Router):**
```tsx
// layout.tsx
"use client"
import { AnimatePresence } from "motion/react"
import { usePathname } from "next/navigation"

export default function Template({ children }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={usePathname()}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

---

## Gestures

### Hover + Tap

```tsx
<motion.button
  whileHover={{ scale: 1.05, boxShadow: "0 8px 30px rgba(0,0,0,0.2)" }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 25 }}
>
  Click me
</motion.button>
```

### Drag

```tsx
function DraggableCard() {
  const constraintsRef = useRef(null)

  return (
    <motion.div ref={constraintsRef} style={{ overflow: "hidden" }}>
      <motion.div
        drag
        dragConstraints={constraintsRef}
        dragElastic={0.1}
        dragMomentum={true}
        dragTransition={{ bounceStiffness: 600, bounceDamping: 20 }}
        whileDrag={{ scale: 1.1, cursor: "grabbing" }}
        onDragEnd={(e, { offset, velocity }) => {
          if (Math.abs(offset.x) > 200) dismiss()
        }}
      />
    </motion.div>
  )
}
```

---

## Scroll Animations

### whileInView — Trigger on scroll into viewport

```tsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px", amount: 0.3 }}
  transition={{ duration: 0.6 }}
/>
```

### useScroll — Scroll-linked values

```tsx
import { motion, useScroll, useTransform } from "motion/react"

function ParallaxHero() {
  const { scrollY } = useScroll()
  const y = useTransform(scrollY, [0, 500], [0, -150])
  const opacity = useTransform(scrollY, [0, 300], [1, 0])
  const scale = useTransform(scrollY, [0, 500], [1, 1.2])

  return (
    <motion.div style={{ y, opacity, scale }}>
      <img src="/hero.jpg" />
    </motion.div>
  )
}
```

**Scroll progress of a container:**
```tsx
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "end start"]  // when target enters/exits viewport
})
```

**Offset strings:** `"start"`, `"center"`, `"end"`, or pixels `"100px"`, or viewport-relative like `"start end"` (target start meets viewport end).

---

## Layout Animations

### Auto layout (the magic prop)

```tsx
// Just add layout — Motion handles the rest
<motion.div layout>
  {isExpanded && <p>Extra content here</p>}
</motion.div>
```

### Shared layout / morphing

```tsx
function Tabs({ tabs, activeTab, setActiveTab }) {
  return (
    <div style={{ display: "flex", gap: 8 }}>
      {tabs.map(tab => (
        <button key={tab.id} onClick={() => setActiveTab(tab.id)}>
          {tab.label}
          {activeTab === tab.id && (
            <motion.div
              layoutId="activeTab"
              style={{
                position: "absolute", bottom: 0, left: 0, right: 0,
                height: 2, background: "#E5B444"
              }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
            />
          )}
        </button>
      ))}
    </div>
  )
}
```

`layoutId` creates a seamless morph animation between two components with the same ID, even across different parent trees. This is how card-to-modal, tab indicators, and shared element transitions work.

---

## Hooks

### useAnimate — Imperative animations

```tsx
import { useAnimate } from "motion/react"

function Component() {
  const [scope, animate] = useAnimate()

  async function handleClick() {
    await animate(scope.current, { scale: 1.2 }, { duration: 0.2 })
    await animate(scope.current, { scale: 1 }, { type: "spring" })
    // Or animate children:
    await animate("li", { opacity: 1, y: 0 }, { delay: stagger(0.1) })
  }

  return <div ref={scope} onClick={handleClick}>...</div>
}
```

### useMotionValue — Reactive animation values

```tsx
import { useMotionValue, useTransform } from "motion/react"

function Slider() {
  const x = useMotionValue(0)
  const background = useTransform(x, [-100, 0, 100], ["#ff0000", "#ffffff", "#00ff00"])
  const scale = useTransform(x, [-100, 100], [0.8, 1.2])

  return <motion.div drag="x" style={{ x, background, scale }} />
}
```

### useInView

```tsx
import { useInView } from "motion/react"

function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return <div ref={ref} style={{ opacity: isInView ? 1 : 0 }} />
}
```

### useReducedMotion

```tsx
import { useReducedMotion } from "motion/react"

function Component() {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      animate={{ x: shouldReduceMotion ? 0 : 100 }}
      transition={shouldReduceMotion ? { duration: 0 } : { type: "spring" }}
    />
  )
}
```

---

## Performance Rules

1. **Animate transforms and opacity only** when possible — they run on the GPU compositor thread. Animating `width`, `height`, `top`, `left` causes layout recalculation and jank.
2. **Use `layout` prop** instead of animating width/height explicitly — Motion uses FLIP technique (transform-based) under the hood.
3. **LazyMotion** for bundle size — reduces initial load from ~30kb to ~5kb:
   ```tsx
   import { LazyMotion, domAnimation, m } from "motion/react"

   function App() {
     return (
       <LazyMotion features={domAnimation}>
         <m.div animate={{ opacity: 1 }} />  {/* use m. instead of motion. */}
       </LazyMotion>
     )
   }
   ```
4. **`will-change`** is applied automatically by Motion — don't add it manually.
5. **Keys matter** — give unique keys to AnimatePresence children to avoid animation glitches.
6. **`useReducedMotion`** — always respect accessibility preferences for users who get motion sickness.

---

## Common Patterns

### Staggered List Entrance
```tsx
const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } }
}
const item = {
  hidden: { opacity: 0, y: 20, filter: "blur(4px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)" }
}
```

### Notification Toast
```tsx
<AnimatePresence>
  {toast && (
    <motion.div
      initial={{ opacity: 0, y: 50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 20, scale: 0.9 }}
      transition={{ type: "spring", damping: 20 }}
    />
  )}
</AnimatePresence>
```

### Card Expand to Modal
```tsx
// Card
<motion.div layoutId={`card-${id}`} onClick={() => setSelected(id)}>
  <motion.img layoutId={`img-${id}`} src={item.image} />
  <motion.h2 layoutId={`title-${id}`}>{item.title}</motion.h2>
</motion.div>

// Modal (rendered when selected)
<AnimatePresence>
  {selected && (
    <motion.div layoutId={`card-${selected}`} className="modal">
      <motion.img layoutId={`img-${selected}`} />
      <motion.h2 layoutId={`title-${selected}`} />
      <p>Full content here...</p>
    </motion.div>
  )}
</AnimatePresence>
```

### Number Counter
```tsx
import { useMotionValue, useTransform, animate } from "motion/react"

function Counter({ target }) {
  const count = useMotionValue(0)
  const rounded = useTransform(count, v => Math.round(v))

  useEffect(() => {
    const controls = animate(count, target, { duration: 2 })
    return controls.stop
  }, [target])

  return <motion.span>{rounded}</motion.span>
}
```

### Infinite Marquee
```tsx
<div style={{ overflow: "hidden" }}>
  <motion.div
    animate={{ x: [0, -1920] }}
    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
    style={{ display: "flex", width: "fit-content" }}
  >
    {[...items, ...items].map((item, i) => <Card key={i} {...item} />)}
  </motion.div>
</div>
```

### Pulse / Glow
```tsx
<motion.div
  animate={{
    boxShadow: [
      "0 0 20px rgba(229,180,68,0.3)",
      "0 0 40px rgba(229,180,68,0.6)",
      "0 0 20px rgba(229,180,68,0.3)"
    ]
  }}
  transition={{ duration: 2, repeat: Infinity }}
/>
```

---

## With Snowball Design System

When building animations for Snowball, use these tokens:

```tsx
// Snowball springs
const snowballSprings = {
  snappy: { type: "spring", stiffness: 400, damping: 25 },
  smooth: { type: "spring", stiffness: 200, damping: 20 },
  bouncy: { type: "spring", stiffness: 300, damping: 15 },
  heavy:  { type: "spring", stiffness: 80, damping: 12, mass: 2 },
}

// Snowball colors for animated properties
const colors = {
  gold: "#E5B444",
  ice: "#C2E4EE",
  cream: "#EEE8DC",
  bg: "#060402",
}
```
