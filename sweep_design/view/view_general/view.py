import numpy as np

from sweep_design.named_signals.named_sweep import NamedSpecrogram

from ..base_view.abc_common_framer_grapher.figure import CommonFigure, CommonFigureMaker
from ..base_view.abc_common_framer_grapher.frame import CommonFrameMaker

from ...math_signals import Relation
from ...named_signals import NamedRelation, NamedSweep

from .controller import InteracterPlotView

from typing import Any, Dict, Type, Union


class GeneralView:
    def __init__(
        self,
        grapher: Type[CommonFigureMaker],
        framer: Type[CommonFrameMaker[CommonFigure, InteracterPlotView]],
        figure_properties: Dict[str, Any],
        frame_properties: Dict[str, Any],
        checkbox_properties: Dict[str, Any],
        dropdown_properties: Dict[str, Any],
    ) -> None:

        self._grapher = grapher()
        self._controller = InteracterPlotView()

        figure = grapher.get_figure(figure_properties)
        self._frame = framer.get_figure_frame(figure, frame_properties)
        self._checkbox = framer.get_checkbox_frame(
            checkbox_properties, self._controller
        )
        self._dropdown = framer.get_dropdown_frame(
            dropdown_properties, self._controller
        )

        result_frame = self._frame.h_add(self._checkbox)
        result_frame = self._dropdown.v_add(result_frame)

        self._result_frame = result_frame

        self._controller.set_controlled_object(
            self._frame, self._checkbox, self._dropdown
        )

    @property
    def result_view(self):
        return self._result_frame

    def add_line(
        self,
        x: Union[NamedRelation, np.ndarray],
        y: np.ndarray = None,
        name: str = None,
        line_properties: Dict[str, Any] = None,
    ):

        if line_properties is None:
            line_properties = self._grapher.get_next_line_properties()

        if isinstance(x, (Relation, NamedRelation)):
            if name is None:
                name = str(x)
            line = self._frame.get_figure().add_line(
                *x.get_data(), name, None, line_properties
            )

        else:
            line = self._frame.get_figure().add_line(x, y, name, None, line_properties)

        self._checkbox.add_choise(
            name, None, {"color": line.get_color()}, self._controller
        )

    def add_image(
        self,
        x,
        y: np.ndarray = None,
        s_xy: np.ndarray = None,
        name: str = None,
        image_properties: Dict[str, Any] = None,
    ):

        if image_properties is None:
            image_properties = self._grapher.get_next_image_properties()

        if isinstance(x, (NamedSweep, NamedSpecrogram)):
            if name is None:
                name = str(x)
            if isinstance(x, NamedSweep):
                spectrogram = x.spectrogram
            else:
                spectrogram = x
            self._frame.get_figure().add_image(
                spectrogram.time,
                spectrogram.frequency,
                spectrogram.spectrogram_matrix,
                unique_name=name,
                groups=None,
                image_properties=image_properties,
            )

        else:
            self._frame.get_figure().add_image(x, y, s_xy, name, None, image_properties)

        self._dropdown.add_choise(name)

    def show(self):
        return self._result_frame.get_output()
