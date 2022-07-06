# The project is intended for designing sweep signals.
  
- - -  

The package is written in Python for creating and developing sweep signals of varying complexity.  
  
The package contains not only tools for creation, but also tools for analysis, visualization and other purposes. 
    
The project can be used both for educational and production purposes.  
  
It is convenient to use `Jupyter Lab` or `Jupyter Notebook` to speed up the development  
of signals, to compare their parameters with other signals, and to visualize them.  
To visualize graphs, the project contains packages corresponding to these tasks.  
(In code editors or IDEs such as vscode, rendering of images, graphs may not be correct.  
It's better to use `Jupyter Lab` directly.)  
  
The project is designed so that you can easily change the creation of sweep signals.  
For example, write your own methods describing how the frequency and amplitude will change from the time of the sweep signal.  
  
The project was created to be able to create various sweep signals: implemented and not implemented by a vibration  
source, from simple ones, like a linear sweep signal, to complex ones, like a pseudo-random sweep signal.
  
Tools were written with the help of which unrealizable sweep signals could be made realizable. The tools are in the "tools" folder.  
  
In addition to them, the project contains the `example` folder, which contains examples of the implementation of various sweep signals.  
The folder contains the following examples:  
* Leanear sweep signal.
* Adaptive sweep signal.  
* Pseudorandom sweep signal.  
* Pseudorandom sweep signal built using m-sequence. 

- - -
## Using the library. 

Проект является библиотекой или пакетом. Работа с ним происходит, как и с другими сторонними библиотеками языка python.
Пример как подключить библиотеку описан здесь. 

- - -
## Описание методов для построения свип сигналов.

Добавление фазы сигналу.


- - -
## Пример работы с пакетом.
  
Ниже приведен простой пример создания свип-сигнала и его визуализации.  
Более расширенное описание работы библиотеки в файле manual.ipynb. 
Остальные примеры содержатся в папке examples.

```
import numpy as np
import matplotlib.pyplot as plt

from math_signals.math_uncalcsweep import UncalculatedSweep

T = 50
dt = 0.01
time = np.linspace(0, T, int(T/dt)+1)

usw = UncalculatedSweep(t=time)
sw = usw()

t_sw, a_sw = sw.get_data()
plt.plot(t_sw, a_sw)
plt.xlabel('Time, s')
plt.ylabel('Amplitude')
plt.title('Sweep-signal')
```python  

![sweep_with_matplotlib](https://user-images.githubusercontent.com/89973180/156033978-ccc8de40-9f6b-4bb1-b59f-7a3ea41d2f64.png "Linear Sweep") 

или используя для визуализации пакет ```viewrelation.view``` по умолчанию, основанный на использовании библиотек ipywidget и bokeh  

```
from compose_signals.c_sweep import ComposedSweep
from viewrelation.view import get_viewer_ipywidgets_bokeh
c_sw = ComposedSweep(sw)
bokeh_view = get_viewer_ipywidgets_bokeh()
bokeh_view.add(c_sw)
bokeh_view.show()
```python

![sweep_with_ipywidgets_bokeh](https://user-images.githubusercontent.com/89973180/156037232-c3b11ec4-f653-44a2-be20-ec87f481d9b7.png "Linear Sweep GUI")