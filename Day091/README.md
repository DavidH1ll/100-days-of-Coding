# Day 91 - Image to Color List

## Overview
Extracts dominant colors from any image using K-Means clustering. Outputs hex codes, RGB values, and percentages, plus generates a color palette visualization image.

## Features
- K-Means clustering for color quantization
- Configurable number of colors (default 5)
- Console output with hex, RGB, and percentage
- ASCII bar visualization in terminal
- Saves palette image with color swatches

## Key Concepts
- sklearn.cluster.KMeans for unsupervised clustering
- Pillow for image loading and pixel manipulation
- RGB ↔ Hex color conversion
- Reshaping image arrays for ML input

## Reflection
K-Means is surprisingly effective for color extraction. The key insight is treating each pixel as a 3D data point (R, G, B) and letting K-Means find the centroids. Resizing to 200×200 before clustering makes it fast without losing color accuracy.

**Day 91 Complete!** ✅
