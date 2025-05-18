var: int = 1
from typing import Any, Dict, List, Tuple

var = "hello"


class MyClass:
    def __init__(self, var: int, var2: int, var3: int):
        self.var = var
        self.var2 = var2
        self.var3 = var3


def my_function(var: int, var2: int, var3: Any) -> int:
    return var + var2 + var3


List[int] = [1, 2, 3]

Dict[str, int] = {"a": 1, "b": 2, "c": 3}

Tuple[int, str, bool] = (1, "hello", True)

type: MyType = int

my_function()


def my_function(var: MyType) -> MyType:
    return var


print(
    my_function(1),
    my_function("hello")
    + "Thisdfkldnfslkfnsldkfnsdc,vclkfbndslkfsbndfjkdzbfzksj.dfb.sdk",
)
