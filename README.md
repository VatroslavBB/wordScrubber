# wordScrubber

wordScrubber is a lightweight desktop utility that lets you:

1. Press a global hotkey.
2. Drag over an area of your screen.
3. Automatically detect text in that region.
4. Remove the detected text using inpainting.
5. Save the cleaned result as a new image.

## Features

- Global shortcut: `Ctrl+Shift+J`
- Full-screen transparent selection overlay
- Text detection with OpenCV Differentiable Binarization with ResNet-50 backbone (`models/DB50.onnx`)
- Text removal via OpenCV inpainting (`INPAINT_NS`)
- Output image saved to desktop folder with timestamped filename

## Project Structure

- `app.py`: App entry point, hotkey listener, screenshot capture flow
- `widget.py`: Full-screen selection UI (drag to select area)
- `textRemoval.py`: Text detection and inpainting logic
- `models/DB50.onnx`: OCR text detection model
- `app.spec`: PyInstaller build configuration

## Notes and Limitations

- The temporary screenshot name is fixed internally (`screenshotQ121.png`) before processing.
- Very small selections are ignored.
- Detection quality depends on image quality, font size, and contrast.
- Inpainting can blur backgrounds where text is removed.
