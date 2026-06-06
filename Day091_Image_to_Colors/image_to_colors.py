import argparse
import os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import colorsys


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def get_dominant_colors(image_path, n_colors=5):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((200, 200), Image.LANCZOS)
    pixels = np.array(img).reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)

    counts = np.bincount(kmeans.labels_)
    percentages = counts / len(kmeans.labels_) * 100

    colors_rgb = kmeans.cluster_centers_.astype(int)

    sorted_idx = np.argsort(counts)[::-1]
    colors_rgb = colors_rgb[sorted_idx]
    percentages = percentages[sorted_idx]

    return colors_rgb, percentages


def create_palette_image(colors_rgb, percentages, output_path):
    swatch_h = 80
    swatch_w = 400
    total_h = swatch_h * len(colors_rgb)

    palette = Image.new("RGB", (swatch_w, total_h), "white")
    for i, (color, pct) in enumerate(zip(colors_rgb, percentages)):
        y = i * swatch_h
        for x in range(swatch_w):
            for dy in range(swatch_h):
                palette.putpixel((x, y + dy), tuple(color))

    palette.save(output_path)
    return palette


def main():
    parser = argparse.ArgumentParser(description="Extract dominant colors from an image")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("-c", "--colors", type=int, default=5, help="Number of colors to extract (default: 5)")
    parser.add_argument("-o", "--output", default=None, help="Output palette image path")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Error: File not found: {args.image}")
        return

    if not args.output:
        base = os.path.splitext(os.path.basename(args.image))[0]
        args.output = f"{base}_palette.png"

    print(f"Analyzing: {args.image}")
    print(f"Extracting {args.colors} dominant colors...")

    colors_rgb, percentages = get_dominant_colors(args.image, args.colors)

    print(f"\n{'Rank':<6} {'Hex':<10} {'RGB':<20} {'%':<8}")
    print("-" * 45)
    for i, (color, pct) in enumerate(zip(colors_rgb, percentages)):
        hex_code = rgb_to_hex(color)
        rgb_str = f"({color[0]}, {color[1]}, {color[2]})"
        bar = "█" * int(pct / 2)
        print(f"#{i+1:<5} {hex_code:<10} {rgb_str:<20} {pct:5.1f}%  {bar}")

    create_palette_image(colors_rgb, percentages, args.output)
    print(f"\nPalette image saved to: {args.output}")


if __name__ == "__main__":
    main()
