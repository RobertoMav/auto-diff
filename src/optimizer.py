import numpy as np

class Optimizer:
    def __init__(self, learning_rate, parameters):
        self.learning_rate = learning_rate
        self.parameters = parameters

    def zero_grad(self):
        for param in self.parameters:
            param.grad = None


class SGD(Optimizer):
    def __init__(self, learning_rate, parameters):
        super().__init__(learning_rate, parameters)

    def step(self):
        for param in self.parameters:
            if param.grad is not None:
                param.data -= self.learning_rate * param.grad
        self.zero_grad()


class Adam(Optimizer):
    def __init__(self, learning_rate, parameters, beta1=0.9, beta2=0.999, epsilon=1e-8):
        super().__init__(learning_rate, parameters)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = [np.zeros_like(p.data) for p in self.parameters]
        self.v = [np.zeros_like(p.data) for p in self.parameters]
        self.t = 0

    def step(self):
        self.t += 1
        for i, param in enumerate(self.parameters):
            grad = param.grad
            if grad is None:
                continue
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grad
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (grad**2)
            m_hat = self.m[i] / (1 - self.beta1**self.t)
            v_hat = self.v[i] / (1 - self.beta2**self.t)
            param.data -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
        self.zero_grad()
