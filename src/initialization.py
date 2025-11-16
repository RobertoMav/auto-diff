import numpy as np

class Initialization:
    @staticmethod
    def xavier(size):
        input = size[0]
        stddev = np.sqrt(1 / input)
        return np.random.normal(0, stddev, size=size)

    @staticmethod
    def he(size):
        fan_in = size[0]
        stddev = np.sqrt(2 / fan_in)
        return np.random.normal(0, stddev, size=size)

    @staticmethod
    def normal(size):
        return np.random.randn(*size)

    @staticmethod
    def uniform(size):
        return np.random.uniform(size=size)

    @staticmethod
    def zeros(size):
        return np.zeros(size)

    @staticmethod
    def explode(size):
        return 1000000 * np.random.randn(*size)

    @staticmethod
    def vanish(size):
        return np.random.normal(size=size) / 1000000
