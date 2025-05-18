from typing import TypedDict


class Learning(TypedDict):
    focus: int
    crazy: float


learner = Learning(focus=7, crazy=3.2)
print(learner)


def add_testing(hook: Hook) -> None:
    pass



