import itertools
import copy
from typing import Callable, Dict, Any, Protocol

import ipywidgets as widgets
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure, Figure
from bokeh.models.renderers import GlyphRenderer
from bokeh.palettes import Set1_9, Set2_8

from viewrelation.commonview.protocols.figureprotocols import FigureMaker, Line, Image
from viewrelation.commonview.protocols.figureprotocols import Figure as ProtocolFigure
output_notebook()

_colors = list(Set1_9)
_colors.extend(list(Set2_8))
color_palette = itertools.cycle(_colors)

_default_line_property = {
        'line_color': None,
        'line_width': 2,
        'line_dash': 'solid'
        }


class BokehFigureMaker(FigureMaker):
    def __init__(self, defualt_line_property=_default_line_property, 
                                color_palette=color_palette) -> None:
        self.default_line_property = defualt_line_property
        self.color_palette = color_palette
    
    @staticmethod
    def get_figure(figure_properties: Dict[str, Any]) -> 'BokehFigure':

        fig = figure(
            title=figure_properties['title'],
            title_location = 'above',
            plot_width=figure_properties['width'],
            plot_height=figure_properties['height']
        )
        fig.xaxis.axis_label = figure_properties['x_axis_label']
        fig.yaxis.axis_label = figure_properties['y_axis_label']
        return BokehFigure(fig)
    
    def get_next_line_properties(self) -> Dict[str, Any]:
        line_properties = copy.deepcopy(self.default_line_property)
        line_properties['line_color'] = next(self.color_palette)
        return line_properties

    def get_image_properties(self) -> Dict[str, Any]:
        return {'palette':"Spectral11"}

class BokehFigure(widgets.Output):

    def __init__(self, figure: Figure) -> None:
        super().__init__()
        self._figure = figure
        self._handle = None
        self.on_displayed(lambda x: x.set_handle())

    def set_handle(self):
        self.clear_output()
        with self:
            self._handle = show(self._figure, notebook_handle=True)

    def get_handle(self):
        return self._handle
    
    def get_figure(self) -> Figure:
        return self._figure

    def update(self):
        push_notebook(handle=self._handle)

    def plot_line(self, x, y, line_property: Dict[str, Any], group: Any, name: str) -> 'BokehLine':
        line = self._figure.line(x, y, **line_property)
        self.update()
        return BokehLine(line, name, group, self.update)

    def plot_image(self, x, y, S, image_properties: Dict[str, Any]) -> 'BokehImage':
        image = self._figure.image(
            image=[S], x=x[0], y=y[0], dw= x[-1] - x[0], dh = y[-1] - y[0], 
            **image_properties
            )
        self.update()
        return BokehImage(image, self.update)


class BokehLine:

    def __init__(self, line: GlyphRenderer, name: str, group: Any, update: Callable[..., None]) -> None:
        self.line = line 
        self.name = name
        self.group = group
        self.update = update

    def get_color(self) -> str:
        return list(self.line.glyph.references())[0].line_color

    def trigger_by_check(self, check: bool) -> None:
        self.line.visible = check
        self.update()

class BokehImage:

    def __init__(self, image: GlyphRenderer, update: Callable[..., None]) -> None:
        self.image = image 
        self.update = update
    
    def set_visible(self, is_visible: bool) -> None:
        self.image.visible = is_visible
        self.update()


