"""Configuration file for frame and figure are used ipywidget and bokeh.

"""
from ..base_view.default_screen_properties import get_screen_params

result = get_screen_params()
width, height = result["width"], result["height"]


def get_figure_window(
    title: str,
    x_axis_label: str,
    y_axis_label: str,
    k_width=0.7,
    k_height=0.4,
) -> None:

    figure_window = {
        "width": width * k_width * 0.95,
        "height": height * k_height * 0.95,
        "title": title,
        "x_axis_label": x_axis_label,
        "y_axis_label": y_axis_label,
    }
    return figure_window


def get_figure_frame(k_width=0.7, k_height=0.4):

    figure_frame = {
        "width": f"{int(width*k_width)}px",
        "hieght": f"{int(height*k_height)}px",
        "border": "solid 1px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
        "location": "up",
    }
    return figure_frame


def get_checkbox_frame(description: str, no_data: str, k_width: float, k_height: float):

    checbox_frame = {
        "width": f"{int(width*k_width)}px",
        "height": f"{int(height*k_height)}px",
        "border": "solid 1px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
        "name_no_data": no_data,
        "description": description,
    }
    return checbox_frame


def get_dropdown_properties():

    dropdown_frame = {
        "border": "solid 0px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
        "name_no_data": "No data!",
        "description": "Data:",
    }

    return dropdown_frame


def get_default_line_properties():

    return
