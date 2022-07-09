# The project is intended for designing sweep signals.
  
- - -  

The package is written using Python to create and develop sweep signals of 
varying complexity. 
  
The package contains not only tools for creation, but also tools for analysis, 
visualization and other purposes. 
    
The project can be used both for educational and production purposes.

It is convenient to use [`Jupyter Lab`](https://jupyter.org/) or 
[`Jupyter Notebook`](https://jupyter.org/) to speed up the development 
of signals, to compare their parameters with other signals, 
and to visualize them. To visualize graphs, the project contains modules 
corresponding to these tasks. (In code editors or IDEs, rendering of images, 
graphs may not be correct. It's better to use `Jupyter Lab` directly.)  
  
The project is designed so that you can easily change the creation of sweep 
signals. For example, write your own methods describing how the frequency 
and amplitude will change from the time of the sweep signal.  
  
The project was made to be able to create various sweep signals: implemented 
and not implemented by a vibration source, from simple ones, like a linear 
sweep signal, to complex ones, like a pseudo-random sweep signal.
  
Tools have been written with which unrealizable sweep signals 
could be made realizable. The tools are in the 
"sweep_design/math_signals/utility_function" folder. 

In addition to them, the project contains the `example` folder, which contains 
examples of the implementation of various sweep signals.  

- - -

## Install.

You can install the library using `pip install sweep_design`, or you can 
clone or load it from GitHub, add path to the module and install requremnt 
packages using the `poetry install` or `pip install -r requirement.txt`, 
or coping pieces of code and create your own.

- - - 
## Using the library. 

The project is a library. Working with it is the same as with 
other third-party libraries of the python language.  
An example of how to include the library is described 
[here](https://docs.python.org/3/tutorial/modules.html).

The library consists of five sub-modules.

* `sweep_design.config` - contains the project configuration.
* `sweep_design.dataio` - contains simple functions for loading and saving 
data. For a difficult situation, write your own.
* `sweep_design.math_signals` - There is the core of project. Here is the basic 
concept of creating signals, specectra and sweep-signals realising. 
* `sweep_design.named_signals` - There is a representation of the created 
`math_signals` object. For simplicity, each represented object from 
`named_signals` has an additional field like name and category. This is 
convenient when you work with many signals, spectra and you don't to get 
confused.
* `sweep_design.view` - There is a sub-module for visualasing results. 
Contains a few `GUI` for `jupyter notebook`, `jupyter lab`.


- - -

## Quickstart.
  
Below is a simple example of creating a sweep signal and visualizing it. 
A more extended description of the work of the library in the documentation. 
Other examples are contained in the examples 
[folder](https://github.com/Omnivanitate/sweep_design/tree/main/examples).

```python
import matplotlib.pyplot as plt

from sweep_design import UncalculatedSweep
from sweep_design.math_signals.utility_functions import  get_time

time = get_time(end=50, dt=0.01)

usw = UncalculatedSweep(t=time)
sw = usw()

t_sw, a_sw = sw.get_data()
plt.plot(t_sw, a_sw)
plt.xlabel('Time, s')
plt.ylabel('Amplitude')
plt.title('Sweep-signal')

```  

![sweep_with_matplotlib](https://user-images.githubusercontent.com/89973180/156033978-ccc8de40-9f6b-4bb1-b59f-7a3ea41d2f64.png "Linear Sweep") 

or using the default ```sweep_design.view``` module for rendering,
based on using the [`ipywidget`](https://ipywidgets.readthedocs.io/) and 
[`bokeh`](http://docs.bokeh.org/) libraries

```python
from sweep_design import NamedSweep
from sweep_design.view import get_view_sweep_bokeh_ipywidget

c_sw = NamedSweep(sw)
bokeh_view = get_view_sweep_bokeh_ipywidget()
bokeh_view.add(c_sw)
bokeh_view.show()
```

![sweep_with_ipywidgets_bokeh](https://user-images.githubusercontent.com/89973180/156037232-c3b11ec4-f653-44a2-be20-ec87f481d9b7.png "Linear Sweep GUI")

- - - 

## More information in documentation.

More detailed tutorial can be found in the file examples.manual.ipynb.
Documentation is in documentation/sweep_design/index.html
