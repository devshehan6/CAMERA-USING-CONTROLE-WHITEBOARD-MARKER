# Camera Whiteboard Controller

A starter project for tracking hand gestures with a webcam and sending board
motion commands to an Arduino-based drawing controller.

## Setup

Use Python 3.10 or newer. Install the dependencies and copy `.env.example` to
`.env`, then set the serial port for your controller.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Upload `firmware/controller/controller.ino` to the board. The firmware expects
two stepper drivers and an optional pen servo; review the pin assignments and
mechanics before connecting hardware.

## Calibration

Edit `config/calibration.json` with the camera pixel coordinates of the four
board corners in top-left, top-right, bottom-right, bottom-left order. The
destination corners are board coordinates in millimeters. Run
`python scripts/calibrate_board.py` to validate the calibration and view the
projected board outline.

## Run

```powershell
python scripts/run.py
```

Raise only the index finger to draw. An open hand moves the pen without
drawing. Press `q` in the camera window to exit. Configure `SERIAL_PORT`,
board dimensions, and step scales in `.env` to match your setup.

## Tests

```powershell
python -m pytest
```

The motion code sends absolute step coordinates as `MOVE x y` and pen state as
`PEN 0` or `PEN 1`, each terminated by a newline. The Arduino replies with
`OK` after accepting a command.