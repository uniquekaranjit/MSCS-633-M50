# QR Code Generator (Python)
This application generates a QR code image from a URL you enter (CLI).



## Requirements
- Python 3.8+
- `qrcode[pil]` (installs Pillow automatically)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage (CLI)
```bash
python qr_generator.py --url "https://example.com" --out "qr_output.png"
```
 
Note: the generated QR image will be saved in the same directory as this project with the filename `qr_output.png`.
