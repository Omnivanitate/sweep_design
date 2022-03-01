from typing import Protocol, Any, Dict

import numpy as np


class Figure(Protocol):

    def __init__(self, figure: Any) -> None:
        self._figure = figure

    @property
    def _figure(self) -> Any: ...

    def get_figure(self): ...

    def plot_line(self, x: Any, y: Any, line_property: dict) -> 'Line': ...

    def plot_image(self, x: Any, y: Any, S: Any, image_property: dict) -> 'Image': ...

class Line(Protocol):
    
    def __init__(self, line: Any) -> None:
        self._line = line
    
    def _line(self) -> Any: ...

    def set_visible(self, is_visible: bool) -> None: ...

    def trigger_by_check(self, check: bool) -> None: ...

class Image(Protocol):
    
    def __init__(self, image: Any) -> None:
        self._image = image

    @property
    def _image(self) -> Any: ...

    def set_visible(self, is_visible: bool) -> None: ...


class Frame(Protocol):

    def __init__(self, output: Any) -> None:
        self.output = output

    @property
    def output(self) -> Any: ...

    def h_add(self, other: 'Frame') -> 'Frame': ...

    def v_add(Self, other: 'Frame') -> 'Frame': ...

    def add_element(self, other: Any) -> None: ...

class FigureFrame(Frame, Protocol):

    def __init__(self, figure: Figure, output: Any) -> None:
        super().__init__(output)
        self.figure = figure

    def figure(self) -> Figure: ...

class DropdownFrame(Frame, Protocol):

    def __init__(self, dropdown: Any) -> None:
        super().__init__(dropdown)
        self.dropdown = dropdown

    @property
    def dropdown(self) -> Any: ...
    
    def add_choise(self) -> None: ...

    def add_images_to_observe(self, images: Dict['str': Image]) -> None: ...

class CheckBox(Protocol):
    
    def __init__(self, checkbox: Any) -> None: ...

    def add_lisners(self, listeners: Dict) -> None: ...

    def trigger_by_check(self, check: bool) -> None: ...