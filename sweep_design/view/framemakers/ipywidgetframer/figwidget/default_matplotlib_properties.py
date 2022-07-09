from ....base_view.default_screen_properties import get_screen_params

result = get_screen_params()

width, height = result["width"], result["height"]


def get_figure_window(
    title: str, x_axis_label: str, y_axis_label: str, k_width=1.0, k_height=1.0
):
    figure_window = {
        "width": width * k_width * 1.2,
        "height": height * k_height,
        "title": title,
        "x_axis_label": x_axis_label,
        "y_axis_label": y_axis_label,
    }
    return figure_window
