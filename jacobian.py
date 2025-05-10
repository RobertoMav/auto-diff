import numpy as np


def scalar_input(x: int, w: float) -> np.array:
    y: np.array = x * np.ones(17) * w
    return y


print(scalar_input(7, 3.2))

# Ok, so next steps is to:
# 1. Compute the Jacobian of this scalar_input_func
# 2. Compute the derivative
# 3. Understand the Gradient vector of this function
# 4. Get why is the jacobian the trasnposes grad vector

# Jacobian is the matrix of all first order partial derivatives of a vector-valued function.
# It's a matrix of the derivatives of the function with respect to each of its variables.


def derivative_of_scalar_input(x: int, w: float) -> np.array:
    return np.array([w])


print(derivative_of_scalar_input(7, 3.2))
