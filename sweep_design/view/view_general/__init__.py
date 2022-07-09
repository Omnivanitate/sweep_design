from .view import GeneralView
from ..framemakers.ipywidgetframer.figwidget.bokehfig import BokehFigureMaker
from ..framemakers.ipywidgetframer.figwidget.matplotlibfig import MatplotlibFigureMaker
from ..framemakers.ipywidgetframer.ipywidgetframe import WidgetFrameMaker

from ..framemakers.ipywidgetframer.default_ipywidget_properties import (
    get_checkbox_frame,
    get_dropdown_frame,
    get_figure_frame,
)
from ..framemakers.ipywidgetframer.figwidget.default_bokeh_properties import (
    get_figure_window as get_bokeh_figure_window,
)
from ..framemakers.ipywidgetframer.figwidget.default_matplotlib_properties import (
    get_figure_window as get_matplotlib_figure_window,
)


def get_general_view_bokeh_ipywidget(
    x_axis_label: str, y_axis_label: str, title: str, k_width: float, k_height: float
):
    return GeneralView(
        BokehFigureMaker,
        WidgetFrameMaker,
        get_bokeh_figure_window(
            title, x_axis_label, y_axis_label, 0.8 * k_width, k_height * 0.9
        ),
        get_figure_frame(k_width=0.8 * k_width, k_height=k_height * 0.9),
        get_checkbox_frame(title, "No data", 0.2 * k_width, k_height * 0.9),
        get_dropdown_frame("Data:", "No data!"),
    )


def get_general_view_matplotlib_ipywidget(
    x_axis_label: str,
    y_axis_label: str,
    title: str,
    k_width: float = 1.0,
    k_height: float = 1.0,
):

    return GeneralView(
        MatplotlibFigureMaker,
        WidgetFrameMaker,
        get_matplotlib_figure_window(
            title, x_axis_label, y_axis_label, 0.8 * k_width, k_height * 0.9
        ),
        get_figure_frame(k_width=0.8 * k_width, k_height=k_height * 0.9),
        get_checkbox_frame(title, "No data", 0.2 * k_width, k_height * 0.9),
        get_dropdown_frame("Data:", "No data!"),
    )
