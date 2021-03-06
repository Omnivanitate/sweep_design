# Проект по разработке свип-сигналов.
  
- - -  

Пакет написан на языке **Python** для создания и разработки свип-сигналов различной сложности.  
  
Пакет содержит не только инструменты для создания, но и инструменты для анализа, визуализации и других целей. 
    
Проект может быть использовании как в обучающих целях, так и производственных.  
  
Для быстроты разработки сигналов, для сопоставления их параметров с другими сигналами, для  
их визуализации удобно использовать `Jupyter Lab` или `Jupyter Notebook`.  
Для визуализации графиков проект содержит соответствующие этим задачам пакеты.  
(В редакторах кода или IDE, таких как vscode, построение изображений, графиков возможно не корректно.  
Лучше использовать напрямую `Jupyter Lab`.)  
  
Проект создан так, чтобы можно было легко менять создание свип-сигналов.   
Например, написать свои методы описывающие, как будет изменяется частота и амплитуда от времени свип-сигнала.  
  
Проект создан для возможности создавать различные свип сигналы: реализуемые и не реализуемые вибрационным источником,  
от простых, как линейный свип-сигнал, до сложных, как псевдослучайный свип-сигнал. Написаны инструменты с помощью,  
которых, из нереализуемых свип-сигналов можно было сделать реализуемые. Инструменты содержаться в папке `tools`.  
  
Кроме них проект содержит папку `example`, которая содержит примеры реализации различных свип-сигналов.  
В папке содержаться следующие примеры:  
* Линейный свип-сигнала.  
* Адаптивный свип-сигнал.
* Псевдослучайный спип-сигнал.  
* Псевдослучайный свип-сигнал, построенный с использованием m-последовательности. 

- - -
## Использование библиотеки. 

Проект является библиотекой или пакетом. Работа с ним происходит, как и с другими сторонними библиотеками языка python.
Пример как подключить библиотеку описан 
[здесь](https://all-python.ru/osnovy/podklyuchenie-modulej.html 'Import module') 
и на [английском] (https://docs.python.org/3/tutorial/modules.html) языке. 
- - -
## Описание методов для построения свип сигналов.

Добавление фазы к сигналу.
Вычитание фазы из сигнала.
Получение спектра.
Получение амплиткдного спетра.
Получение фазагого спектра.
Получение обратного фильтра.

и др.

- - -
## Пример работы с пакетом.
  
Ниже приведен простой пример создания свип-сигнала и его визуализации.  
Более расширенное описание работы библиотеки в файле manual.ipynb. 
Остальные примеры содержатся в папке examples.

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

или используя для визуализации пакет ```viewrelation.view```, по умолчанию основанный на использовании библиотек ipywidget и bokeh  

```python
from sweep_design import NamedSweep
from sweep_design.view import get_view_sweep_bokeh_ipywidget

c_sw = NamedSweep(sw)
bokeh_view = get_view_sweep_bokeh_ipywidget()
bokeh_view.add(c_sw)
bokeh_view.show()
```

![sweep_with_ipywidgets_bokeh](https://user-images.githubusercontent.com/89973180/156037232-c3b11ec4-f653-44a2-be20-ec87f481d9b7.png "Linear Sweep GUI")