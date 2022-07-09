from typing import Any, Callable
from abc import ABCMeta, abstractmethod


class CommonController(metaclass=ABCMeta):
    @abstractmethod
    def widget_notify(self, sender: Any) -> Callable[[Any], None]:
        pass
