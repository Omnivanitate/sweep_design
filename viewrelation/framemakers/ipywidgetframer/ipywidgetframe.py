from typing import Callable, List, Dict, Any, Union
import ipywidgets as widgets

from viewrelation.commonview.protocols.frameprotocols import FrameMaker, Frame, FigureFrame, CheckTrigger
from viewrelation.commonview.protocols.frameprotocols import DropdownFrame as DropdownProtocol
from viewrelation.commonview.protocols.frameprotocols import CheckBox as CheckBoxProtocol
 
from viewrelation.framemakers.ipywidgetframer.defaults.frame_property import default_categories_properties, default_categories_layout
from viewrelation.framemakers.ipywidgetframer.figwidget.bokehfig import Image

class WidgetFrameMaker(FrameMaker):

    def __init__(self, categories_properties: Dict[str, Dict[str, Any]] = None, 
            categories_layout: List[Union[str, List[str]]] = None) -> None:
        
        if categories_properties is None:
            categories_properties = default_categories_properties

        self.categories_properties = categories_properties

        if categories_layout is None:
            categories_layout = default_categories_layout
        
        self.categories_layout = categories_layout

        
    
    @staticmethod
    def get_output_figure(figure, frame_property: dict) -> 'WidgetFrame':
        window = widgets.HBox([figure])
        window.layout = widgets.Layout(
                border='solid 1px black',
                margins='10px, 10px, 10px, 10px',
                padding='5px, 5px, 5px, 5px'
        )     
        return WidgetFrame(window)
    
    @staticmethod
    def get_output_checkbox(name: str, frame_property) -> 'WidgetFrame':
        label = widgets.HTML(value=f"<b><font color='black'>{name}:</b>")
        output = widgets.VBox([label])
        output.layout = widgets.Layout(
            width='{0}px'.format(frame_property['width']*0.20),
            border='solid 1px black',
            margins='10px, 10px, 10px, 10px',
            padding='5px, 5px, 5px, 5px'
        )
        return WidgetFrame(output)
    
    @staticmethod
    def get_output_dropdown(images: Dict[str, Image], 
                name_no_data: str = 'No Spectrogram!') -> 'DropdownFrame':
        w = widgets.Dropdown(
            options=[name_no_data],
            value=name_no_data,
            description='Spectrograms',
            disabled=False
        )
        return DropdownFrame(w, images, name_no_data)

    @staticmethod
    def get_checkbox(name: str, color: str, group: Any) -> 'CheckBox':
        text = '____ {0}'.format(name)
        w = widgets.Checkbox(
            value=True,
            description=f'<b><font color={color}>{text}</b>',
            disabled=False,
            indent=False
        )
        return CheckBox(w, name, group)

class WidgetFrame:
    
    def __init__(self, output: widgets.Box = None) -> None:
        self.output = output
        
    def h_add(self, other: 'Frame') -> 'WidgetFrame':
        return WidgetFrame(widgets.HBox([self.output, other.output]))
    
    def v_add(self, other: 'Frame') -> 'WidgetFrame':
        return WidgetFrame(widgets.VBox([self.output, other.output]))

    def add_element(self, other) -> 'WidgetFrame':
         self.output.children += (other,)

class FiguraFrame(WidgetFrame, FigureFrame):

    def __init__(self, figure, output: widgets.Output) -> None:
        super().__init__(widgets.Box(output))
        self.figure = figure

class DropdownFrame(WidgetFrame, DropdownProtocol):

    def __init__(self, dropdown: widgets.Dropdown, images: Dict[str, Image], 
                                                    name_no_data: str) -> None:
        super().__init__(widgets.VBox([dropdown]))
        self.name_no_data = name_no_data
        self.dropdown: widgets.Dropdown = dropdown
        self.images: Dict[Any, Image] = images
        self.dropdown.observe(self._change_image(self.images), 'value')

    def add_choise(self, name: str) -> None:
        options = list(self.dropdown.options)
        options.append(name)
        self.dropdown.options = options
    
    def _change_image(self, images: Dict[Any, Image]) -> Callable[[Any], None]:
        def listner(value: Any) -> None:
            if value.new != self.name_no_data:
                images[value.new].set_visible(True)
            
            if value.old != self.name_no_data:
                images[value.old].set_visible(False)
            
            if value.new == self.name_no_data:
                images[value.old].set_visible(False)
        return listner    
    
class CheckBox(CheckBoxProtocol):

    def __init__(self, checkbox: widgets.Checkbox, name: str, group: Any) -> None:
        self.checkbox: widgets.Checkbox = checkbox
        self.name = name
        self.group = group
        self.verifiable_item: Dict[Any, CheckTrigger] = {}
        self.checkbox.observe(bound_elements(self.verifiable_item), "value")

    def add_listener(self, listener: Dict[Any, CheckTrigger]) -> None:
        self.verifiable_item.update(listener)

    def trigger_by_check(self, check: bool) -> None:
        self.checkbox.value = check

def bound_elements(elements: Dict[str, CheckTrigger]) -> Callable[[Any], None]:
    def listner(value: Any) -> None:
        for listner in elements.values():
            listner.trigger_by_check(value.new)
    return listner
