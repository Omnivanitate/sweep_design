'''Module view.

The module provides several functions to get simple GUI to visualize the 
results in `jupyter notebook`.

The `sweep_design.view.base_view.abc_common_framer_grapher` module contains 
abstract classes for creating GUI elements.

The `sweep_design.view.framemakers` module contains concrete classes for 
creating GUIs.

For example, classes that create graphics windows use libraries such as 
`bokeh` (http://docs.bokeh.org/) or `matplotlib` (https://matplotlib.org/), 
classes that create controls use the `ipywidget` (https://ipywidgets.readthedocs.io) 
library.

The modules described above can be used to create your own GUI.

Also, the `sweep_design.view` module contains several ready-made solutions. 
There are only 4 of them so far and they use the ipywidget, matplotlib and 
bokeh libraries:

- - -

The `sweep_design.view.view_general` module provides functions for general 
visualization (get_general_view_bokeh_ipywidget and 
get_general_view_matplotlib_ipywidget (the names indicate which libraries are used))

Functions accept:
> k_width: float = 1. - the horizontal ratio of the render model window size 
to the screen size
> k_height: float = 1. - vertical ratio of the render model window size to 
the screen size

Return a `GeneralView` object (`sweep_design.view.view_general.view.GeneralView`) 
that represents a single render window. But by calling the function several 
times, you can get several new instances of the GeneralView class,
and they can be combined as needed.

Next, you can build graphs and images using the `add_line` and `add_image` 
methods in the required corresponding instances, and then render in the 
corresponding cell by calling the `show()` method or by selecting an attribute 
of the object `result_view` and calling the `get_output()` method.

An example can be seen in the `examples.general_view.ipynb` folder in the project 
https://github.com/Omnivanitate/sweep_design  

- - -

The `sweep_design.view.view_source` module contains functions for visualizing a 
sweep signal for a vibration source. Displays the change in force as well as 
a graph of displacement.

A new visualization object is created using the get_view_source_bokeh_ipywidget 
function, which is passed the parameters:
> reaction_mass: float = 1. - reaction mass of the source, 
> limits: float = None - limits limiting its fluctuations, 
> k_width: float = 1. - horizontal ratio of the visualization model window 
size to the screen size,
> k_height: float = 1. - vertical ratio of render model window size to screen size

The function returns an instance of the `ViewSource` class 
(`sweep_design.view.view_source.source_view_builder.ViewSource`).

The newly created instance can be passed a signal (an instance of the 
NamedRealtion class) using the add_signal method. 
And by calling the show() method, visualize the result in the cell.

An example can be seen in the `examples.source_view.ipynb` folder in the project 
https://github.com/Omnivanitate/sweep_design 

- - -

The  module `sweep_design.view.view_sweep contains the 
`get_view_sweep_bokeh_ipywidget` function. 

The function accepts:
> k_width: float = 1. - horizontal ratio of the visualization model window 
size to the screen size,
> k_height: float = 1. - vertical ratio of render model window size to screen size

The function retruns an instanse of `CommonVeiwSweepBuilder` class 
(sweep_design.view.view_sweep.common_view_builder.CommonVeiwSweepBuilder) 
to visualize sweep signals (`NamedSweep`) and other signals (`NamedSignal`).

The instance of the `CommonVeiwSweepBuilder` class contains an `add` method
that can take the `NamedSweep` or `NamedSignal` instance.

You can plot the result in a cell using the `show()` method.

An example can be seen in the `examples.sweep_view.ipynb` folder in the project 
https://github.com/Omnivanitate/sweep_design

- - -

`sweep_design.view.view_pilot_rm_bp` module for visualization of 
control signal, plate signal and reaction mass signal.
The module contains a function (get_pilot_rm_bp_view_bokeh_ipywidget) 
that takes two arguments:
> k_width: float = 1. - horizontal ratio of the visualization model window 
size to the screen size,
> k_height: float = 1. - vertical ratio of render model window size to screen size

The function returns a `PilotRMBPBokehView` instance 
(`sweep_design.view.view_pilot_rm_bp.bokeh_view.PilotRMBPBokehView`) for rendering.

To add signals (pilot: `NamedSweep`, reaction_mass: `NamedSweep`, base_plate: `NamedSweep`) 
the class instance has an `add_pilot_rm_bp` method that accepts them.

You can plot the result in a cell using the `show()` method.

An example can be seen in the `examples.pilot_rm_bp_view.ipynb` folder in 
the project https://github.com/Omnivanitate/sweep_design

'''

from .view_general import get_general_view_bokeh_ipywidget as \
                                        get_general_view_bokeh_ipywidget    
from .view_general import get_general_view_matplotlib_ipywidget as \
                                        get_general_view_matplotlib_ipywidget    
from .view_pilot_rm_bp import get_pilot_rm_bp_view_bokeh_ipywidget as \
                                        get_pilot_rm_bp_view_bokeh_ipywidget
from .view_source import get_view_source_bokeh_ipywidget as \
                                        get_view_source_bokeh_ipywidget
from .view_sweep import get_view_sweep_bokeh_ipywidget as \
                                        get_view_sweep_bokeh_ipywidget