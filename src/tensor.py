import numpy as np

class Tensor:
    def __init__(self, data, requires_grad=True):
        self.data = np.array(data, dtype=np.float64)
        self.requires_grad = requires_grad
        self.grad = None
        self._backward = lambda: None  # Função que calcula o gradiente
        self._prev = set()  # Tensores que são anteriores
        self._op = ""  # Supported operations (+, -, *, /, etc)

    def __repr__(self):
        return f"Tensor(data={self.data}, requires_grad={self.requires_grad}) \
            {self._op=}, {self._prev=}, {self._backward=}, {self.grad=}"

    def backward(self):
        # Topologically sort
        topo_order = []
        visited = set()

        # Building this in the middle of the function to avoid recursion problems
        # Simple topological order
        def build_topo(tensor):
            if tensor not in visited:
                visited.add(tensor)
                for child in tensor._prev:
                    build_topo(child)
                topo_order.append(tensor)

        build_topo(self)

        # Initialize gradient to 0
        for tensor in topo_order:
            tensor.grad = np.zeros_like(tensor.data)
        # Gradient of the output tensor is 1
        self.grad = np.ones_like(self.data)

        # Backpropagation (Reverse order)
        for tensor in reversed(topo_order):
            tensor._backward()

    ## ADDITION
    def __add__(self, other):
        other = (
            # It has to be a tensor
            other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        )
        # Sum of the data
        data = self.data + other.data
        # Output tensor
        out = Tensor(data, requires_grad=(self.requires_grad or other.requires_grad))

        def _backward():
            if self.requires_grad:
                grad_self = out.grad
                while grad_self.ndim > self.data.ndim:
                    grad_self = grad_self.sum(axis=0)

                for axis, size in enumerate(self.data.shape):
                    if size == 1:
                        grad_self = grad_self.sum(axis=axis, keepdims=True)
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

            if other.requires_grad:
                grad_other = out.grad
                while grad_other.ndim > other.data.ndim:
                    grad_other = grad_other.sum(axis=0)
                for axis, size in enumerate(other.data.shape):
                    if size == 1:
                        grad_other = grad_other.sum(axis=axis, keepdims=True)
                other.grad = other.grad + grad_other if other.grad is not None else grad_other

        # This is what will be called when calculating the gradient
        out._backward = _backward
        out._prev = {self, other}
        out._op = "+"
        return out

    def __radd__(self, other):
        return self + other

    ## SUBTRACTION
    def __sub__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        data = self.data - other.data
        out = Tensor(data, requires_grad=(self.requires_grad or other.requires_grad))

        def _backward():
            if self.requires_grad:
                grad_self = out.grad
                while grad_self.ndim > self.data.ndim:
                    grad_self = grad_self.sum(axis=0)
                for axis, size in enumerate(self.data.shape):
                    if size == 1:
                        grad_self = grad_self.sum(axis=axis, keepdims=True)
                self.grad = self.grad + grad_self if self.grad is not None else grad_self
            if other.requires_grad:
                grad_other = -out.grad
                while grad_other.ndim > other.data.ndim:
                    grad_other = grad_other.sum(axis=0)
                for axis, size in enumerate(other.data.shape):
                    if size == 1:
                        grad_other = grad_other.sum(axis=axis, keepdims=True)
                other.grad = other.grad + grad_other if other.grad is not None else grad_other

        out._backward = _backward
        out._prev = {self, other}
        out._op = "-"
        return out

    def __rsub__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        return other - self

    # MULTIPLICATION
    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        data = self.data * other.data
        out = Tensor(data, requires_grad=(self.requires_grad or other.requires_grad))

        def _backward():
            if self.requires_grad:
                grad_self = other.data * out.grad
                while grad_self.ndim > self.data.ndim:
                    grad_self = grad_self.sum(axis=0)
                for axis, size in enumerate(self.data.shape):
                    if size == 1:
                        grad_self = grad_self.sum(axis=axis, keepdims=True)
                self.grad = self.grad + grad_self if self.grad is not None else grad_self
            if other.requires_grad:
                grad_other = self.data * out.grad
                while grad_other.ndim > other.data.ndim:
                    grad_other = grad_other.sum(axis=0)
                for axis, size in enumerate(other.data.shape):
                    if size == 1:
                        grad_other = grad_other.sum(axis=axis, keepdims=True)
                other.grad = other.grad + grad_other if other.grad is not None else grad_other

        out._backward = _backward
        out._prev = {self, other}
        out._op = "*"
        return out

    def __rmul__(self, other):
        return self * other

    # DIVISION
    def __truediv__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        data = self.data / other.data
        out = Tensor(data, requires_grad=(self.requires_grad or other.requires_grad))

        def _backward():
            if self.requires_grad:
                grad_self = (1 / other.data) * out.grad
                while grad_self.ndim > self.data.ndim:
                    grad_self = grad_self.sum(axis=0)
                for axis, size in enumerate(self.data.shape):
                    if size == 1:
                        grad_self = grad_self.sum(axis=axis, keepdims=True)
                self.grad = self.grad + grad_self if self.grad is not None else grad_self
            if other.requires_grad:
                grad_other = (-self.data / (other.data**2)) * out.grad
                while grad_other.ndim > other.data.ndim:
                    grad_other = grad_other.sum(axis=0)
                for axis, size in enumerate(other.data.shape):
                    if size == 1:
                        grad_other = grad_other.sum(axis=axis, keepdims=True)
                other.grad = other.grad + grad_other if other.grad is not None else grad_other

        out._backward = _backward
        out._prev = {self, other}
        out._op = "/"
        return out

    def __rtruediv__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        return other / self

    # NEGATION
    def __neg__(self):
        data = -self.data
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_self = -out.grad
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "neg"
        return out

    # POWER
    def __pow__(self, exponent):
        data = self.data**exponent
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_self = exponent * (self.data ** (exponent - 1)) * out.grad
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "**"
        return out

    # MULTIPLICATION OF MATRICES
    def matmul(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        data = self.data @ other.data
        out = Tensor(data, requires_grad=(self.requires_grad or other.requires_grad))

        def _backward():
            if self.requires_grad:
                grad_self = out.grad @ other.data.T
                self.grad = self.grad + grad_self if self.grad is not None else grad_self
            if other.requires_grad:
                grad_other = self.data.T @ out.grad
                other.grad = other.grad + grad_other if other.grad is not None else grad_other

        out._backward = _backward
        out._prev = {self, other}
        out._op = "matmul"
        return out

    def __matmul__(self, other):
        return self.matmul(other)

    def __rmatmul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        return other.matmul(self)

    # ACTIVATION FUNCTIONS
    def relu(self):
        data = np.maximum(0, self.data)
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_self = out.grad.copy()
                grad_self[self.data <= 0] = 0
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "relu"
        return out

    def sigmoid(self):
        data = 1 / (1 + np.exp(-self.data))
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_self = data * (1 - data) * out.grad
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "sigmoid"
        return out

    def tanh(self):
        data = np.tanh(self.data)
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_self = (1 - data**2) * out.grad
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "tanh"
        return out

    def softmax(self):
        exps = np.exp(self.data - np.max(self.data, axis=1, keepdims=True))
        data = exps / np.sum(exps, axis=1, keepdims=True)
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_output = out.grad  # Shape: (batch_size, num_classes)
                s = out.data  # Softmax output, shape: (batch_size, num_classes)
                grad_input = s * (grad_output - (grad_output * s).sum(axis=1, keepdims=True))
                self.grad = self.grad + grad_input if self.grad is not None else grad_input

        out._backward = _backward
        out._prev = {self}
        out._op = "softmax"
        return out

    def log(self):
        data = np.log(self.data)
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_self = (1 / self.data) * out.grad
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "log"
        return out

    def sum(self, axis=None, keepdims=False):
        data = np.sum(self.data, axis=axis, keepdims=keepdims)
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_self = out.grad
                if axis is not None and not keepdims:
                    grad_self = np.expand_dims(grad_self, axis=axis)
                grad_self = np.broadcast_to(grad_self, self.data.shape)
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "sum"
        return out

    def mean(self, axis=None, keepdims=False):
        data = np.mean(self.data, axis=axis, keepdims=keepdims)
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad_self = out.grad / np.prod(self.data.shape)
                if axis is not None and not keepdims:
                    grad_self = np.expand_dims(grad_self, axis=axis)
                grad_self = np.broadcast_to(grad_self, self.data.shape)
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "mean"
        return out

    def clip(self, min_value, max_value):
        data = np.clip(self.data, min_value, max_value)
        out = Tensor(data, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                grad = out.grad
                mask = (self.data >= min_value) & (self.data <= max_value)
                grad_self = grad * mask.astype(np.float64)
                self.grad = self.grad + grad_self if self.grad is not None else grad_self

        out._backward = _backward
        out._prev = {self}
        out._op = "clip"
        return out
