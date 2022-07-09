from __future__ import annotations

from typing import Any, Dict, Set, Union

import ipywidgets as widgets

from ...base_view.abc_common_framer_grapher.controller import CommonController
from ...base_view.abc_common_framer_grapher.frame import (
    CommonCheckBox,
    CommonCheckBoxFrame,
    CommonController,
    CommonDropdownFrame,
    CommonFigureFrame,
    CommonFrame,
    CommonFrameMaker,
)


class WidgetFrameMaker(CommonFrameMaker):
    @staticmethod
    def get_figure_frame(figure, frame_properties: Dict[str, Any]) -> "FigureFrame":

        window = widgets.HBox([figure])
        window.layout = widgets.Layout(**frame_properties)
        return FigureFrame(figure, window)

    @staticmethod
    def get_checkbox_frame(
        frame_properties: Dict[str, Any], controller: CommonController
    ) -> "CheckBoxFrame":

        header_label = frame_properties["description"]
        label = widgets.HTML(value=f"<b><font color='black'>{header_label}:</b>")
        output = widgets.VBox([label])
        output.layout = widgets.Layout(**frame_properties)
        return CheckBoxFrame(output, controller)

    @staticmethod
    def get_dropdown_frame(
        dropdown_frame_properties: Dict[str, Any], controller: CommonController
    ) -> "DropdownFrame":
        w = widgets.Dropdown(
            options=[dropdown_frame_properties["name_no_data"]],
            value=dropdown_frame_properties["name_no_data"],
            description=dropdown_frame_properties["description"],
            disabled=False,
        )
        w.layout = widgets.Layout(**dropdown_frame_properties)
        return DropdownFrame(w, dropdown_frame_properties["name_no_data"], controller)


class WidgetFrame(CommonFrame[widgets.Box, CommonController]):
    def h_add(self, other: "WidgetFrame") -> "WidgetFrame":
        if not (self._output is None or other._output is None):
            return WidgetFrame(widgets.HBox([self._output, other._output]))
        elif self._output is None:
            return other
        else:
            return self

    def v_add(self, other: "WidgetFrame") -> "WidgetFrame":
        if not (self._output is None or other._output is None):
            return WidgetFrame(widgets.VBox([self._output, other._output]))
        elif self._output is None:
            return other
        else:
            return self

    def add_outputs(self, other: Any) -> None:
        self._output.children += (other,)

    def remove_outputs(self, other: Any) -> None:
        list_outputs = list(self._output.children)
        list_outputs.pop(list_outputs.index(other))
        self._output.children = tuple(list_outputs)


class FigureFrame(WidgetFrame, CommonFigureFrame):
    pass


class CheckBoxFrame(WidgetFrame, CommonCheckBoxFrame["CheckBox"]):
    def add_choise(
        self,
        choise: str,
        groups: str,
        checkbox_properties: Dict[str, Any],
        controller: CommonController,
    ) -> None:

        text = "____ {0}".format(choise)
        checkbox = widgets.Checkbox(
            value=True,
            description=f'<b><font color={checkbox_properties["color"]}>{text}</b>',
            disabled=False,
            indent=False,
        )
        choise_box = CheckBox(checkbox, choise, groups, controller)
        self.add_outputs(choise_box._output)
        self._checkboxs.update({choise: choise_box})

    def return_choise(self, choise: str) -> None:
        self._checkboxs[choise]._checkbox.value = True
        self.add_outputs(self._checkboxs[choise]._output)

    def remove_choise(self, choise: str) -> None:
        self._checkboxs[choise]._checkbox.value = False
        self.remove_outputs(self._checkboxs[choise]._output)


class DropdownFrame(WidgetFrame, CommonDropdownFrame[widgets.Dropdown]):
    def __init__(
        self,
        dropdown: widgets.Dropdown,
        no_data_name: str,
        controller: CommonController,
    ) -> None:
        super().__init__(dropdown, no_data_name, controller)
        self._dropdown.observe(self._controller.widget_notify(self), "value")

    def add_choise(self, choise: str) -> None:
        options = list(self._dropdown.options)
        options.append(choise)
        self._dropdown.options = options
        self._dropdown.value = choise

    def remove_choise(self, choise: str) -> None:
        options = list(self._dropdown.options)
        options.remove(choise)
        self._dropdown.options = options

    def get_choise(self) -> None:
        return self._dropdown.value


class CheckBox(WidgetFrame, CommonCheckBox[widgets.Checkbox, CommonController]):
    def __init__(
        self,
        output: widgets.Checkbox,
        name: str,
        groups: Union[str, Set[str], None],
        controller: CommonController,
    ) -> None:
        super().__init__(output, name, groups, controller)
        self._checkbox.observe(self._controller.widget_notify(self), "value")

    def set_select(self, value: bool) -> None:
        self._checkbox.value = value
