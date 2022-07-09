import copy
import itertools
from typing import Any, Callable, Dict, Literal, Set, Union

import ipywidgets as widgets
import numpy as np
from bokeh.io import output_notebook, push_notebook, show
from bokeh.models import DataRange1d, LinearAxis, Span
from bokeh.models.renderers import GlyphRenderer
from bokeh.palettes import Set1_9, Set2_8
from bokeh.plotting import Figure, figure
from loguru import logger

from ....base_view.abc_common_framer_grapher.figure import (
    CommonFigure,
    CommonFigureMaker,
    CommonImage,
    CommonLine,
)

output_notebook()

_colors = list(Set1_9)
_colors.extend(list(Set2_8))
color_palette = itertools.cycle(_colors)

default_line_property = {"line_color": None, "line_width": 2, "line_dash": "solid"}

default_image_properties = {"palette": "Viridis256", "level": "image"}


class BokehFigureMaker(CommonFigureMaker):
    def __init__(
        self, default_line_property=default_line_property, color_palette=color_palette
    ) -> None:
        self.default_line_property = default_line_property
        self.color_palette = color_palette
        self.default_image_propertis = default_image_properties

    @staticmethod
    def get_figure(figure_properties: Dict[str, Any]) -> "BokehFigure":

        fig = figure(
            title=figure_properties["title"],
            title_location="above",
            plot_width=int(figure_properties["width"]),
            plot_height=int(figure_properties["height"]),
        )
        fig.xaxis.axis_label = figure_properties["x_axis_label"]
        fig.yaxis.axis_label = figure_properties["y_axis_label"]
        return BokehFigure(fig)

    def get_next_line_properties(self) -> Dict[str, Any]:
        line_properties = copy.deepcopy(self.default_line_property)
        line_properties["line_color"] = next(self.color_palette)
        return line_properties

    def get_next_image_properties(self) -> Dict[str, Any]:
        return {"palette": "Spectral11"}


class MetaFigure(type(widgets.Output), type(CommonFigure)):
    pass


class BokehFigure(widgets.Output, CommonFigure[Figure], metaclass=MetaFigure):
    def __init__(self, figure: Figure) -> None:
        super().__init__()
        self._figure = figure
        self._handle = None
        self._lines = {}
        self._images = {}
        self.on_displayed(lambda x: x.set_handle())

    def set_handle(self):
        self.clear_output()
        with self:
            self._handle = show(self._figure, notebook_handle=True)

    def get_handle(self):
        return self._handle

    def update(self):
        push_notebook(handle=self._handle)

    def add_extra_axis(self, axis_name: str, axis_label: str, location="right") -> None:
        self._figure.extra_y_ranges[axis_name] = DataRange1d()
        self._figure.add_layout(
            LinearAxis(y_range_name=axis_name, axis_label=axis_label), location
        )

    def get_axis(self, axis_name: str = None, type_axis: str = "y"):
        if type_axis == "x":
            if axis_name in self._figure.extra_x_ranges:
                return self._figure.extra_x_ranges[axis_name]
            else:
                return self._figure.x_range
        elif type_axis == "y":
            if axis_name in self._figure.extra_y_ranges:
                return self._figure.extra_y_ranges[axis_name]
            else:
                return self._figure.y_range

    def set_limits(
        self,
        range_axis: DataRange1d,
        min_z=0,
        max_z=1,
    ):

        range_axis.start = min_z + min_z * 0.25
        range_axis.end = max_z + max_z * 0.25

    def add_line(
        self,
        x: np.ndarray,
        y: np.ndarray,
        name: str,
        groups: Set[str],
        line_property: Dict[str, Any],
    ) -> "BokehLine":

        line = self._figure.line(x, y, **line_property)
        bokeh_line = BokehLine(line, name, groups, self.update)
        self._lines.update({name: bokeh_line})
        return bokeh_line

    def add_image(
        self,
        x: np.ndarray,
        y: np.ndarray,
        s_xy: np.ndarray,
        unique_name: str,
        groups: Union[str, Set[str]],
        image_properties: Dict[str, Any],
    ) -> None:

        if isinstance(groups, str):
            groups = set([groups])

        image = self._figure.image(
            image=[s_xy],
            x=x[0],
            y=y[0],
            dw=x[-1] - x[0],
            dh=y[-1] - y[0],
            **image_properties
        )
        image.level = "underlay"
        self._images.update(
            {unique_name: BokehImage(image, unique_name, groups, self.update)}
        )

    def add_infty_line(
        self,
        k: np.ndarray,
        axis: Literal["x", "y"],
        unique_name: str,
        groups: Set[str],
        line_properties: Dict[str, Any],
    ) -> None:

        if axis == "x":
            line = Span(location=k, dimension="height", **line_properties)
        elif axis == "y":
            line = Span(location=k, dimension="width", **line_properties)
        else:
            line = None

        self._figure.add_layout(line)
        bokeh_line = BokehLine(line, unique_name, groups, self.update)
        self._lines.update({unique_name: bokeh_line})


class BokehLine(CommonLine[GlyphRenderer]):
    def __init__(
        self, line: GlyphRenderer, name: str, groups: Union[str, Set[str]], update: Any
    ) -> None:
        super().__init__(line, name, groups)
        self._update = update

    def get_color(self) -> str:
        return list(self._line.glyph.references())[0].line_color

    def set_visible(self, check: bool) -> None:
        self._line.visible = check
        self._update()


class BokehImage(CommonImage[GlyphRenderer]):
    def __init__(
        self,
        image: GlyphRenderer,
        name: str,
        groups: Set[str],
        update: Callable[..., None],
    ) -> None:
        super().__init__(image, name, groups)
        self._update = update

    def set_visible(self, is_visible: bool) -> None:
        self._image.visible = is_visible
        self._update()
