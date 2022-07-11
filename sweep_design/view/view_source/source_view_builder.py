from typing import Any, Dict, Type

from ...named_signals.named_sweep import NamedSweep
from ..base_view.abc_common_framer_grapher.figure import CommonFigure, CommonFigureMaker
from ..base_view.abc_common_framer_grapher.frame import CommonFrameMaker
from .controller import InteracterSource


class ViewSource:
    def __init__(
        self,
        grapher: Type[CommonFigureMaker],
        framer: Type[CommonFrameMaker[CommonFigure, InteracterSource]],
        properties_source_figure_window: Dict[str, Any],
        properties_source_figure_frame: Dict[str, Any],
        properties_dropdown_signals_frame: Dict[str, Any],
        properties_checkbox_types_signals_frame: Dict[str, Any],
        line_properties_sweep,
        line_properties_envelope,
        line_properties_displacement,
        line_properties_limits,
        reaction_mass=1,
        limits=None,
    ) -> None:
        self._line_properties_sweep = line_properties_sweep
        self._line_properties_envelope = line_properties_envelope
        self._line_properties_displacement = line_properties_displacement
        self._line_properties_limits = line_properties_limits
        controller = InteracterSource()

        source_figure = grapher.get_figure(properties_source_figure_window)
        source_figure.add_extra_axis(
            properties_source_figure_window["extra_range_y_name"],
            properties_source_figure_window["y_axis_label_2"],
        )
        self._source_figure_frame = framer.get_figure_frame(
            source_figure, properties_source_figure_frame
        )
        self._dropdown_signals_frame = framer.get_dropdown_frame(
            properties_dropdown_signals_frame, controller
        )
        self._checkbox_types_signals_frame = framer.get_checkbox_frame(
            properties_checkbox_types_signals_frame, controller
        )

        result_frame = self._source_figure_frame.h_add(
            self._checkbox_types_signals_frame
        )
        result_frame = self._dropdown_signals_frame.v_add(result_frame)

        self._result_frame = result_frame

        controller.set_controlled_objects(
            self._dropdown_signals_frame,
            self._source_figure_frame,
            self._checkbox_types_signals_frame,
        )
        self._controller = controller

        self._reaction_mass = reaction_mass
        if limits is not None:
            source_figure.add_infty_line(
                -abs(limits),
                "y",
                "bottom_limit",
                "limits",
                self._line_properties_limits,
            )
            source_figure.add_infty_line(
                abs(limits), "y", "upper_limit", "limits", self._line_properties_limits
            )

        self._checkbox_types_signals_frame.add_choise(
            "sweep",
            "types_signals",
            {"color": self._line_properties_sweep["line_color"]},
            self._controller,
        )

        self._checkbox_types_signals_frame.add_choise(
            "displacement",
            "types_signals",
            {"color": self._line_properties_displacement["line_color"]},
            self._controller,
        )

        self._checkbox_types_signals_frame.add_choise(
            "envelope",
            "types_signals",
            {"color": self._line_properties_envelope["line_color"]},
            self._controller,
        )

        self._checkbox_types_signals_frame.add_choise(
            "limits",
            None,
            {"color": self._line_properties_limits["line_color"]},
            self._controller,
        )

    def add_signal(self, sweep_signal: NamedSweep) -> None:
        plot = self._source_figure_frame.get_figure()

        plot.add_line(
            *sweep_signal.get_data(),
            str(sweep_signal),
            set(["sweep", str(sweep_signal)]),
            self._line_properties_sweep,
        )

        displacement = sweep_signal.integrate().integrate() / self._reaction_mass

        plot.add_line(
            *displacement.get_data(),
            f"{str(sweep_signal)}_displacement",
            set(["displacement", str(sweep_signal)]),
            self._line_properties_displacement,
        )

        plot.add_line(
            *sweep_signal.a_t.get_data(),
            f"{str(sweep_signal)}_a_t",
            set(["envelope", str(sweep_signal)]),
            self._line_properties_envelope,
        )

        self._dropdown_signals_frame.add_choise(str(sweep_signal))

    def show(self):
        return self._result_frame.get_output()
