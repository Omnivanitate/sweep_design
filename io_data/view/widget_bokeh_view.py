import itertools


from IPython.display import display, clear_output
import ipywidgets as widgets
from ipywidgets.widgets import VBox, Box
from bokeh.models import ColumnDataSource, Dropdown, CustomJS, Legend
from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure, Figure
from bokeh.palettes import Set1_9 as palette

from math_signals.math_relation import Relation
from math_signals.defaults.base_structures import Spectrogram
from io_data.view.widget_tools import build_line_output, get_widgets_check_box
from io_data.view.config_view import default_categories, default_categories_layout

output_notebook()

colors = itertools.cycle(palette)


class IpywidgetBokehView:

    defualt_entity_property = dict(
        color=None,
        line_width=2,
        line_dash='solid'
    )

    def __init__(self, categories_properties: dict = None, categories_layout: list = None) -> None:

        if categories_properties is None:
            categories_properties = default_categories
        if categories_layout is None:
            categories_layout = default_categories_layout

        self.categories_layout = categories_layout
        self.categories_properties = categories_properties
        self.figures = {}
        self.checkbox = {}
        self.blocks = {}
        self.dropdown = {}
        self.images = {}

    def add_line(self, relation_entity: Relation, line_properties: dict = None):
        if relation_entity.category in list(self.categories_properties.keys()):
            
            if relation_entity.category not in list(self.figures.keys()):
                category_property = self.categories_properties[relation_entity.category]
                fig = get_fig(category_property)
                self.figures.update({relation_entity.category: fig})
                fig_out = get_out(fig, category_property)
                block, checkbox =build_line_output(fig_out, category_property)
                self.blocks.update({relation_entity.category: block})
                self.checkbox.update({relation_entity.category: checkbox})

            line = get_line(self.figures[relation_entity.category], relation_entity, line_properties)

            self.checkbox[relation_entity.category].children += (
                get_widgets_check_box(relation_entity.get_name(), line, line_properties['color']),)

        else:
            print('Category {0} are not set'.format(relation_entity.category))
        
    def get_next_color(self):
        return next(colors)
    
    def show(self):
        display(get_output_layout2(self.categories_layout, self.blocks))
        


def get_output_layout2(category_layout: list, pre_outs: dict):
    layout_ = []
    if isinstance(category_layout, list):
        for k in category_layout:
            result = get_output_layout2(k, pre_outs)
            if isinstance(result, Box):
                layout_.append(result)

    elif isinstance(category_layout, str):
        if category_layout in list(pre_outs.keys()):
            return pre_outs[category_layout]

    return VBox(layout_)




def get_out(fig: Figure, property_category: dict):
    
    out = widgets.Output()

    with out:
        clear_output(True)
        show(fig, notebook_handle=True)

    out.layout = widgets.Layout(width='{0}px'.format(property_category['width']),
                                height='{0}px'.format(
                                    property_category['height']),
                                border='solid 1px black',
                                margins='10px, 10px, 10px, 10px',
                                padding='5px, 5px, 5px, 5px'
                                )
    return out

def get_fig(fig_properties: dict):
    fig = figure(**fig_properties)
    return fig

def get_line(fig: Figure, relation_entity: Relation, line_properties: dict):
    print(line_properties)
    print(fig)
    x, y = relation_entity.get_data()
    source = ColumnDataSource(data={'x': x, 'y': y})
    line = fig.line(x='x', y='y', source=source, **line_properties)
    print(line)
    push_notebook()
    return line
