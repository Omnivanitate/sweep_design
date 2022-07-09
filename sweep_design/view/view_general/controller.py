from typing import Dict, Union

from ..base_view.abc_common_framer_grapher.figure import CommonFigure
from ..base_view.abc_common_framer_grapher.frame import (
    CommonCheckBox,
    CommonCheckBoxFrame,
    CommonDropdownFrame,
    CommonFigureFrame,
)

from ..base_view.abc_common_framer_grapher.controller import CommonController


class InteracterPlotView(CommonController):
    def __init__(self) -> None:
        self._frame = None
        self._checkbox = None
        self._dropdown = None

    def set_controlled_object(
        self,
        frame: CommonFigureFrame[CommonFigure],
        checkbox: CommonCheckBoxFrame,
        dropdown: CommonDropdownFrame,
    ) -> None:

        self._frame = frame
        self._checkbox = checkbox
        self._dropdown = dropdown

    def widget_notify(self, obj: Union[CommonCheckBox, CommonDropdownFrame]):
        def listner(value: Dict):
            if isinstance(obj, CommonCheckBox):
                self._set_line_by_checkbox(obj, value["new"])

            if obj is self._dropdown:
                self._set_image(value["new"], True)
                self._set_image(value["old"], False)

        return listner

    def _set_line_by_checkbox(self, checkbox: CommonCheckBox, value: bool) -> None:

        line = self._frame.get_figure().get_line(checkbox.get_name())
        if line:
            line.set_visible(value)

    def _set_image(self, image_name: str, value: bool) -> None:

        image = self._frame.get_figure().get_image(image_name)
        if image:
            image.set_visible(value)
