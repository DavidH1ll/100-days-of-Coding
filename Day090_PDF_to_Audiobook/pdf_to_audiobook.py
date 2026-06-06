import argparse
import os
import sys


def extract_text_pypdf2(pdf_path):
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            if (i + 1) % 5 == 0:
                print(f"  Extracted {i + 1}/{len(reader.pages)} pages...")
        return text.strip()
    except ImportError:
        print("Error: PyPDF2 not installed. Install with: pip install PyPDF2")
        return None


def extract_text_pdfplumber(pdf_path):
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                if (i + 1) % 5 == 0:
                    print(f"  Extracted {i + 1}/{len(pdf.pages)} pages...")
        return text.strip()
    except ImportError:
        print("Error: pdfplumber not installed. Install with: pip install pdfplumber")
        return None


def text_to_speech_gtts(text, output_path):
    try:
        from gtts import gTTS
        print(f"  Converting {len(text)} characters to speech...")
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(output_path)
        return True
    except ImportError:
        print("Error: gTTS not installed. Install with: pip install gTTS")
        return False


def text_to_speech_pyttsx3(text, output_path):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return True
    except ImportError:
        print("Error: pyttsx3 not installed. Install with: pip install pyttsx3")
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert a PDF to an audiobook (MP3)")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("-o", "--output", default=None, help="Output MP3 file path")
    parser.add_argument("--engine", choices=["gtts", "pyttsx3"], default="gtts",
                        help="Text-to-speech engine (default: gtts)")
    parser.add_argument("--extractor", choices=["pypdf2", "pdfplumber"], default="pypdf2",
                        help="PDF text extractor (default: pypdf2)")
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"Error: File not found: {args.pdf}")
        sys.exit(1)

    if not args.output:
        base = os.path.splitext(os.path.basename(args.pdf))[0]
        args.output = f"{base}_audiobook.mp3"

    print("=" * 50)
    print("PDF TO AUDIOBOOK CONVERTER")
    print("=" * 50)
    print(f"Input:  {args.pdf}")
    print(f"Output: {args.output}")
    print(f"Engine: {args.engine}")
    print()

    print("[1/2] Extracting text from PDF...")
    if args.extractor == "pdfplumber":
        text = extract_text_pdfplumber(args.pdf)
    else:
        text = extract_text_pypdf2(args.pdf)

    if text is None:
        sys.exit(1)
    if not text:
        print("Error: No text could be extracted from the PDF.")
        sys.exit(1)

    print(f"  Done! Extracted {len(text)} characters, ~{len(text.split())} words.")

    print(f"\n[2/2] Converting text to speech...")
    if args.engine == "pyttsx3":
        success = text_to_speech_pyttsx3(text, args.output)
    else:
        success = text_to_speech_gtts(text, args.output)

    if success:
        size_kb = os.path.getsize(args.output) / 1024
        print(f"  Done! Audiobook saved to: {args.output} ({size_kb:.1f} KB)")
        print("\n" + "=" * 50)
        print("Conversion complete! Happy listening.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
