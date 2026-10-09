"""Newline-delimited serial protocol for the Arduino controller."""

import serial


class SerialBridge:
    def __init__(self, port: str, baud_rate: int = 115200, timeout: float = 1.0):
        self._connection = serial.Serial(port, baud_rate, timeout=timeout)

    def move_to_steps(self, x_steps: int, y_steps: int) -> None:
        self._send(f"MOVE {x_steps} {y_steps}")

    def set_pen(self, down: bool) -> None:
        self._send(f"PEN {1 if down else 0}")

    def _send(self, command: str) -> None:
        self._connection.write(f"{command}\n".encode("ascii"))

    def close(self) -> None:
        self._connection.close()