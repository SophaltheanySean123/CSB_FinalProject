# AI Quiz Generator - Figma Style Guide

Complete reference for recreating the Quiz Generator layout in Figma.

---

## 📐 Typography

### Text Sizes & Line Heights

| Tailwind Class | Font Size | Line Height | Weight | Usage |
|---------------|-----------|-------------|---------|-------|
| `text-sm` | 14px | 21px (1.5) | 400 | Small text, labels, metadata |
| `text-base` | 16px | 24px (1.5) | 400 | Body text, default |
| `text-lg` | 18px | 27px (1.5) | 500 | Section labels, h3 headings |
| `text-xl` | 20px | 30px (1.5) | 500 | Subheadings, h2 headings |
| `text-2xl` | 24px | 36px (1.5) | 500 | Page headings, h1 headings |
| `text-3xl` | 30px | 45px (1.5) | 500 | Main quiz title |
| `text-4xl` | 36px | 54px (1.5) | 500 | Main page title |
| `text-6xl` | 60px | 90px (1.5) | 500 | Large percentage display |

### Font Weights

| Tailwind Class | Weight | Usage |
|---------------|--------|-------|
| `font-normal` | 400 | Body text, paragraphs, inputs |
| `font-medium` | 500 | Headings, labels, buttons |

---

## 🎨 Colors

### Primary Colors

| Color Name | HEX | RGB | HSL | Usage |
|-----------|-----|-----|-----|-------|
| Indigo 50 | `#EEF2FF` | `rgb(238, 242, 255)` | `hsl(225, 100%, 97%)` | Background light accent |
| Indigo 500 | `#6366F1` | `rgb(99, 102, 241)` | `hsl(239, 84%, 67%)` | Primary border active |
| Indigo 600 | `#4F46E5` | `rgb(79, 70, 229)` | `hsl(243, 75%, 59%)` | Primary button background |
| Indigo 700 | `#4338CA` | `rgb(67, 56, 202)` | `hsl(246, 58%, 51%)` | Primary button hover |

### Blue Colors

| Color Name | HEX | RGB | HSL | Usage |
|-----------|-----|-----|-----|-------|
| Blue 50 | `#EFF6FF` | `rgb(239, 246, 255)` | `hsl(214, 100%, 97%)` | Background gradient start |
| Blue 600 | `#2563EB` | `rgb(37, 99, 235)` | `hsl(221, 83%, 53%)` | Medium score indicator |

### Green Colors

| Color Name | HEX | RGB | HSL | Usage |
|-----------|-----|-----|-----|-------|
| Green 50 | `#F0FDF4` | `rgb(240, 253, 244)` | `hsl(138, 76%, 97%)` | Success background light |
| Green 500 | `#22C55E` | `rgb(34, 197, 94)` | `hsl(142, 71%, 45%)` | Answered indicator |
| Green 600 | `#16A34A` | `rgb(22, 163, 74)` | `hsl(142, 76%, 36%)` | Success state, correct answers, submit button |
| Green 700 | `#15803D` | `rgb(21, 128, 61)` | `hsl(142, 72%, 29%)` | Submit button hover |
| Green 900 | `#14532D` | `rgb(20, 83, 45)` | `hsl(140, 61%, 20%)` | Correct answer text |

### Red Colors

| Color Name | HEX | RGB | HSL | Usage |
|-----------|-----|-----|-----|-------|
| Red 50 | `#FEF2F2` | `rgb(254, 242, 242)` | `hsl(0, 86%, 97%)` | Error background light |
| Red 500 | `#EF4444` | `rgb(239, 68, 68)` | `hsl(0, 84%, 60%)` | Incorrect border |
| Red 600 | `#DC2626` | `rgb(220, 38, 38)` | `hsl(0, 73%, 51%)` | Error state, incorrect indicator |
| Red 900 | `#7F1D1D` | `rgb(127, 29, 29)` | `hsl(0, 63%, 31%)` | Incorrect answer text |

### Yellow Colors

| Color Name | HEX | RGB | HSL | Usage |
|-----------|-----|-----|-----|-------|
| Yellow 600 | `#CA8A04` | `rgb(202, 138, 4)` | `hsl(43, 96%, 40%)` | Low score indicator, warning text |

### Gray Colors

| Color Name | HEX | RGB | HSL | Usage |
|-----------|-----|-----|-----|-------|
| Gray 50 | `#F9FAFB` | `rgb(249, 250, 251)` | `hsl(210, 20%, 98%)` | Neutral background |
| Gray 200 | `#E5E7EB` | `rgb(229, 231, 235)` | `hsl(214, 14%, 91%)` | Borders, unanswered buttons |
| Gray 300 | `#D1D5DB` | `rgb(209, 213, 219)` | `hsl(214, 15%, 84%)` | Border default, hover states |
| Gray 400 | `#9CA3AF` | `rgb(156, 163, 175)` | `hsl(214, 11%, 65%)` | Icons, placeholder |
| Gray 500 | `#6B7280` | `rgb(107, 114, 128)` | `hsl(213, 9%, 46%)` | Muted text |
| Gray 600 | `#4B5563` | `rgb(75, 85, 99)` | `hsl(215, 14%, 34%)` | Secondary text, unanswered text |
| Gray 700 | `#374151` | `rgb(55, 65, 81)` | `hsl(217, 19%, 27%)` | Body text |
| Gray 800 | `#1F2937` | `rgb(31, 41, 55)` | `hsl(217, 28%, 17%)` | Option text |
| Gray 900 | `#111827` | `rgb(17, 24, 39)` | `hsl(222, 39%, 11%)` | Headings, primary text |

### White & Background

| Color Name | HEX | RGB | HSL | Usage |
|-----------|-----|-----|-----|-------|
| White | `#FFFFFF` | `rgb(255, 255, 255)` | `hsl(0, 0%, 100%)` | Card backgrounds, buttons |

---

## 🌈 Gradients

### Background Gradient (All Pages)

| Property | Value |
|---------|-------|
| Type | Linear gradient |
| Direction | Bottom-right (135°) |
| Start Color | Blue 50: `#EFF6FF` / `rgb(239, 246, 255)` |
| End Color | Indigo 100: `#E0E7FF` / `rgb(224, 231, 255)` |
| CSS | `background: linear-gradient(135deg, #EFF6FF 0%, #E0E7FF 100%)` |

---

## 📏 Spacing & Sizing

### Padding Values

| Tailwind Class | Pixels | Usage |
|---------------|--------|-------|
| `p-2` | 8px | Small padding |
| `p-3` | 12px | Answer option padding |
| `p-4` | 16px | Medium padding, header badge |
| `p-6` | 24px | Card padding (results detail) |
| `p-8` | 32px | Large card padding, page padding |
| `p-12` | 48px | Upload dropzone padding |
| `px-4` | 16px left/right | Badge horizontal padding |
| `px-6` | 24px left/right | Button horizontal padding |
| `px-8` | 32px left/right | Large button horizontal padding |
| `py-2` | 8px top/bottom | Badge vertical padding |
| `py-6` | 24px top/bottom | Large button vertical padding |

### Margin Values

| Tailwind Class | Pixels | Usage |
|---------------|--------|-------|
| `mb-2` | 8px | Small bottom margin |
| `mb-4` | 16px | Medium bottom margin |
| `mb-6` | 24px | Large section spacing |
| `mb-8` | 32px | Page section spacing |
| `mr-2` | 8px | Icon/text spacing |
| `mt-1` | 4px | Radio button top margin |
| `mt-3` | 12px | Warning message top margin |
| `mt-4` | 16px | Range slider top margin |
| `mt-8` | 32px | Button group top margin |

### Gap Values

| Tailwind Class | Pixels | Usage |
|---------------|--------|-------|
| `gap-2` | 8px | Icon and text, question number navigation |
| `gap-3` | 12px | File upload icon and name |
| `gap-4` | 16px | Form elements, button groups |
| `space-x-3` | 12px | Radio and label horizontal spacing |
| `space-y-2` | 8px | Answer options vertical spacing |
| `space-y-4` | 16px | Radio options vertical spacing |
| `space-y-6` | 24px | Form sections vertical spacing |

### Width & Height Values

| Tailwind Class | Pixels | Usage |
|---------------|--------|-------|
| `w-4` | 16px | Small icon width |
| `w-5` | 20px | Medium icon width |
| `w-6` | 24px | Large icon width |
| `w-8` | 32px | Icon, question number button |
| `w-12` | 48px | Upload icon width |
| `w-20` | 80px | Award icon width |
| `h-2` | 8px | Progress bar height |
| `h-4` | 16px | Small icon height |
| `h-5` | 20px | Medium icon height |
| `h-6` | 24px | Large icon height |
| `h-8` | 32px | Icon, question number button |
| `h-12` | 48px | Upload icon height |
| `h-20` | 80px | Award icon height |
| `max-w-xs` | 320px | Input field max width |
| `max-w-3xl` | 768px | Upload page container |
| `max-w-4xl` | 896px | Quiz/Results page container |
| `min-h-screen` | 100vh | Full screen height |

---

## 🔲 Borders & Radius

### Border Width

| Tailwind Class | Pixels | Usage |
|---------------|--------|-------|
| `border` | 1px | Default border |
| `border-2` | 2px | Upload dropzone, answer options |

### Border Radius

| Tailwind Class | Pixels | Usage |
|---------------|--------|-------|
| `rounded-lg` | 10px (0.625rem) | Cards, buttons, inputs, options |
| `rounded-full` | 9999px | Question number buttons (circular) |

### Border Colors (Referenced Above)

- Default: `border-gray-200` → `#E5E7EB`
- Hover: `border-indigo-300` → `#A5B4FC`
- Active: `border-indigo-500` → `#6366F1`
- Success: `border-green-500` → `#22C55E`
- Error: `border-red-500` → `#EF4444`
- Dashed: Used in upload dropzone

---

## 🎯 Component-Specific Spacing

### Upload Page

| Element | Padding/Margin | Size |
|---------|---------------|------|
| Page wrapper | `p-8` = 32px | - |
| Container | `max-w-3xl` = 768px | - |
| Title margin bottom | `mb-4` = 16px | - |
| Section margin bottom | `mb-8` = 32px | - |
| Card padding | `p-8` = 32px | - |
| Upload dropzone padding | `p-12` = 48px | - |
| Button margin top | `mt-4` = 16px | - |

### Quiz Page

| Element | Padding/Margin | Size |
|---------|---------------|------|
| Page wrapper | `p-8` = 32px | - |
| Container | `max-w-4xl` = 896px | - |
| Header margin bottom | `mb-6` = 24px | - |
| Card padding | `p-8` = 32px | - |
| Card margin bottom | `mb-6` = 24px | - |
| Option padding | `p-4` = 16px | - |
| Question number button | `w-8 h-8` = 32px × 32px | Circular |

### Results Page

| Element | Padding/Margin | Size |
|---------|---------------|------|
| Page wrapper | `p-8` = 32px | - |
| Container | `max-w-4xl` = 896px | - |
| Score card padding | `p-8` = 32px | - |
| Score card margin bottom | `mb-8` = 32px | - |
| Detail card padding | `p-6` = 24px | - |
| Answer option padding | `p-3` = 12px | - |

---

## 🖼️ Shadows

### Shadow Values (Tailwind)

| Tailwind Class | CSS Box Shadow | Usage |
|---------------|---------------|-------|
| `shadow` | 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1) | Header badge, default |
| `shadow-md` | 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1) | Results detail cards |
| `shadow-lg` | 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1) | Main cards (upload, quiz, results) |

---

## 🎭 States & Interactions

### Button States

| State | Background | Text | Border |
|-------|-----------|------|--------|
| Primary Default | Indigo 600 `#4F46E5` | White `#FFFFFF` | - |
| Primary Hover | Indigo 700 `#4338CA` | White `#FFFFFF` | - |
| Primary Disabled | Gray 300 `#D1D5DB` | Gray 500 `#6B7280` | - |
| Success Default | Green 600 `#16A34A` | White `#FFFFFF` | - |
| Success Hover | Green 700 `#15803D` | White `#FFFFFF` | - |
| Outline Default | White `#FFFFFF` | Gray 900 `#111827` | Gray 300 `#D1D5DB` |
| Outline Hover | Gray 50 `#F9FAFB` | Gray 900 `#111827` | Gray 400 `#9CA3AF` |

### Answer Option States

| State | Background | Border | Text |
|-------|-----------|--------|------|
| Default | White `#FFFFFF` | Gray 200 `#E5E7EB` | Gray 800 `#1F2937` |
| Hover | White `#FFFFFF` | Indigo 300 `#A5B4FC` | Gray 800 `#1F2937` |
| Selected | Indigo 50 `#EEF2FF` | Indigo 500 `#6366F1` | Gray 800 `#1F2937` |
| Correct (Results) | Green 50 `#F0FDF4` | Green 500 `#22C55E` | Green 900 `#14532D` |
| Incorrect (Results) | Red 50 `#FEF2F2` | Red 500 `#EF4444` | Red 900 `#7F1D1D` |

### Question Number Button States

| State | Background | Text |
|-------|-----------|------|
| Current | Indigo 600 `#4F46E5` | White `#FFFFFF` |
| Answered | Green 500 `#22C55E` | White `#FFFFFF` |
| Unanswered | Gray 200 `#E5E7EB` | Gray 600 `#4B5563` |
| Unanswered Hover | Gray 300 `#D1D5DB` | Gray 600 `#4B5563` |

### Upload Dropzone States

| State | Background | Border |
|-------|-----------|--------|
| Default | White `#FFFFFF` | Gray 300 `#D1D5DB` dashed |
| Hover | White `#FFFFFF` | Indigo 400 `#818CF8` dashed |
| Dragging | Indigo 50 `#EEF2FF` | Indigo 500 `#6366F1` dashed |
| File Selected | Green 50 `#F0FDF4` | Green 500 `#22C55E` dashed |

---

## 📊 Icon Sizes

| Usage | Size Class | Pixels |
|-------|-----------|--------|
| Small icons (in buttons) | `w-4 h-4` | 16 × 16px |
| Medium icons (header) | `w-5 h-5` | 20 × 20px |
| Large icons (status) | `w-6 h-6` | 24 × 24px |
| Icon buttons | `w-8 h-8` | 32 × 32px |
| Upload icon | `w-12 h-12` | 48 × 48px |
| Award icon | `w-20 h-20` | 80 × 80px |

---

## 🔄 Transitions

All interactive elements use:
- **Property**: `all`
- **Duration**: `150ms` (default Tailwind transition)
- **Timing Function**: `cubic-bezier(0.4, 0, 0.2, 1)` (ease-in-out)

Applied with Tailwind class: `transition-all`

---

## 📱 Responsive Breakpoints

While the current design is primarily desktop-focused, these are standard Tailwind breakpoints:

| Breakpoint | Min Width | Usage |
|-----------|-----------|-------|
| `sm` | 640px | Small tablets |
| `md` | 768px | Tablets |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Large desktop |
| `2xl` | 1536px | Extra large desktop |

---

## 🎨 Quick Reference: Color Palette Summary

### Primary Palette
- **Indigo 600**: `#4F46E5` - Primary actions
- **Green 600**: `#16A34A` - Success states
- **Red 600**: `#DC2626` - Error states
- **Gray 900**: `#111827` - Primary text
- **Gray 600**: `#4B5563` - Secondary text

### Background Palette
- **White**: `#FFFFFF` - Cards
- **Blue 50**: `#EFF6FF` - Gradient start
- **Indigo 100**: `#E0E7FF` - Gradient end
- **Indigo 50**: `#EEF2FF` - Selected state
- **Green 50**: `#F0FDF4` - Success background
- **Red 50**: `#FEF2F2` - Error background

---

## 💡 Tips for Figma Implementation

1. **Create a Color Styles Library**: Set up all colors as Figma color styles for consistency
2. **Text Styles**: Create text styles for each typography combination (size + weight + line-height)
3. **Component Variants**: Use Figma variants for button states, option states, etc.
4. **Auto Layout**: Use auto layout with the spacing values above for proper padding/gaps
5. **Effects**: Create shadow effects matching the values in the shadows section
6. **Grid Layout**: Use 8px grid system for spacing consistency

---

*This style guide is generated from the Quiz Generator application codebase and represents the exact values used in the implementation.*
