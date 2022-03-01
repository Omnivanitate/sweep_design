'''viewrelation.

В модуле написана функция get_view, которая возращает экземпляр класса 
View, в коструктор, которого передан экземпляр класса ViewBuilder.
Для экземпляра класса ViewBuilder переданы параметры grafer и frame, 
представленные эземплярами классов BokehFigureMaker и WidgetFrameMaker
с параметрами по умолчанию. 

Экземпляр переменной framer, отвечает за создание рамок для изображений
и за то, как они будут распологаться на экране.  

Экземпляр класса заданный для переменной grapher отвечет за создание   
полотна, на котором будут происходить отображение линий и различной 
графики, и которое связано с рамкой, в которой оно расположен. 

Классы BokehFigureMaker и WidgetFrameMaker написаны для визуализации графиков 
в jupyter notebook, jupyter lab и др. 
В зависимости от редактора возможно некорректное отображение (Например в VSCode).

WidgetFrameMaker использует для построения структуры расположения 
изображения и элементов взаимодействия библиотеку ipywidgets
https://ipywidgets.readthedocs.io/

BokehFigureMaker использует для построения изображения библиотеку bokeh
https://bokeh.org/
и для свизи со структурой используется библиотека ipywidgets

Можно написать собственне классы для построния структуры, описывающей как будут 
распологаться изображения, какие элементы взаимодействи будут применены и
какие библиотеки будут использоваться для этого. 
Можно написать свои классы для визулизации, как будут оформлены и какие 
библотеки для этого бдут использоваться. 

Други примеры для streamlit, matplotlib, как и для ipywidgets и bokeh,
можно найти в данном модуле в папке framemakers

'''
from viewrelation.commonview.viewbuilder import ViewBuilder
from viewrelation.commonview.view import View
from viewrelation.framemakers.ipywidgetframer.ipywidgetframe import WidgetFrameMaker
from viewrelation.framemakers.ipywidgetframer.figwidget.bokehfig import BokehFigureMaker

base_view: ViewBuilder = ViewBuilder(BokehFigureMaker(), WidgetFrameMaker())

def get_viewer_ipywidgets_bokeh():
    return View(base_view=base_view)
