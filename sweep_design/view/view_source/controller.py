from typing import Any, Dict

from ..base_view.abc_common_framer_grapher.figure import CommonFigure

from ..base_view.abc_common_framer_grapher.frame import (
    CommonCheckBoxFrame,
    CommonDropdownFrame,
    CommonFigureFrame,
    CommonCheckBox,
)

from ..base_view.abc_common_framer_grapher.controller import CommonController


class BoundElement:
    def __init__(self, element: Any) -> None:
        self._element = element
        self._bound_elements: Dict[int, Any] = {}

    def bound_element(self, bound_element: Any) -> None:
        self._bound_elements.update({int(bound_element): bound_element})


class InteracterSource(CommonController):
    def __init__(
        self,
        dropdown_singals_frame: CommonDropdownFrame = None,
        signal_figure_frame: CommonFigureFrame[CommonFigure] = None,
        checkbox_types_signals_frame: CommonCheckBoxFrame[CommonCheckBox] = None,
    ) -> None:
        self._dropdown_singals_frame = dropdown_singals_frame
        self._signal_figure_frame = signal_figure_frame
        self._checkbox_types_signals_frame = checkbox_types_signals_frame

    def set_controlled_objects(
        self,
        dropdown_singals_frame: CommonDropdownFrame,
        signal_figure_frame: CommonFigureFrame[CommonFigure],
        checkbox_types_signals_frame: CommonCheckBoxFrame[CommonCheckBox],
    ) -> None:
        self._dropdown_singals_frame = dropdown_singals_frame
        self._signal_figure_frame = signal_figure_frame
        self._checkbox_types_signals_frame = checkbox_types_signals_frame

    def widget_notify(self, obj):
        def listner(value: Dict[str, Any]):
            if obj is self._dropdown_singals_frame:
                self._call_dropdown_signal(value)

            if obj in self._checkbox_types_signals_frame.get_checkboxs().values():
                self._call_checkbox_types_signals(obj.get_name(), value)

                # line = self._signal_figure_frame.get_figure().get_line(obj.get_name())
                # print(line)
                # print(obj.get_name())
                # if line:
                #     line.set_visible(value['new'])

        return listner

    def _call_checkbox_types_signals(self, group: str, value: bool):
        current_dropdown_choise = self._dropdown_singals_frame.get_choise()

        for line in self._signal_figure_frame.get_figure().get_lines_by_groups(
            set([group, current_dropdown_choise])
        ):
            line.set_visible(value["new"])
        if group == "limits":
            for line in self._signal_figure_frame.get_figure().get_lines_by_groups(
                set([group])
            ):
                line.set_visible(value["new"])

    def _call_dropdown_signal(self, value: Dict[str, Any]):
        value_new = value["new"]
        for line in self._signal_figure_frame.get_figure().get_lines_by_groups(
            set([value_new])
        ):
            line.set_visible(True)
        value_old = value["old"]
        for line in self._signal_figure_frame.get_figure().get_lines_by_groups(
            set([value_old])
        ):
            line.set_visible(False)

        for checkbox in self._checkbox_types_signals_frame.get_checkboxs().values():
            checkbox.set_select(True)
