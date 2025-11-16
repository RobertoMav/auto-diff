# Auto-Diff: Automatic Differentiation & MLP from Scratch

A minimalist implementation of automatic differentiation and a Multi-Layer Perceptron (MLP) built entirely from scratch in Python using only NumPy. This project demonstrates the fundamentals of how modern deep learning frameworks like PyTorch and TensorFlow compute gradients under the hood.

## 🎯 Project Goal

Build a complete automatic differentiation engine and train a neural network **without using any deep learning frameworks**. Everything from gradient computation to backpropagation to optimization is implemented by hand.

## 🧠 What is Automatic Differentiation?

Automatic differentiation (autodiff) is a technique for computing derivatives of functions specified by computer programs. Unlike symbolic differentiation (which manipulates mathematical expressions) or numerical differentiation (which uses finite differences), autodiff achieves machine precision derivatives efficiently.

This implementation uses **reverse-mode automatic differentiation** (backpropagation):
1. Build a computational graph during the forward pass
2. Traverse the graph backwards, applying the chain rule to compute gradients

## 📁 Project Structure

```
auto-diff/
├── src/
│   ├── tensor.py           # Core Tensor class with autodiff engine
│   ├── auto_diff.py        # MLP implementation
│   ├── activation.py       # Activation functions (ReLU, Sigmoid, Tanh, Softmax)
│   ├── loss.py             # Loss functions (MSE, CrossEntropy)
│   ├── optimizer.py        # Optimizers (SGD, Adam)
│   ├── initialization.py   # Weight initialization methods (Xavier, He, etc.)
│   └── dataset.py          # Dataset handling and batching
├── test/
│   └── auto-diff.py        # Example usage on MNIST and Iris datasets
└── README.md
```

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.13+ required
uv sync  # Install dependencies
```

### Quick Example: Simple Gradient Computation

```python
from src.tensor import Tensor

# Define a simple function: f(x) = 3x + x²
def simple_function(x):
    return x * 3 + x**2

# Create tensor with gradient tracking
x = Tensor(2.0, requires_grad=True)

# Forward pass
y = simple_function(x)
print(f"f(2) = {y.data}")  # Output: 10.0

# Backward pass: compute df/dx = 3 + 2x = 7
y.backward()
print(f"df/dx = {x.grad}")  # Output: 7.0
```

### Training an MLP on MNIST

```python
from src.auto_diff import MLP
from src.dataset import Dataset
from src.optimizer import Adam
from src.loss import Loss
from src.activation import Activation
from src.initialization import Initialization
from keras.datasets import mnist

# Load data
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(-1, 784).astype(np.float32) / 255.0
X_test = X_test.reshape(-1, 784).astype(np.float32) / 255.0

# Create dataset
dataset = Dataset(X_train, y_train, X_test, y_test, num_classes=10)

# Build MLP: 784 -> 256 -> 128 -> 10
model = MLP(
    neurons=[784, 256, 128, 10],
    activations=[Activation.relu, Activation.softmax],
    weight_initialization=Initialization.he
)

# Setup optimizer and loss
parameters = model.weights + model.biases
optimizer = Adam(learning_rate=3e-4, parameters=parameters)

# Train
metrics = model.train(
    dataset=dataset,
    epochs=20,
    optimizer=optimizer,
    loss_fn=Loss.CrossEntropy,
    batch_size=32
)

# Test
test_acc, test_loss = model.test(*dataset.get_test_data())
print(f"Test Accuracy: {test_acc:.4f}")
```

### Run the Full Example

```bash
uv run test/auto-diff.py
```

This trains an MLP on the MNIST dataset and plots training metrics.

## 🔧 Key Components

### 1. Tensor (`src/tensor.py`)

The core class that wraps NumPy arrays and tracks computational graphs for automatic differentiation.

**Supported Operations:**
- Arithmetic: `+`, `-`, `*`, `/`, `**`, `@` (matmul)
- Activations: `relu()`, `sigmoid()`, `tanh()`, `softmax()`
- Reductions: `sum()`, `mean()`
- Utilities: `log()`, `clip()`

**Key Features:**
- Builds computational graph automatically
- Topological sorting for correct gradient flow
- Broadcasting support for operations
- Memory-efficient gradient accumulation

### 2. MLP (`src/auto_diff.py`)

A flexible Multi-Layer Perceptron implementation.

**Features:**
- Arbitrary depth and width
- Configurable activation functions per layer
- Built-in training loop with batch processing
- Automatic metrics tracking (train loss, val loss, val accuracy)

### 3. Optimizers (`src/optimizer.py`)

- **SGD**: Stochastic Gradient Descent
- **Adam**: Adaptive Moment Estimation with momentum and RMSprop

### 4. Loss Functions (`src/loss.py`)

- **MSE**: Mean Squared Error (for regression)
- **CrossEntropy**: Cross-Entropy Loss (for classification)

### 5. Weight Initialization (`src/initialization.py`)

- **Xavier**: For sigmoid/tanh activations
- **He**: For ReLU activations
- **Normal, Uniform, Zeros**
- **Explode/Vanish**: For demonstrating gradient problems

## 📊 How It Works

### Forward Pass

```python
# Example: y = (x * 3) + x²
x = Tensor(2.0, requires_grad=True)
y1 = x * 3          # Creates computational node
y2 = x ** 2         # Creates computational node
y = y1 + y2         # Creates final node
```

This builds a graph:
```
    x (2.0)
   / \
  *   **
  |    |
  3    2
   \  /
    +
    |
    y
```

### Backward Pass

```python
y.backward()  # Traverses graph in reverse, applies chain rule
```

1. **Topological Sort**: Orders nodes for correct gradient flow
2. **Initialize Gradients**: Sets output gradient to 1.0
3. **Backpropagate**: Each node computes gradients for its inputs using the chain rule

## 🎓 Educational Value

This project demonstrates:

1. **Computational Graphs**: How operations create nodes and edges
2. **Chain Rule**: How gradients flow backwards through operations
3. **Backpropagation**: The algorithm that makes neural networks trainable
4. **Matrix Calculus**: Gradient computation for matrix operations
5. **Optimization**: How gradient descent updates parameters

## 🧪 Testing

The test file (`test/auto-diff.py`) includes:
- Simple gradient checks
- Matrix multiplication gradients
- Full MLP training on MNIST and Iris datasets
- Visualization of training metrics

## 📝 Implementation Notes

- **Broadcasting**: Properly handles NumPy broadcasting in gradient computation
- **Gradient Accumulation**: Supports multiple backward passes (e.g., in loops)
- **Numerical Stability**: Uses epsilon clipping in log operations and softmax
- **Efficiency**: Leverages NumPy's vectorization for performance

## 🔍 Limitations

This is an educational implementation, not production-ready:
- No GPU support (CPU-only NumPy)
- Limited operation set compared to PyTorch/TensorFlow
- No automatic memory management or optimization
- No static graph compilation

## 🤝 Contributing

This is a learning project. Feel free to fork and experiment!

## 📚 References

- [Automatic Differentiation in Machine Learning: a Survey](https://arxiv.org/abs/1502.05767)
- [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)
- [Micrograd by Andrej Karpathy](https://github.com/karpathy/micrograd)

---

Built with ❤️ to understand the magic behind modern deep learning frameworks.

