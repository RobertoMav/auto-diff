import torch


def add_numbers(a: int, b: int) -> int:
    """_summary_

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    return a + b


print(add_numbers(1, 2))


x: torch.Tensor = torch.Tensor(1.0)
y: torch.Tensor = torch.Tensor(2.0)

z: torch.Tensor = x + y
print(z)
print(type(z))

print(z.item())
print(type(z.item()))


def function_nice(
    a: int,
    b: int,
    c: int,
) -> int:
    """
    This function is a nice function.
    """
    c = a + b + c
    return c


VALUE = "hi"

VALUE.strip("a").strip("b").strip("c").strip("a").strip("b").strip("c").strip(
    "a"
).strip("a").strip("a").strip("a").strip("a").strip("a").strip("a").strip("a").strip(
    "a"
).strip("a")
