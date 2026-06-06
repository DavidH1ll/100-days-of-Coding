import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
import io
import os

BACKGROUND_COLOR = "#2d2d2d"
CONTROL_BG = "#3c3c3c"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#4a9eff"
ACCENT_HOVER = "#3a8eef"
BUTTON_BG = "#4a9eff"
BUTTON_FG = "#ffffff"
CANVAS_BG = "#1e1e1e"
ENTRY_BG = "#555555"


def pil_to_tk_image(pil_image):
    buf = io.BytesIO()
    pil_image.save(buf, format='PPM')
    buf.seek(0)
    return tk.PhotoImage(data=buf.read())


class WatermarkApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Watermark Application")
        self.window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
        self.window.minsize(800, 700)

        self.original_image = None
        self.watermarked_image = None
        self.preview_image = None
        self.canvas_image_id = None
        self.logo_watermark = None
        self.watermark_type = tk.StringVar(value="text")

        self._build_title()
        self._build_canvas()
        self._build_controls()

    def _build_title(self):
        frame = tk.Frame(self.window, bg=BACKGROUND_COLOR)
        frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tk.Label(
            frame, text="\U0001f4f7 Watermark Application",
            font=("Arial", 20, "bold"), fg=ACCENT_COLOR, bg=BACKGROUND_COLOR
        ).pack()

        tk.Label(
            frame,
            text="Add text or logo watermarks to your images",
            font=("Arial", 11), fg="#aaaaaa", bg=BACKGROUND_COLOR
        ).pack()

    def _build_canvas(self):
        self.canvas = tk.Canvas(
            self.window, width=760, height=400,
            bg=CANVAS_BG, highlightthickness=0, relief="ridge"
        )
        self.canvas.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        self.canvas.create_text(
            380, 180,
            text="Upload an image to get started",
            fill="#666666", font=("Arial", 14, "italic")
        )
        self.canvas.create_text(
            380, 210,
            text="Supported formats: PNG, JPG, JPEG, BMP, GIF",
            fill="#555555", font=("Arial", 10)
        )

    def _build_controls(self):
        controls = tk.Frame(self.window, bg=CONTROL_BG, padx=20, pady=15)
        controls.grid(row=2, column=0, sticky="ew")
        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)

        row = 0

        # Upload button
        self.upload_btn = tk.Button(
            controls, text="\u2b07 Upload Image", font=("Arial", 11, "bold"),
            bg=ACCENT_COLOR, fg=BUTTON_FG, activebackground=ACCENT_HOVER,
            activeforeground=BUTTON_FG, relief="flat", padx=16, pady=6,
            cursor="hand2", highlightthickness=0,
            command=self._upload_image
        )
        self.upload_btn.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        row += 1

        # Watermark type
        tk.Label(
            controls, text="Watermark Type:", font=("Arial", 10, "bold"),
            fg=TEXT_COLOR, bg=CONTROL_BG
        ).grid(row=row, column=0, sticky="w", pady=4)

        type_frame = tk.Frame(controls, bg=CONTROL_BG)
        type_frame.grid(row=row, column=1, sticky="e")
        row += 1

        tk.Radiobutton(
            type_frame, text="Text", variable=self.watermark_type, value="text",
            font=("Arial", 10), fg=TEXT_COLOR, bg=CONTROL_BG,
            selectcolor=CONTROL_BG, activebackground=CONTROL_BG,
            activeforeground=ACCENT_COLOR, highlightthickness=0,
            command=self._toggle_watermark_fields
        ).pack(side="left", padx=(0, 15))

        tk.Radiobutton(
            type_frame, text="Logo", variable=self.watermark_type, value="logo",
            font=("Arial", 10), fg=TEXT_COLOR, bg=CONTROL_BG,
            selectcolor=CONTROL_BG, activebackground=CONTROL_BG,
            activeforeground=ACCENT_COLOR, highlightthickness=0,
            command=self._toggle_watermark_fields
        ).pack(side="left")

        # Text watermark fields
        self.text_frame = tk.Frame(controls, bg=CONTROL_BG)
        self.text_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=4)
        row += 1

        tk.Label(
            self.text_frame, text="Text:", font=("Arial", 10),
            fg=TEXT_COLOR, bg=CONTROL_BG
        ).pack(side="left", padx=(0, 6))

        self.text_entry = tk.Entry(
            self.text_frame, font=("Arial", 11), bg=ENTRY_BG, fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR, relief="flat", width=22
        )
        self.text_entry.insert(0, "Your Watermark")
        self.text_entry.pack(side="left", padx=(0, 10))

        tk.Label(
            self.text_frame, text="Size:", font=("Arial", 10),
            fg=TEXT_COLOR, bg=CONTROL_BG
        ).pack(side="left", padx=(0, 6))

        self.font_size = tk.IntVar(value=36)
        self.font_spinbox = tk.Spinbox(
            self.text_frame, from_=8, to=120, textvariable=self.font_size,
            width=4, font=("Arial", 10), bg=ENTRY_BG, fg=TEXT_COLOR,
            buttonbackground=BUTTON_BG, relief="flat"
        )
        self.font_spinbox.pack(side="left")

        # Logo watermark fields
        self.logo_frame = tk.Frame(controls, bg=CONTROL_BG)
        self.logo_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=4)
        self.logo_frame.grid_remove()
        row += 1

        self.logo_label = tk.Label(
            self.logo_frame, text="No logo selected", font=("Arial", 10),
            fg="#999999", bg=CONTROL_BG, anchor="w"
        )
        self.logo_label.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.logo_btn = tk.Button(
            self.logo_frame, text="Browse", font=("Arial", 10),
            bg="#666666", fg=BUTTON_FG, activebackground="#777777",
            activeforeground=BUTTON_FG, relief="flat", padx=10, pady=2,
            cursor="hand2", highlightthickness=0,
            command=self._upload_logo
        )
        self.logo_btn.pack(side="right")

        # Logo size control
        tk.Label(
            self.logo_frame, text="Size %:", font=("Arial", 10),
            fg=TEXT_COLOR, bg=CONTROL_BG
        ).pack(side="right", padx=(10, 6))

        self.logo_scale_var = tk.IntVar(value=15)
        tk.Spinbox(
            self.logo_frame, from_=5, to=50, textvariable=self.logo_scale_var,
            width=4, font=("Arial", 10), bg=ENTRY_BG, fg=TEXT_COLOR,
            buttonbackground=BUTTON_BG, relief="flat"
        ).pack(side="right")

        # Opacity
        tk.Label(
            controls, text="Opacity:", font=("Arial", 10, "bold"),
            fg=TEXT_COLOR, bg=CONTROL_BG
        ).grid(row=row, column=0, sticky="w", pady=(12, 0))
        row += 1

        self.opacity_var = tk.IntVar(value=50)
        self.opacity_scale = tk.Scale(
            controls, from_=5, to=100, orient="horizontal",
            variable=self.opacity_var, length=200,
            font=("Arial", 9), fg=TEXT_COLOR, bg=CONTROL_BG,
            troughcolor=ENTRY_BG, activebackground=ACCENT_COLOR,
            highlightthickness=0, cursor="hand2"
        )
        self.opacity_scale.grid(row=row, column=0, sticky="w", pady=(0, 6))

        self.opacity_label = tk.Label(
            controls, text="50%", font=("Arial", 10),
            fg=ACCENT_COLOR, bg=CONTROL_BG
        )
        self.opacity_label.grid(row=row, column=0, padx=(220, 0))
        self.opacity_var.trace_add("write", lambda *a: self._update_opacity_label())

        # Position
        tk.Label(
            controls, text="Position:", font=("Arial", 10, "bold"),
            fg=TEXT_COLOR, bg=CONTROL_BG
        ).grid(row=row, column=1, sticky="e", padx=(0, 10))
        row += 1

        self.position_var = tk.StringVar(value="Bottom Right")
        self.position_menu = ttk.Combobox(
            controls, textvariable=self.position_var, state="readonly",
            values=["Top Left", "Top Right", "Center", "Bottom Left", "Bottom Right"],
            font=("Arial", 10), width=14
        )
        self.position_menu.grid(row=row, column=1, sticky="e", pady=(0, 6))

        # Action buttons
        btn_frame = tk.Frame(controls, bg=CONTROL_BG)
        btn_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        row += 1

        self.apply_btn = tk.Button(
            btn_frame, text="\u2728 Add Watermark", font=("Arial", 11, "bold"),
            bg="#4caf50", fg=BUTTON_FG, activebackground="#43a047",
            activeforeground=BUTTON_FG, relief="flat", padx=14, pady=6,
            cursor="hand2", highlightthickness=0,
            command=self._apply_watermark
        )
        self.apply_btn.pack(side="left")

        self.save_btn = tk.Button(
            btn_frame, text="\U0001f4be Save Image", font=("Arial", 11, "bold"),
            bg="#ff9800", fg=BUTTON_FG, activebackground="#f57c00",
            activeforeground=BUTTON_FG, relief="flat", padx=14, pady=6,
            cursor="hand2", highlightthickness=0,
            command=self._save_image
        )
        self.save_btn.pack(side="left", padx=(10, 0))

    def _toggle_watermark_fields(self):
        if self.watermark_type.get() == "text":
            self.logo_frame.grid_remove()
            self.text_frame.grid()
        else:
            self.text_frame.grid_remove()
            self.logo_frame.grid()

    def _update_opacity_label(self):
        self.opacity_label.config(text=f"{self.opacity_var.get()}%")

    def _upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        if not file_path:
            return

        try:
            self.original_image = Image.open(file_path).convert("RGBA")
            self.watermarked_image = None
            self._show_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{str(e)}")

    def _upload_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select a Logo Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        if not file_path:
            return

        try:
            self.logo_watermark = Image.open(file_path).convert("RGBA")
            filename = os.path.basename(file_path)
            self.logo_label.config(text=filename, fg=ACCENT_COLOR)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open logo:\n{str(e)}")

    def _show_preview(self):
        if self.original_image is None:
            return

        canvas_w = self.canvas.winfo_width() or 760
        canvas_h = self.canvas.winfo_height() or 400
        margin = 20
        max_w = canvas_w - margin * 2
        max_h = canvas_h - margin * 2

        display = self.watermarked_image if self.watermarked_image else self.original_image
        img = display.copy()
        img.thumbnail((max_w, max_h), Image.LANCZOS)

        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, CANVAS_BG)
            bg.paste(img, mask=img.split()[3])
            img = bg

        self.preview_image = pil_to_tk_image(img)
        self.canvas.delete("all")

        if self.canvas_image_id is None:
            self.canvas_image_id = self.canvas.create_image(
                canvas_w // 2, canvas_h // 2,
                image=self.preview_image, anchor="center"
            )
        else:
            self.canvas.itemconfig(self.canvas_image_id, image=self.preview_image)
            self.canvas.coords(self.canvas_image_id, canvas_w // 2, canvas_h // 2)

    def _apply_watermark(self):
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return

        img = self.original_image.copy()
        opacity = int(self.opacity_var.get() * 255 / 100)
        position = self.position_var.get()

        if self.watermark_type.get() == "text":
            text = self.text_entry.get().strip()
            if not text:
                messagebox.showwarning("No Text", "Please enter watermark text.")
                return
            img = self._add_text_watermark(img, text, opacity, position)
        else:
            if self.logo_watermark is None:
                messagebox.showwarning("No Logo", "Please select a logo image.")
                return
            img = self._add_logo_watermark(img, opacity, position)

        self.watermarked_image = img
        self._show_preview()

    def _add_text_watermark(self, img, text, opacity, position):
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        font_size = self.font_size.get()
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except (OSError, IOError):
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except (OSError, IOError):
                font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        x, y = self._get_position(img.size[0], img.size[1], text_w, text_h, position)
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))

        return Image.alpha_composite(img, overlay)

    def _add_logo_watermark(self, img, opacity, position):
        logo = self.logo_watermark.copy()

        scale_pct = self.logo_scale_var.get()
        new_w = int(img.size[0] * scale_pct / 100)
        aspect = logo.size[1] / logo.size[0] if logo.size[0] > 0 else 1
        new_h = int(new_w * aspect)
        logo = logo.resize((new_w, new_h), Image.LANCZOS)

        if logo.mode == "RGBA":
            r, g, b, a = logo.split()
            a = a.point(lambda p: int(p * opacity / 255))
            logo = Image.merge("RGBA", (r, g, b, a))
        else:
            overlay_alpha = Image.new("L", logo.size, opacity)
            logo.putalpha(overlay_alpha)

        x, y = self._get_position(img.size[0], img.size[1], new_w, new_h, position)
        img.paste(logo, (x, y), logo)

        return img

    def _get_position(self, img_w, img_h, elem_w, elem_h, position):
        margin = 20
        positions = {
            "Top Left": (margin, margin),
            "Top Right": (img_w - elem_w - margin, margin),
            "Center": ((img_w - elem_w) // 2, (img_h - elem_h) // 2),
            "Bottom Left": (margin, img_h - elem_h - margin),
            "Bottom Right": (img_w - elem_w - margin, img_h - elem_h - margin),
        }
        return positions.get(position, positions["Bottom Right"])

    def _save_image(self):
        image_to_save = self.watermarked_image or self.original_image
        if image_to_save is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return

        if self.watermarked_image is None:
            if not messagebox.askyesno(
                "No Watermark",
                "You haven't applied a watermark yet. Save the original image?"
            ):
                return

        file_path = filedialog.asksaveasfilename(
            title="Save Watermarked Image",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        if not file_path:
            return

        try:
            save_img = image_to_save.convert("RGB")
            save_img.save(file_path)
            messagebox.showinfo("Success", f"Image saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image:\n{str(e)}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    try:
        app = WatermarkApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application crashed:\n{str(e)}")
