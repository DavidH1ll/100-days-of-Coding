from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory
script_dir = Path(__file__).parent
images_dir = script_dir / "images"
images_dir.mkdir(exist_ok=True)

print(f"Creating images in: {images_dir}")

# Create card_front.png (white card)
card_front = Image.new('RGB', (800, 526), color='white')
draw = ImageDraw.Draw(card_front)
# Add a border
draw.rectangle([10, 10, 790, 516], outline='black', width=3)
card_front.save(images_dir / "card_front.png")
print("✓ Created card_front.png")

# Create card_back.png (green card)
card_back = Image.new('RGB', (800, 526), color='#91C788')
draw = ImageDraw.Draw(card_back)
draw.rectangle([10, 10, 790, 516], outline='black', width=3)
card_back.save(images_dir / "card_back.png")
print("✓ Created card_back.png")

# Create right.png (checkmark button)
right_btn = Image.new('RGBA', (100, 100), color=(0, 255, 0, 0))
draw = ImageDraw.Draw(right_btn)
draw.ellipse([10, 10, 90, 90], fill='#4CAF50', outline='darkgreen', width=3)
# Draw checkmark
draw.line([30, 50, 45, 65], fill='white', width=8)
draw.line([45, 65, 70, 30], fill='white', width=8)
right_btn.save(images_dir / "right.png")
print("✓ Created right.png")

# Create wrong.png (X button)
wrong_btn = Image.new('RGBA', (100, 100), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(wrong_btn)
draw.ellipse([10, 10, 90, 90], fill='#F44336', outline='darkred', width=3)
# Draw X
draw.line([30, 30, 70, 70], fill='white', width=8)
draw.line([70, 30, 30, 70], fill='white', width=8)
wrong_btn.save(images_dir / "wrong.png")
print("✓ Created wrong.png")

print("\n✅ All images created successfully!")
print(f"Images location: {images_dir.absolute()}")
