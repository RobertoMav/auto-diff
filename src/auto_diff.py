import time
import numpy as np

from tqdm import tqdm

from src.tensor import Tensor
from src.dataset import Dataset
from src.optimizer import Optimizer
from src.loss import Loss
np.random.seed(42)


class MLP:
    def __init__(self, neurons, activations, weight_initialization):
        self.MLP_DEPTH = len(neurons) - 1
        self.neurons = neurons
        if len(activations) == 1:
            self.activations = [activations[0] for _ in range(self.MLP_DEPTH)]
        elif len(activations) == 2 and self.MLP_DEPTH > 2:
            self.activations = [activations[0] for _ in range(self.MLP_DEPTH)]
            self.activations[-1] = activations[1]
        else:
            self.activations = activations

        if isinstance(weight_initialization, list):
            self.weights = [Tensor(w, requires_grad=True) for w in weight_initialization]
        else:
            self.weights = [
                Tensor(
                    weight_initialization((neurons[i], neurons[i + 1])),
                    requires_grad=True,
                )
                for i in range(self.MLP_DEPTH)
            ]

        self.biases = [
            Tensor(np.zeros((1, neurons[i + 1])), requires_grad=True)
            for i in range(self.MLP_DEPTH)
        ]

    def forward(self, input):
        a = Tensor(input, requires_grad=False)  # Input shape: (batch_size, input_size)
        for i in range(self.MLP_DEPTH):
            W = self.weights[i]  # Shape: (input_size, output_size)
            b = self.biases[i]  # Shape: (1, output_size)
            z = a.matmul(W) + b  # (batch_size, output_size)
            a = self.activations[i](z)
        return a


    def train(self, dataset: Dataset, epochs: int, optimizer: Optimizer, loss_fn: Loss, batch_size: int = 32):
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.metrics = {}
        self.metrics["train_loss"] = []
        self.metrics["val_loss"] = []
        self.metrics["val_acc"] = []
        self.metrics["train_time"] = []

        for epoch in tqdm(range(epochs)):
            batch_loss = 0
            batch_count = 0
            start = time.time()

            for X_batch, y_batch in dataset.create_batches(batch_size, "train"):
                y_batch_tensor = Tensor(y_batch, requires_grad=False)

                pred = self.forward(X_batch)
                loss = loss_fn(y_batch_tensor, pred)
                batch_loss += loss.data
                batch_count += 1

                # Backward pass
                loss.backward()

                # Update parameters
                optimizer.step()

                # Zero gradients
                optimizer.zero_grad()

            self.metrics["train_time"].append(time.time() - start)

            avg_batch_loss = float(batch_loss / batch_count)
            val_acc, val_loss = self.test(*dataset.get_val_data())

            # Metrics
            self.metrics["val_loss"].append(float(val_loss.data))
            self.metrics["val_acc"].append(float(val_acc))
            self.metrics["train_loss"].append(avg_batch_loss)

            print(
                f"Epoch {epoch + 1} Train Loss: {self.metrics['train_loss'][-1]:.4f}, Val Acc: {val_acc:.4f}, Val Loss: {val_loss.data:.4f}"
            )

        return self.metrics


    def test(self, test_data: np.ndarray, test_labels: np.ndarray):
        y_tensor = Tensor(test_labels, requires_grad=False)
        y_hat = self.forward(test_data)
        loss = self.loss_fn(y_tensor, y_hat)

        predictions = np.argmax(y_hat.data, axis=1)
        true_labels = np.argmax(test_labels, axis=1)
        accuracy = np.mean(predictions == true_labels)

        return accuracy, loss