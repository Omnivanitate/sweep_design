"""Module view.

The module provides several functions to get simple `GUI` to visualize the 
results in `jupyter notebook`.

The `sweep_design.view.base_view.abc_common_framer_grapher` module contains 
abstract classes for creating GUI elements.

The `sweep_design.view.framemakers` module contains concret classes for 
creating GUIs.

For example, classes that create graphics windows use libraries such as 
`bokeh` (http://docs.bokeh.org/) or `matplotlib` (https://matplotlib.org/), 
classes that create controls use the `ipywidget` (https://ipywidgets.readthedocs.io) 
library.

The modules described above can be used to create your own GUI.

Also, the `sweep_design.view` module contains several ready-made solutions. 
There are only 4 of them so far and they use the `ipywidget`, `matplotlib` and 
`bokeh` libraries:

- - -

The `sweep_design.view.view_general` module provides functions for general 
visualization (`sweep_design.view.view_general.get_general_view_bokeh_ipywidget` 
and `sweep_design.view.view_general.get_general_view_matplotlib_ipywidget` 
(the names of functions indicate which libraries are used))

Functions accept:
> **k_width**: `float` = 1. - the horizontal ratio of the render model window 
size to the screen size.  
> **k_height**: `float` = 1. - vertical ratio of the render model window 
size to the screen size.

Return a `sweep_design.view.view_general.view.GeneralView` object 
that represents a single render window. But by calling the function several 
times, you can get several new instances of the 
`sweep_design.view.view_general.view.GeneralView` class, and they can be 
combined as needed.

Next, you can build graphs and images using the 
`sweep_design.view.view_general.view.GeneralView.add_line` 
and `sweep_design.view.view_general.view.GeneralView.add_image` 
methods in the required corresponding instances, and then render in the 
corresponding cell by calling the 
`sweep_design.view.view_general.view.GeneralView.show()` method or by 
selecting an attribute of the object 
`sweep_design.view.view_general.view.GeneralView.result_view` and calling 
the `get_output()` method.

An example can be seen in the `examples.general_view.ipynb` folder in the project 
https://github.com/Omnivanitate/sweep_design  

- - -

The `sweep_design.view.view_source` module contains functions for visualizing a 
sweep signal for a vibration source. Displays the change in force as well as 
a graph of displacement.

A new visualization object is created using the get_view_source_bokeh_ipywidget 
function, which is passed the parameters:
> **reaction_mass**: `float` = 1. - reaction mass of the source,  
> **limits**: `float` = `None` - limits limiting its fluctuations,  
> **k_width**: `float` = 1. - horizontal ratio of the visualization model window 
size to the screen size,  
> **k_height**: `float` = 1. - vertical ratio of render model window size to 
screen size

The function returns an instance of the 
`sweep_design.view.view_source.source_view_builder.ViewSource` class.

The newly created instance can be passed a signal (an instance of the 
`sweep_design.named_signals.named_relation.NamedRelation` class) using the 
`sweep_design.view.view_source.source_view_builder.ViewSource.add_signal` 
method. And by calling 
the `sweep_design.view.view_source.source_view_builder.ViewSource.show()` 
method, visualize the result in the cell.

An example can be seen in the `examples.source_view.ipynb` folder in the project 
https://github.com/Omnivanitate/sweep_design 

- - -

The  module `sweep_design.view.view_sweep` contains the 
`sweep_design.view.view_sweep.bokeh_view.get_view_sweep_bokeh_ipywidget` 
function. 

The function accepts:
> **k_width**: `float` = 1 - horizontal ratio of the visualization model window 
size to the screen size,  
> **k_height**: `float` = 1 - vertical ratio of render model window size to screen size

The function retruns an instanse of 
`sweep_design.view.view_sweep.common_view_builder.CommonVeiwSweepBuilder` class 
to visualize sweep signals (`sweep_design.named_signals.named_sweep.NamedSweep`) 
and other signals (`sweep_design.named_signals.named_signal.NamedSignal`).

The instance of the 
`sweep_design.view.view_sweep.common_view_builder.CommonVeiwSweepBuilder` class 
contains an 
`sweep_design.view.view_sweep.common_view_builder.CommonVeiwSweepBuilder.add` 
method that can take the `sweep_design.named_signals.named_sweep.NamedSweep` 
or `sweep_design.named_signals.named_signal.NamedSignal` instance.

You can plot the result in a cell using the 
`sweep_design.view.view_sweep.common_view_builder.CommonVeiwSweepBuilder.show()` 
method.

An example can be seen in the `examples.sweep_view.ipynb` folder in the project 
https://github.com/Omnivanitate/sweep_design

- - -

`sweep_design.view.view_pilot_rm_bp` module for visualization of 
*pilot signal*, *plate signal* and *reaction mass signal*.
The module contains a function 
(`sweep_design.view.view_pilot_rm_bp.bokeh_view.get_pilot_rm_bp_view_bokeh_ipywidget`) 
that takes two arguments:

> **k_width**: `float` = 1 - horizontal ratio of the visualization model window 
size to the screen size,  
> **k_height**: `float` = 1. - vertical ratio of render model window size to 
screen size

The function returns a 
`sweep_design.view.view_pilot_rm_bp.bokeh_view.PilotRMBPBokehView` 
instance for rendering.

To add signals (**pilot**: `sweep_design.named_signals.named_sweep.NamedSweep`, 
**reaction_mass**: `sweep_design.named_signals.named_sweep.NamedSweep`, 
**base_plate**: `sweep_design.named_signals.named_sweep.NamedSweep`) 
the class instance has an 
`sweep_design.view.view_pilot_rm_bp.bokeh_view.PilotRMBPBokehView.add_pilot_rm_bp` 
method that accepts them.

You can plot the result in a cell using the 
`sweep_design.view.view_pilot_rm_bp.bokeh_view.PilotRMBPBokehView.show()` 
method.

An example can be seen in the `examples.pilot_rm_bp_view.ipynb` folder in 
the project https://github.com/Omnivanitate/sweep_design

"""

from .view_general import (
    get_general_view_bokeh_ipywidget as get_general_view_bokeh_ipywidget,
)
from .view_general import (
    get_general_view_matplotlib_ipywidget as get_general_view_matplotlib_ipywidget,
)
from .view_pilot_rm_bp import (
    get_pilot_rm_bp_view_bokeh_ipywidget as get_pilot_rm_bp_view_bokeh_ipywidget,
)
from .view_source import (
    get_view_source_bokeh_ipywidget as get_view_source_bokeh_ipywidget,
)
from .view_sweep import get_view_sweep_bokeh_ipywidget as get_view_sweep_bokeh_ipywidget
