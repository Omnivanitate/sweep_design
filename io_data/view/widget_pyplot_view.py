from functools import wraps
import itertools
import logging

from ipywidgets import VBox, Box
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display

from math_signals.math_relation import Relation
from math_signals.defaults.base_structures import Spectrogram
from io_data.view.config_view import default_categories, default_categories_layout

_name = 'Set3'
_cmap = plt.cm.get_cmap(_name)
_colors = list(_cmap.colors)
_name2 = 'tab10'
_cmap2 = plt.cm.get_cmap(_name2)
_colors.extend(list(_cmap2.colors))

_colors = itertools.cycle(_colors)

px = 1/plt.rcParams['figure.dpi']

def rgb2hex(rgb):
    return '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def complite_default_fig(fig):
    def small_sleep(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            plt.ioff()
            _ = plt.figure(fig.number)
            plt.ion()
            return result
        return wrapper
    return small_sleep


class IpywidgetsMatplotlibView:
    
    _default_fig = plt.figure(-1)

    defualt_entity_property = dict(
        color=None,
        linewidth=2,
        linestyle='solid'
    )

    def __init__(self, categories: dict = None, categories_layout: list = None) -> None:
        if categories is None:
            categories = default_categories
        if categories_layout is None:
            categories_layout = default_categories_layout

        self.categories_layout = categories_layout
        self.categories_properties = categories
        self.figures = {}
        self.axes = {}
        self.checkbox = {}
        self.outs = {}
        self.dropdown = {}
        self.images = {}

    def add_figure(self, category: str) -> bool:
    
        if category in list(self.categories_properties.keys()):
            if category not in list(self.outs.keys()):
                category_properties = self.categories_properties[category]
                fig, axes = get_plot(category_properties)
                self.figures.update({category:fig})
                self.axes.update({category:axes})
                out, checkbox = build_line_output(fig, category_properties)
                self.checkbox.update({category:checkbox})
                self.outs.update({category: out})
                logging.debug('Added figure with category {0}'.format(category))
            return True
        else:
            logging.warning('Category {0} of relation entity does not set \
                in categories_properties!'.format(category))
            return False

    @complite_default_fig(_default_fig)
    def add_line(self, relation_entity: Relation, property_line: dict):
        category = relation_entity.category
        if not self.add_figure(category):
            return 
        if self.axes[category]:
            line = get_line(relation_entity, self.axes[category], property_line)
            self.checkbox[category].children += (
                get_widgets_check_box(line[0], relation_entity.get_name()),)
            logging.debug('Added line relation entity {0}'.format(str(relation_entity)))
        
    @complite_default_fig(_default_fig)
    def add_image(self, spectrogram: Spectrogram, name: str, property_image: dict):
        category = spectrogram.category
        if not self.add_figure(category):
            return
        else:
            extent = (0, 1, -10, 10)
            img = self.axes[category].imshow(
                spectrogram.S, extent=extent, 
                origin = 'lower', aspect='auto')
            self.images.update({category:{name: spectrogram}})
            self.dropdown.update({category: get_drop_down(img, self.images[category])})
            self.outs[category] = widgets.VBox(
                [self.dropdown[category], self.outs[category]])
            
        self.images[category].update({name: spectrogram})
        options = list(self.dropdown[spectrogram.category].options)
        options.append(name)

        self.dropdown[category].options = options
        self.dropdown[category].value = name

    def get_next_color(self):
        return next(_colors)

    @complite_default_fig(_default_fig)
    def show(self):
        display(get_output_layout(self.categories_layout, self.outs))
        

def get_plot(property_category):
    fig, axes = plt.subplots(constrained_layout=True,
                    figsize=(0.65*property_category['width']*px, 0.61*property_category['height']*px))
    fig.canvas.header_visible = False
    axes.set_xlabel(property_category['x_axis_label'])
    axes.set_ylabel(property_category['y_axis_label'])
    axes.set_title(property_category['title'])
    return fig, axes

def get_line(relation_entety: Relation, axes, property_line: dict):
    x, y = relation_entety.get_data()
    line = axes.plot(x, y, **property_line)
    return line

def get_output_layout(category_layout: list, pre_outs: dict):
    layout_ = []
    if isinstance(category_layout, list):
        for k in category_layout:
            result = get_output_layout(k, pre_outs)
            if isinstance(result, Box):
                layout_.append(result)

    elif isinstance(category_layout, str):
        if category_layout in list(pre_outs.keys()):
            return pre_outs[category_layout]

    return VBox(layout_)

def build_line_output(fig, property_category: dict):

    out = widgets.Output()

    with out:
        plt.show(fig)

    out.layout = widgets.Layout(width='{0}px'.format(property_category['width']),
                                height='{0}px'.format(
                                    property_category['height']),
                                border='solid 1px black',
                                margins='10px, 10px, 10px, 10px',
                                padding='5px, 5px, 5px, 5px'
                                )
    label = widgets.HTML(value=f"<b><font color='black'>Lines:</b>")
    checkbox = widgets.VBox([label])
    out2 = widgets.Output()
    
    with out2:
        display(checkbox)

    out3 = widgets.HBox([out2])
    out3.layout = widgets.Layout(width='{0}px'.format(property_category['width']*0.25),
                                 height='{0}px'.format(
                                     property_category['height']),
                                 border='solid 1px black',
                                 margins='10px, 10px, 10px, 10px',
                                 padding='5px, 5px, 5px, 5px'
                                 )

    return widgets.HBox([out, out3]), checkbox

def get_widgets_check_box(line, name):
    text = '____ {0}'.format(name)
    w = widgets.Checkbox(
        value=True,
        description=f'<b><font color={rgb2hex(line.get_color())}>{text}</b>',
        disabled=False,
        indent=False
    )
    # w.layout.width = '{0}px'.format(len(text)*10)
    w.observe(disable_line(line), names='value')
    return w

def disable_line(line):
    def listner(value):
        line.set_visible(value.new)
    return listner

def get_drop_down(currnet_image, images: dict):
    w = widgets.Dropdown(
        options=['No spectrogram'],
        value='No spectrogram',
        description='Spectrograms',
        disabled=False
    )
    w.observe(change_image(currnet_image, images), 'value')
    return w

def change_image(current_image, images: dict):
    def listner(value):
        if value.new != 'No spectrogram':
            data = images[value.new]
            extent = (data.t[0], data.t[-1], data.f[0], data.f[-1])
            current_image.set_data(A=data.S/data.S.max())

            current_image.set_extent(extent)
            current_image.set_visible(True)
        else:
            current_image.set_visible(False)

    return listner    


