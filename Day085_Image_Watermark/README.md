# Day 85 - Image Watermark Application

## Overview
A desktop GUI application built with Tkinter and Pillow that lets you automatically add text or logo watermarks to images. No Photoshop required — upload an image, configure your watermark (text content, font size, opacity, position, or a logo image), preview the result in real-time, and export.

## Features

- **Text Watermarks**: Customizable text, font size (8-120pt), opacity (5-100%), and 5 position options
- **Logo Watermarks**: Upload a PNG/JPEG logo, scale it (5-50% of image width), control opacity and position
- **Live Preview**: See your watermarked image on the canvas before saving
- **Position Control**: Top Left, Top Right, Center, Bottom Left, Bottom Right with smart margin
- **Save Export**: Save as PNG or JPEG to any location
- **Supports**: PNG, JPG, JPEG, BMP, GIF input formats
- **RGBA Compositing**: Proper alpha-channel blending for semi-transparent logos

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python Day085/watermark_gui.py
```

### Interface

```
┌──────────────────────────────────────┐
│       📷 Watermark Application       │
├──────────────────────────────────────┤
│                                      │
│        [Image Preview Canvas]        │
│                                      │
├──────────────────────────────────────┤
│ [⬇ Upload Image]                    │
│                                      │
│ ○ Text Watermark   ○ Logo Watermark │
│ Text: [Your Watermark]  Size: [36]  │
│                                      │
│ Opacity: [====▬========] 75%        │
│ Position: [▾ Bottom Right     ]     │
│                                      │
│ [✨ Add Watermark]  [💾 Save Image] │
└──────────────────────────────────────┘
```

## How It Works

### Text Watermarking
1. User text is drawn onto a transparent RGBA overlay using `ImageDraw.text()`
2. The overlay is alpha-composited with the original image
3. Font: DejaVu Sans Bold (Linux), falls back to Arial (Windows), then PIL default

### Logo Watermarking
1. Logo image is loaded in RGBA mode, scaled to a percentage of the base image width
2. Alpha channel is adjusted by the opacity slider
3. Logo is pasted onto the base image at the chosen position using its alpha channel as a mask

### Image Preview (PPM Workaround)
Since `PIL.ImageTk` may not be available in all Pillow installations, images are converted to PPM format in memory and loaded by `tk.PhotoImage(data=...)`. RGBA images are composited onto the canvas background color first since PPM doesn't support transparency.

## Key Concepts

- **Tkinter GUI**: Canvas, Scale, Entry, Spinbox, Combobox, Radiobutton, filedialog, messagebox
- **Pillow Image Processing**: RGBA compositing, alpha channel manipulation, thumbnail resizing, format conversion
- **Class-based Architecture**: `WatermarkApp` encapsulates all widgets, state, and image processing
- **PPM In-Memory Conversion**: Workaround for environments without `ImageTk`

## Reflection

### How I Approached the Project

I started by auditing all existing Tkinter projects in the repo (Days 27, 28, 29, 31, 34) to extract conventions — the `tk.Tk()` + `window.config()` setup, `grid()` layout dominance, UPPER_CASE color constants, Canvas usage for image display, and class-based architecture for complex projects (like Day 34's QuizInterface). I structured the app as a single `WatermarkApp` class with methods for each UI section (`_build_title`, `_build_canvas`, `_build_controls`) and separate methods for the two watermark types.

### What Was Hard

**ImageTk was unavailable.** The `from PIL import ImageTk` import failed because this system's Pillow was compiled without Tk support (`tk-devel` missing at build time). This meant I couldn't use `ImageTk.PhotoImage` to display PIL images on the canvas. I solved it by converting images to PPM format in a `BytesIO` buffer and passing the raw bytes to `tk.PhotoImage(data=...)`. For RGBA images, I first composited them onto a solid background since PPM doesn't support alpha channels. This added complexity but made the app work everywhere without compile-time dependencies.

**Alpha compositing for logo watermarks.** Getting the opacity right for logo images required splitting the RGBA channels, scaling the alpha channel with `point(lambda p: int(p * opacity / 255))`, then merging them back. Using `paste()` with the logo as its own mask handled the per-pixel transparency correctly.

### What Was Easy

**The Tkinter layout** fell into place quickly since I'd studied the existing patterns. The `grid()` layout with `columnspan=2` for full-width elements, the `control_frame` wrapper pattern, and toggle visibility with `grid()`/`grid_remove()` for the text vs logo fields all mirrored existing repo conventions. **Position calculation** was five simple coordinate tuples — the hardest part was remembering the margin offset.

### Biggest Learning

The `PPM`/`BytesIO` workaround taught me that understanding your toolchain's limitations is as important as knowing its features. Rather than fighting a missing system package, I found the lowest-common-denominator format that both Pillow (write) and Tkinter (read) support. This "find the overlap" approach is broadly applicable — not just for image formats but for any interoperability problem. Also, `Image.paste()` with a mask argument handles alpha compositing correctly, which was not immediately obvious from the Pillow docs.

### What I'd Do Differently

1. **Add drag-and-drop support** via Tkinter DnD — clicking "Browse" is functional but feels clunky for a desktop app
2. **Add a tiling/repeat mode** for watermarks (cover the entire image with repeated text/logos for stronger protection)
3. **Add rotation** — diagonal watermarks are harder to crop out
4. **Batch processing** — apply the same watermark to a folder of images at once
5. **Use `tkinter.ttk` properly** — the app mixes classic Tk and ttk widgets (the Combobox is ttk but buttons are classic). A uniform ttk approach with custom `ttk.Style` would be cleaner
6. **Add undo/reset** — once you apply a watermark, there's no way to revert without re-uploading the original

---

**Day 85: Complete!** ✅
