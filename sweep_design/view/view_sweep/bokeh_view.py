from ..framemakers.ipywidgetframer.figwidget.bokehfig import BokehFigureMaker

from ..framemakers.ipywidgetframer.ipywidgetframe import WidgetFrameMaker

from .common_view_builder import CommonVeiwSweepBuilder

from ..framemakers.ipywidgetframer.default_ipywidget_properties import (
    get_checkbox_frame,
    get_dropdown_frame,
    get_figure_frame,
)
from ..framemakers.ipywidgetframer.figwidget.default_bokeh_properties import (
    get_figure_window,
)


def get_view_sweep_bokeh_ipywidget(
    k_width=1.0,
    k_height=1.0,
):
    return CommonVeiwSweepBuilder(
        BokehFigureMaker,
        WidgetFrameMaker,
        get_figure_window(
            "Signal", "Time, s", "Amplitude", 0.7 * k_width, 0.4 * k_height
        ),
        get_figure_frame(0.7 * k_width, 0.4 * k_height),
        get_checkbox_frame("Signals", "No signal", 0.2 * k_width, 0.4 * k_height),
        get_figure_window(
            "Amplitude spectrum",
            "Frequency, Hz",
            "Amplitude",
            0.7 * 0.5 * k_width,
            0.4 * k_height,
        ),
        get_figure_frame(0.7 * 0.5 * k_width, 0.4 * k_height),
        get_figure_window(
            "Phase spectrum",
            "Frequency, Hz",
            "Phase",
            0.7 * 0.5 * k_width,
            0.4 * k_height,
        ),
        get_figure_frame(0.7 * 0.5 * k_width, 0.4 * k_height),
        get_figure_window(
            "Sweep", "Time, s", "Amplitude", 0.7 * k_width, 0.4 * k_height
        ),
        get_figure_frame(0.7 * k_width, 0.4 * k_height),
        get_figure_window(
            "Spectrogram", "Time, s", "Frequency, Hz", 0.7 * k_width, 0.4 * k_height
        ),
        get_figure_frame(0.7 * k_width, 0.4 * k_height),
        get_dropdown_frame("Sweeps", "No sweep"),
        get_figure_window(
            "Envelop", "Time, s", "Amplitude", 0.7 * k_width, 0.4 * k_height
        ),
        get_figure_frame(0.7 * k_width, 0.4 * k_height),
        get_checkbox_frame("Sweeps", "No sweep", 0.2 * k_width, 0.4 * k_height),
    )
