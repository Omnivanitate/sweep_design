import numpy as np
from abc import ABCMeta, abstractmethod, abstractstaticmethod
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Set,
    Union,
    TypeVar,
    Generic,
)

Figure = TypeVar("Figure")
Line = TypeVar("Line")
Image = TypeVar("Image")


class CommonFigureMaker(metaclass=ABCMeta):
    @abstractstaticmethod
    def get_figure(figure_properties: Dict[str, Any]) -> "CommonFigure":
        pass

    @abstractmethod
    def get_next_line_properties(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_next_image_properties(self) -> Dict[str, Any]:
        pass


class CommonFigure(Generic[Figure], metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, figure: Figure) -> None:
        self._figure = figure
        self._lines: Dict[str, CommonLine] = {}
        self._images: Dict[str, CommonImage] = {}

    @abstractmethod
    def add_extra_axis(self, axis_name: str, axis_titel: str, location: str) -> None:
        pass

    @abstractmethod
    def add_line(
        self,
        x: np.ndarray,
        y: np.ndarray,
        unique_name: str,
        groups: Union[str, Set[str]],
        line_properties: Dict[str, Any],
    ) -> "CommonLine":
        pass

    @abstractmethod
    def add_image(
        self,
        x: np.ndarray,
        y: np.ndarray,
        s_xy: np.ndarray,
        unique_name: str,
        groups: Set[str],
        image_properties: Dict[str, Any],
    ) -> None:
        pass

    @abstractmethod
    def add_infty_line(
        self,
        k: float,
        axis: Literal["x", "y"],
        unique_name: str,
        groups: Set[str],
        line_properties: Dict[str, Any],
    ) -> None:
        pass

    def get_figure(self) -> Figure:
        return self._figure

    def get_line(self, unique_name) -> Optional["CommonLine"]:
        return self._lines.get(unique_name, None)

    def get_image(self, unique_name) -> Optional["CommonImage"]:
        return self._images.get(unique_name, None)

    def get_lines_by_groups(self, groups: Union[str, Set[str]]) -> List["CommonLine"]:
        if isinstance(groups, str):
            groups = set([groups])
        return [
            line for line in self._lines.values() if groups.issubset(line.get_groups())
        ]

    def get_images_by_groups(self, groups: Union[str, Set[str]]) -> List["CommonImage"]:
        if isinstance(groups, str):
            groups = set([groups])
        return [
            image
            for image in self._images.values()
            if groups.issubset(image.get_groups())
        ]


class CommonGraphElement(metaclass=ABCMeta):
    def __init__(self, name: str, groups: Union[str, Set[str]]) -> None:
        self._name = name
        if isinstance(groups, str):
            groups = set([groups])
        self._groups = groups

    def set_groups(self, groups: Union[str, Iterable[str]]) -> None:
        if isinstance(groups, str):
            groups = set([groups])
        self._groups.update(groups)

    def get_groups(self) -> Set[str]:
        return self._groups

    def get_name(self) -> str:
        return self._name

    def remove_groups(self, groups: Union[str, Iterable[str]]) -> None:
        if isinstance(groups, str):
            groups = set([groups])
        for group in groups:
            self._groups.discard(group)

    @abstractmethod
    def set_visible(self, is_visible: bool) -> None:
        pass


class CommonLine(CommonGraphElement, Generic[Line]):
    def __init__(self, line: Line, name: str, groups: Union[str, Set[str]]) -> None:
        self._line = line
        super().__init__(name, groups)

    @abstractmethod
    def get_color(self) -> Any:
        pass


class CommonImage(CommonGraphElement, Generic[Image]):
    def __init__(self, image: Image, name: str, groups: Union[str, Set[str]]) -> None:
        self._image = image
        super().__init__(name, groups)
