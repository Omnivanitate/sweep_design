from ...base_view.default_screen_properties import get_screen_params

_result = get_screen_params()

_width, _height = _result["width"], _result["height"]


def get_figure_frame(k_width=1.0, k_height=1.0):

    figure_frame = {
        "width": f"{int(_width*k_width)}px",
        "hieght": f"{int(_height*k_height)}px",
        "border": "solid 1px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
    }
    return figure_frame


def get_checkbox_frame(description: str, no_data: str = "", k_width=1.0, k_height=1.0):
    checkbox_frame = {
        "width": f"{int(_width*k_width)}px",
        "hieght": f"{int(_height**k_height)}px",
        "border": "solid 1px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
        "name_no_data": no_data,
        "description": description,
    }
    return checkbox_frame


def get_dropdown_frame(description: str, no_data: str):
    dropdown_frame = {
        "description": description,
        "name_no_data": no_data,
        "border": "solid 0px black",
        "margins": "10px, 10px, 10px, 10px",
        "padding": "5px, 5px, 5px, 5px",
        "name_no_data": "No sweep signals!",
        "description": "Sweep signals:",
    }
    return dropdown_frame
