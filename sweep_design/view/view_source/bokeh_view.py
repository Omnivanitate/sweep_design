import copy
from ..framemakers.ipywidgetframer.figwidget.bokehfig import BokehFigureMaker
from ..framemakers.ipywidgetframer.ipywidgetframe import WidgetFrameMaker
from .source_view_builder import ViewSource
from ..framemakers.ipywidgetframer.default_ipywidget_properties import (
    get_checkbox_frame,
    get_dropdown_frame,
    get_figure_frame,
)
from ..framemakers.ipywidgetframer.figwidget.default_bokeh_properties import (
    get_figure_window,
)

from ..framemakers.ipywidgetframer.figwidget.bokehfig import default_line_property


def get_view_source_bokeh_ipywidget(
    reaction_mass=1.0, limits=None, k_width=1.0, k_height=1.0
):

    sweep_color = "blue"
    displacement_color = "green"
    envelop_color = "red"

    line_properties_sweep = copy.deepcopy(default_line_property)
    line_properties_sweep["line_color"] = sweep_color

    line_properties_envelope = copy.deepcopy(default_line_property)
    line_properties_envelope["line_color"] = envelop_color

    line_properties_displacement = copy.deepcopy(default_line_property)
    line_properties_displacement["line_color"] = displacement_color

    line_properties_limits = copy.deepcopy(default_line_property)
    line_properties_limits["line_color"] = "yellow"

    figure_window = get_figure_window(
        "Signals", "Time, s", "Force, N", k_width * 0.8, k_height
    )
    figure_window.update(
        {"extra_range_y_name": "displacement", "y_axis_label_2": "Position, m"}
    )
    figure_frame = get_figure_frame(k_width * 0.8, k_height)
    checbox_frame = get_checkbox_frame(
        "Sweep signals:", "No sweep signals!", k_width * 0.2, k_height
    )
    dropdown_frame = get_dropdown_frame("Sweep signals:", "No sweep signals!")
    line_properties_displacement["y_range_name"] = figure_window["extra_range_y_name"]

    return ViewSource(
        BokehFigureMaker,
        WidgetFrameMaker,
        figure_window,
        figure_frame,
        dropdown_frame,
        checbox_frame,
        line_properties_sweep,
        line_properties_envelope,
        line_properties_displacement,
        line_properties_limits,
        reaction_mass,
        limits,
    )
