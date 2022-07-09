from typing import Dict, Iterable, Literal, Set, Tuple, Any, Union
import copy
import itertools
import ipywidgets as widgets
import numpy as np

from matplotlib.figure import Figure

from ....base_view.abc_common_framer_grapher.figure import (
    CommonFigure,
    CommonFigureMaker,
    CommonImage,
    CommonLine,
)

import matplotlib.pyplot as plt

import matplotlib.colors as mcolors


PaletteColors = Iterable[Tuple[float, float, float]]

_px = 1 / plt.rcParams["figure.dpi"]
_default_line_properties = {"color": None, "linewidth": 2, "linestyle": "solid"}


_color_palette = itertools.cycle(mcolors.TABLEAU_COLORS)


class MetaFigure(type(widgets.Output), type(CommonFigure)):
    pass


class MatplotlibFigureMaker(CommonFigureMaker):
    def __init__(
        self,
        default_line_properties=_default_line_properties,
        color_palette=_color_palette,
    ) -> None:
        self._default_line_properties = default_line_properties
        self._color_palette = color_palette
        self._default_image_properties = None

    @staticmethod
    def get_figure(figure_properties: Dict[str, Any]) -> "PltFigure":
        fig, axes = plt.subplots(
            constrained_layout=True,
            figsize=(
                0.75 * figure_properties["width"] * _px,
                0.75 * figure_properties["height"] * _px,
            ),
        )

        fig.canvas.header_visible = False
        axes.set_xlabel(figure_properties["x_axis_label"])
        axes.set_ylabel(figure_properties["y_axis_label"])
        axes.set_title(figure_properties["title"])

        return PltFigure(fig, axes)

    def get_next_line_properties(self) -> Dict[str, Any]:
        line_properties = copy.deepcopy(self._default_line_properties)
        line_properties["color"] = next(self._color_palette)
        return line_properties

    def get_next_image_properties(self) -> Dict[str, Any]:
        return "twilight"


class PltFigure(widgets.Output, CommonFigure[Figure], metaclass=MetaFigure):
    def __init__(self, figuer, axes) -> None:
        super().__init__()
        self.figure = figuer
        self.axes = axes
        self.mult_axes = {}
        self._lines = {}
        self._images = {}

        with self:
            plt.show(self.figure)

    def update(self):
        self.figure.canvas.draw()

    def add_extra_axis(self, axis_name: str, axis_label: str, location="right") -> None:
        self.mult_axes[axis_name] = self.axes.twinx()
        self.mult_axes[axis_name].label(axis_label)

    def get_axis(self, axis_name: str = None, type_axis: str = "y"):
        return self.mult_axes[axis_name]

    def add_line(
        self, x, y, unique_name: str, groups: Union[str, Set[str]], line_property: dict
    ) -> "PltLine":
        (line,) = self.axes.plot(x, y, **line_property)
        plt_line = PltLine(line, unique_name, groups, self.update)
        self._lines.update({unique_name: plt_line})
        return plt_line

    def add_image(
        self,
        x: np.ndarray,
        y: np.ndarray,
        s_xy: np.ndarray,
        unique_name: str,
        groups: Set[str],
        image_properties: dict,
    ) -> None:
        extent = (x[0], x[-1], y[0], y[-1])
        image = self.axes.imshow(
            s_xy, extent=extent, origin="lower", aspect="auto", cmap=image_properties
        )
        self._images.update(
            {unique_name: PltImage(image, unique_name, groups, self.update)}
        )

    def add_infty_line(
        self,
        k: np.ndarray,
        axis: Literal["x", "y"],
        unique_name: str,
        groups: Set[str],
        line_properties: Dict[str, Any],
    ) -> None:
        pass

    def show(self):
        plt.show(self.figure)


class PltLine(CommonLine):
    def __init__(self, line, name: str, groups: Union[str, Set[str]], update) -> None:
        super().__init__(line, name, groups)
        self._update = update

    def get_color(self) -> str:
        color = self._line.get_color()
        color = color.split("tab:")[-1]
        return color

    def set_visible(self, is_visible: bool) -> None:

        self._line.set_visible(is_visible)
        self._update()


class PltImage(CommonImage):
    def __init__(self, image, name: str, groups: Set[str], update) -> None:
        super().__init__(image, name, groups)
        self._update = update

    def set_visible(self, is_visible: bool) -> None:

        self._image.set_visible(is_visible)
        self._update()
