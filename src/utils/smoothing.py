"""Exponential smoothing for noisy tracked coordinates."""


class ExponentialSmoother:
    def __init__(self, alpha: float = 0.35):
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be in the interval (0, 1]")
        self.alpha = alpha
        self._value = None

    def update(self, value: tuple[float, float]) -> tuple[float, float]:
        if self._value is None:
            self._value = value
        else:
            self._value = tuple(
                self.alpha * current + (1 - self.alpha) * previous
                for current, previous in zip(value, self._value)
            )
        return self._value

    def reset(self) -> None:
        self._value = None