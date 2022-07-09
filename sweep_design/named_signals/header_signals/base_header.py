from typing import Callable, Union, Optional
from abc import ABCMeta, abstractmethod


InName = Union["HeaderBase", str, Callable[..., str]]


class HeaderBase(metaclass=ABCMeta):
    def __init__(self, name: InName, category: str) -> None:

        if callable(name):
            self._name = name
            self._category = category
        elif isinstance(name, HeaderBase):
            self._name = name._name
            self._category = name._category
        else:
            r_name = str(name)

            def call() -> str:
                return r_name

            self._name = call
            self._category = category

    @property
    @abstractmethod
    def category(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> Callable[..., str]:
        pass
