import numpy as np
from keras.datasets import mnist
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
import matplotlib.pyplot as plt

from src.auto_diff import (Tensor, Activation, Loss, Initialization, MLP, Dataset, Adam, train, test_whole_set,)
from src.activation import Activation
from src.loss import Loss
from src.initialization import Initialization
from src.auto_diff import MLP
from src.auto_diff import Dataset

print("Loading MNIST dataset...")
(X_train, y_train), (X_test, y_test) = tqdm(mnist.load_data())
print("Loaded MNIST dataset...")

# Normalizando
X_train = X_train.reshape(-1, 784).astype(np.float32) / 255.0  # Flatten images
X_test = X_test.reshape(-1, 784).astype(np.float32) / 255.0  # Flatten images

MNIST_num_classes = 10
MNIST = Dataset(X_train, y_train, X_test, y_test, num_classes=MNIST_num_classes)

# Load and preprocess the Iris dataset
iris = load_iris()
X = iris.data  # Shape: (150, 4)
y = iris.target  # Shape: (150,)

# Normalize the dataset
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

IRIS = Dataset(X_train, y_train, X_test, y_test, num_classes=3)
DATASET = MNIST

# Training the model
EPOCHS = 20
BATCH_SIZE = 32
loss_fn = Loss.CrossEntropy
input_size = next(iter(DATASET.get_train_data()))[0].shape[1]
output_size = DATASET.num_classes
MODEL = MLP(
    [input_size, 256, 128, output_size],
    [Activation.relu, Activation.softmax],
    Initialization.he,
)

parameters = MODEL.weights + MODEL.biases
optim = Adam(3e-4, parameters)
training_metrics = train(MODEL, DATASET, EPOCHS, optim, loss_fn, BATCH_SIZE)

# Testing the model
test_acc, test_loss = test_whole_set(MODEL, *DATASET.get_test_data(), loss_fn)
print(f"Test Accuracy: {test_acc:.4f}, Test Loss: {test_loss.data:.4f}")

def plot_metrics(metrics):
    epochs = range(len(metrics["train_loss"]))

    plt.figure(figsize=(10, 6))
    plt.plot(epochs, metrics["train_loss"], label="Train Loss")
    plt.plot(epochs, metrics["val_loss"], label="Validation Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.grid(True)
    plt.show()


plot_metrics(training_metrics)

# plot time
plt.figure(figsize=(10, 6))
plt.title("Training Time")
plt.xlabel("Epochs")
plt.ylabel("Time (s)")
plt.plot(range(EPOCHS), training_metrics["train_time"])
plt.show()

plt.plot(training_metrics["val_acc"])
plt.show()


def simple_function(x):
    # f(x) = 3x + x^2 == 3*2 + 2^2 = 6 + 4 = 10
    return x * 3 + x**2


# Create a Tensor with requires_grad=True
x = Tensor(2.0, requires_grad=True)  # Let's use x = 2.0 as an example

# Compute the function output
y = simple_function(x)
print(x)
print(y)

# Perform backpropagation to compute the gradient
y.backward()

# 2*2 + 3 = 4 + 3 = 7
# Output the gradient
print(f"Value of f(x): {y.data}")
print(f"Gradient of f(x) w.r.t x: {x.grad}")
print(y._prev)
print(y._op)
z = y * 37 + 2

z.backward()
print(z)
print(x.grad)
A = Tensor([[1.0, 2.0]], requires_grad=True)
B = Tensor([[3.0], [4.0]], requires_grad=True)

C = A @ B

C.backward()
print(f"{A.data=}")
print(f"{B.data=}")
print(f"{C.data=}")
print(f"{A.grad=}")
print(f"{B.grad=}")
print(f"{C.grad=}")