import numpy as np

class Dataset:
    def __init__(
        self,
        train_set,
        train_labels,
        test_set,
        test_labels,
        val_split=0.15,
    ):
        self.train_set = train_set
        self.test_set = test_set
        self.num_classes = train_labels.shape[1]

        # One-hot encode the labels
        self.train_labels = self.one_hot_encode(train_labels)
        self.test_labels = self.one_hot_encode(test_labels)

        # Create validation set
        val_size = int(len(train_set) * val_split)
        self.val_set = train_set[-val_size:]
        self.val_labels = self.train_labels[-val_size:]
        self.train_set = train_set[:-val_size]
        self.train_labels = self.train_labels[:-val_size]

    def one_hot_encode(self, labels):
        # Ensure labels is a 1D array
        labels = np.array(labels).ravel()
        # Check if labels are in the correct range
        if np.min(labels) < 0 or np.max(labels) >= self.num_classes:
            raise ValueError(f"Labels must be in the range 0 to {self.num_classes - 1}")
        # One-hot encode labels
        one_hot = np.zeros((labels.size, self.num_classes))
        one_hot[np.arange(labels.size), labels] = 1
        return one_hot

    def create_batches(self, batch_size, dataset="train"):
        if dataset == "train":
            data, labels = self.train_set, self.train_labels
        elif dataset == "val":
            data, labels = self.val_set, self.val_labels
        elif dataset == "test":
            data, labels = self.test_set, self.test_labels
        else:
            raise ValueError("dataset must be 'train', 'val', or 'test'")

        indices = np.arange(len(data))
        np.random.shuffle(indices)
        for start_idx in range(0, len(data), batch_size):
            batch_indices = indices[start_idx : start_idx + batch_size]
            yield data[batch_indices], labels[batch_indices]

    def get_train_data(self):
        yield next(iter(self.create_batches(len(self.train_set), "train")))

    def get_test_data(self):
        return self.test_set, self.test_labels

    def get_val_data(self):
        return self.val_set, self.val_labels
