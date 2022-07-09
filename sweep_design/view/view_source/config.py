from ..base_view.default_screen_properties import get_screen_params

result = get_screen_params()

width, height = result["width"], result["height"]

layout_categoies = ["source"]


def get_figure_window(k_width=1.0, k_height=1.0):

    figure_window = {
        "width": width * k_width * 0.95,
        "height": height * k_height * 0.95,
        "title": "Signals",
        "x_axis_label": "Time, s",
        "y_axis_label": "Force, N",
        "extra_range_y_name": "displacement",
        "y_axis_label_2": "Position, m",
    }

    return figure_window


def get_figure_frame(k_width=1.0, k_height=1):

    figure_frame = {
        "width": f"{int(width*k_width)}px",
        "hieght": f"{int(height*k_height)}px",
        "border": "solid 1px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
        "location": "up",
    }

    return figure_frame


def get_checkbox_frame(k_width=1.0, k_height=1.0):

    checbox_frame = {
        "width": f"{int(width*0.1)}px",
        "height": f"{int(height*0.4)}px",
        "border": "solid 1px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
        "name_no_data": "No sweep signals!",
        "description": "Sweep signals",
    }

    return checbox_frame


def get_dropdown_frame():
    dropdown_frame = {
        "border": "solid 0px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
        "name_no_data": "No sweep signals!",
        "description": "Sweep signals:",
    }

    return dropdown_frame
