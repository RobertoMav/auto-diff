class Loss:
    @staticmethod
    def MSE(y, y_hat):
        diff = y_hat - y
        return (diff * diff).mean()

    @staticmethod
    def CrossEntropy(y, y_hat):
        epsilon = 1e-15
        y_hat_clipped = y_hat.clip(epsilon, 1 - epsilon)
        loss = -(y * y_hat_clipped.log()).sum(axis=1).mean()
        return loss
