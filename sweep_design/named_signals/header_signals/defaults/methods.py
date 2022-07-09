from typing import Union, Callable, Optional

from ..base_header import HeaderBase

Num = Union[float, int, complex]
InName = Union[HeaderBase, str, Callable[[], str]]


def make_name(name: Optional[InName], func: Callable[..., str], *args) -> InName:

    if name is not None:
        return name

    def call() -> str:
        return func(*args)

    return call


def make_category(
    named_relation: HeaderBase,
    category: Optional[str],
    getter_func: Callable[[str], str] = None,
) -> str:

    if category is None:
        if getter_func is None:
            return named_relation.category
        else:
            return getter_func(named_relation.category)
    return category
