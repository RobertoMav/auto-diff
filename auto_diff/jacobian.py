import numpy as np


def scalar_input(x: int, w: float) -> np.ndarray:
    y: np.ndarray = x * np.ones(17) * w
    return y


# TODO: Implement this
print(scalar_input(7, 3.2))
