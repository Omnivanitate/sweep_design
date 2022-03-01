from typing import Iterable, Tuple, Any

import matplotlib.pyplot as plt
from pltwidget.colorpalette import color_palette

PaletteColors = Iterable[Tuple[float, float, float]]

_px = 1/plt.rcParams['figure.dpi']
_default_line_property = {
                        'color':None,
                        'linewidth':2,
                        'linestyle':'solid'
                        }
_color_palette = color_palette


class MatplotlibFig:
    
    def __init__(self, default_line_property = _default_line_property, 
                color_palette: PaletteColors = _color_palette) -> None:

        self.default_line_property = default_line_property
        self.color_palette = color_palette
        
    @staticmethod
    def get_figure(frame_property: dict) -> 'PltFigure':

       
        fig, axes = plt.subplots(
            constrained_layout=True,
            figsize=(0.75*frame_property['width']*_px, 
                     0.75*frame_property['height']*_px)
        )
    
        fig.canvas.header_visible = False
        axes.set_xlabel(frame_property['x_axis_label'])
        axes.set_ylabel(frame_property['y_axis_label'])
        axes.set_title(frame_property['title'])
     
        return PltFigure(fig, axes)

    def get_next_color(self) -> Tuple[float, float, float]:
        return next(self.color_palette)

class PltFigure:

    def __init__(self, figuer, axes) -> None:
        self.figure = figuer
        self.axes = axes

    def plot_line(self, x, y, line_property: dict) -> 'PltLine':
        line, = self.axes.plot(x, y, **line_property)
        return PltLine(line)
    
    def plot_image(self, x, y, S, image_property: dict) -> 'PltImage':
        extent = (x[0], x[-1], y[0], y[-1])
        image = self.axes.imshow(S, extent=extent, origin = 'lower', aspect='auto')
        return PltImage(image)

    def show(self):
        plt.show(self.figure)

class PltLine:

    def __init__(self, line) -> None:
        self.line = line

    def set_visible(self, is_visible: bool) -> None:
        self.line.set_visible(is_visible)
    
class PltImage:
    def __init__(self, image) -> None:
        self.image = image
    
    def set_visible(self, is_visible: bool) -> None:
        self.image.set_visible(is_visible)
