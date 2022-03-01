from IPython.display import display, clear_output
from bokeh.io.notebook import push_notebook
import ipywidgets as widgets
from ipywidgets import VBox, Box

def build_line_output(out: widgets.Output, property_category: dict):

    label = widgets.HTML(
        value=f"<b><font color='black'>Lines:</b>")

    checkbox = widgets.VBox([label])

    out2 = widgets.Output()
    with out2:
        clear_output(True)
        display(checkbox)

    out2.layout = widgets.Layout(width='{0}px'.format(property_category['width']*0.24),
                                 )

    out3 = widgets.HBox([out2])
    out3.layout = widgets.Layout(width='{0}px'.format(property_category['width']*0.25-1),
                                 height='{0}px'.format(
                                     property_category['height']),
                                 border='solid 1px black',
                                 margins='10px, 10px, 10px, 10px',
                                 padding='5px, 5px, 5px, 5px'
                                 )

    return widgets.HBox([out, out3]), checkbox

def get_widgets_check_box(name, line, color):
    text = '____ {0}'.format(name)
    w = widgets.Checkbox(
        value=True,
        description=f'<b><font color={color}>{text}</b>',
        disabled=False,
        indent=False
    )
    # w.layout.width = '{0}px'.format(len(text)*10)
    w.observe(disable_line(line), names='value')
    return w

def disable_line(line):
    def listner(value):
        line.visible = value
        push_notebook()
    return listner
