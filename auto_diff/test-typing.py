from typing import TypedDict, TypeVar


class Person(TypedDict):
    name: str
    age: int


print(Person(name="John", age=30))


J = TypeVar("J")


def foo(x: J) -> J:
    return x


print(foo(1))
print(foo("hello"))


def foo2[T](x: T) -> T:
    """
    Takes an argument of any type 'T'
    and returns a value of the same type 'T'.
    The '[T]' declares the type variable.
    """
    return x


print(foo2(1))
print(foo2("hello"))


class Learning(TypedDict):
    focus: int
    crazy: float


learner = Learning(focus=7, crazy=3.2)
print(learner)
