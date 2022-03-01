from typing import Protocol, Any, Dict

class FigureMaker(Protocol):
    
    @staticmethod
    def get_figure(figure_properties: Dict[str, Any]) -> 'Figure': ...

    def get_next_line_properties(self) -> Dict[str, Any]: ...

    def get_image_properties(self) -> Dict[str, Any]: ...


class Figure(Protocol):

    figure: Any

    def __init__(self, figure: Any) -> None:
        self.figure = figure

    def get_figure(self): ...

    def plot_line(self, x: Any, y: Any, line_property: Dict[str, Any], 
                            group: Any, name: str) -> 'Line': ...

    def plot_image(self, x: Any, y: Any, S: Any, image_property: Dict[str, Any]) -> 'Image': ...

class Line(Protocol):
    
    line: Any
    name: str
    group: Any
    unique: Any
    
    def __init__(self, line: Any, name: str, group: Any, unique: Any) -> None:
        self.name = name
        self.group = group
        self.unique = unique
        self.line = line
    
    def get_color(self) -> str: ...

    def set_visible(self, is_visible: bool) -> None: ...

    def trigger_by_check(self, check: bool) -> None: ...

class Image(Protocol):

    image: Any

    def __init__(self, image: Any) -> None:
        self.image = image

    def set_visible(self, is_visible: bool) -> None: ...