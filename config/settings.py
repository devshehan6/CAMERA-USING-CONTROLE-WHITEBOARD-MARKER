"""Environment-backed runtime settings."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    camera_index: int = int(os.getenv("CAMERA_INDEX", "0"))
    serial_port: str = os.getenv("SERIAL_PORT", "COM3")
    baud_rate: int = int(os.getenv("BAUD_RATE", "115200"))
    board_width_mm: float = float(os.getenv("BOARD_WIDTH_MM", "300"))
    board_height_mm: float = float(os.getenv("BOARD_HEIGHT_MM", "200"))
    steps_per_mm_x: float = float(os.getenv("STEPS_PER_MM_X", "10"))
    steps_per_mm_y: float = float(os.getenv("STEPS_PER_MM_Y", "10"))
    calibration_path: Path = PROJECT_ROOT / "config" / "calibration.json"


settings = Settings()