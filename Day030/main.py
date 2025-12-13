from pathlib import Path

def main():
    day_dir = Path(__file__).parent  # Day030 folder
    file_path = day_dir / "non_existent_file.txt"

    try:
        with file_path.open("r", encoding="utf-8") as f:
            _ = f.read()
    except FileNotFoundError:
        file_path.write_text("This file was created because it did not exist.", encoding="utf-8")

if __name__ == "__main__":
    main()