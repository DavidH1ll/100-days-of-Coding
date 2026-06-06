# Day 90 - Convert PDF to Audiobook

## Overview
Command-line tool that extracts text from a PDF and converts it to speech, saving the result as an MP3 file. Supports multiple text extraction engines (PyPDF2, pdfplumber) and TTS engines (gTTS, pyttsx3).

## Features
- Extract text from any PDF
- Convert to MP3 audio using Google TTS or offline pyttsx3
- Progress feedback during extraction
- Configurable extraction engine and TTS engine
- Automatic output filename from input

## Usage
```bash
python pdf_to_audiobook.py document.pdf
python pdf_to_audiobook.py document.pdf -o output.mp3 --engine pyttsx3
```

## Key Concepts
- argparse for CLI interface
- PyPDF2 / pdfplumber for PDF text extraction
- gTTS (Google Text-to-Speech) / pyttsx3 for audio synthesis
- Graceful import error handling for optional dependencies

## Reflection
PyPDF2 handles most PDFs well but struggles with scanned/image-based PDFs (those need OCR). gTTS requires internet access while pyttsx3 works offline. The dual-engine architecture lets users choose based on their constraints.

**Day 90 Complete!** ✅
