
class Activation:
    @staticmethod
    def relu(z):
        return z.relu()

    @staticmethod
    def sigmoid(z):
        return z.sigmoid()

    @staticmethod
    def tanh(z):
        return z.tanh()

    @staticmethod
    def softmax(z):
        return z.softmax()
