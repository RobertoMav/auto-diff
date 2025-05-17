from typing import TypedDict


class Learning(TypedDict):
    focus: int
    crazy: float


learner = Learning(focus=7)
print(learner)