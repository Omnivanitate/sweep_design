from email.mime import image
from typing import Protocol, Any, Dict, List, Union

from viewrelation.commonview.protocols.figureprotocols import Figure, Image


class FrameMaker(Protocol):

    categories_properties: Dict[str, Dict[str, Any]]
    categories_layout: List[Union[str, List[str]]]

    @staticmethod
    def get_output_figure(figure: Figure, frame_properties: Dict[str, Any]) -> 'Frame': ...

    @staticmethod
    def get_output_checkbox(checkbox_header: str, frame_properties: Dict[str, Any]) -> 'Frame': ...

    @staticmethod
    def get_output_dropdown(images: Dict[str, Image], no_data_name: str) -> 'DropdownFrame': ...

    @staticmethod
    def get_checkbox(name: str, color: str, group: Any) -> 'CheckBox': ...


class Frame(Protocol):

    output: Any

    def __init__(self, output: Any) -> None:
        self.output = output

    def h_add(self, other: 'Frame') -> 'Frame': ...

    def v_add(Self, other: 'Frame') -> 'Frame': ...

    def add_element(self, other: Any) -> None: ...

class FigureFrame(Frame, Protocol):

    def __init__(self, figure: Figure, output: Any) -> None:
        super().__init__(output)
        self.figure = figure

    def figure(self) -> Figure: ...

class DropdownFrame(Frame, Protocol):

    dropdown: Any
    images: Dict[str, Image]
    
    def __init__(self, dropdown: Any, images: Dict[str, Image]) -> None:
        super().__init__(dropdown)
        self.dropdown = dropdown
        self.images = images
    
    def add_choise(self, choise: str) -> None: ...

class CheckBox(Protocol):

    name: str
    checkbox: Any
    group: Any
    verifiable_item: Dict[str, 'CheckTrigger']
    
    def __init__(self, checkbox: Any, name: str, group: Any) -> None:
        self.checkbox = checkbox
        self.name = name
        self.group = group
        self.verifiable_item = {}

    def add_listener(self, listeners: Dict[Any, 'CheckTrigger']) -> None: ...

    def trigger_by_check(self, check: bool) -> None: ...

class CheckTrigger(Protocol):

    def trigger_by_check(self, check: bool) -> None: ...