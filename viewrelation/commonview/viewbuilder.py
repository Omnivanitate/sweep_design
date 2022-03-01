from typing import Dict, List, Any, Union

from viewrelation.commonview.protocols.inputdataprotocols import ViewRelation, ViewSpectrogram
from viewrelation.commonview.protocols.figureprotocols import FigureMaker, Figure, Line, Image
from viewrelation.commonview.protocols.frameprotocols import FrameMaker, Frame, DropdownFrame, CheckBox

class ViewBuilder:
    '''Класс, помогающий построить отображение результатов.

    Класс ViewBuilder, определяет какой класс будут использоваться для 
    построения структуры расположения окон, которые отображают полотна 
    с графикой, элементы взаимодействия и другое.
    Также он содержит класс, который помогает в построении полотен, на которых 
    будет изображена графика. 

    Параметры:
        grapher: protocols. protocols.figureprotocols.FigureMaker
            Параметр, определяющий используемый класс для построения полотен 
            и их взаимосвязь с элементами, которые их содержат.
        frame: commonview.protocols.frameprotocols.FrameMaker
            Параметр, определяющий используемый класс для построения сетки 
            изображения различных окон (элементы управления, полотена и др.)
         
    '''
    def __init__(self, grapher: FigureMaker, framer: FrameMaker) -> None:

        self.grapher = grapher
        self.framer = framer
        self.categories_properties = self.framer.categories_properties
        self.categories_layout = self.framer.categories_layout
        
        self.elements: Dict[str, VisualCell] = {}

    def get_visual_cell(self, category: str) -> 'VisualCell':
        '''Получить ячеку визуализации.
        
            Извлечь ячейку визуализации из словоря по ключу и вернуть.
            если такого элемента в словаре нет, то создать ячеку и вернуть.
            Параметры: 
                category: str
                    Параметр, определяет к какой категории относятся ячека.
                    
        '''
        if category not in self.elements:
            figure = self.grapher.get_figure(self.categories_properties[category])
            frame = self.framer.get_output_figure(figure, 
                                self.categories_properties[category])
            checkboxs_frame = self.framer.get_output_checkbox('Lines', 
                                self.categories_properties[category])
            frame = frame.h_add(checkboxs_frame)
            element = VisualCell(category, self.framer, frame, 
                                    figure, checkboxs_frame)
            self.elements.update({category:element})

        return self.elements[category]

    def add_line(self, relation_entity: ViewRelation, 
                    line_properties: Dict[str, Any], group: Any) -> None:
        '''Добавить линию к полотну, содержащемся в соответствующей ячейке.

        Параметры:
            relation_entity: ViewRelation 
                Объект, из которого будут извлечена вся
                необходимая инвормация для построения графика линии.
            line_properties: Dict[str, Any]
                Свойства отображаемой линии.
        '''
        element = self.get_visual_cell(relation_entity.category)
        element.add_line(relation_entity, line_properties, group)
        self.bound_elements()

    def add_image(self, image_entity: ViewSpectrogram, 
                                    image_properties: Dict[str, Any]) -> None:
        '''Добавить изображение к полотну, содержащемся в соответствующей ячейке.

        Параметры:
            image_entity: ViewSpectrogram 
                Объект, из которого будут извлечена вся необходимая 
                инвормация для построения изображения.
            image_properties: Dict[str, Any]
                Свойства изображения.
        '''
        element = self.get_visual_cell(image_entity.category)
        if element.dropdown is None:
            self.add_dropdown(element)
        element.add_image(image_entity, image_properties)

    def add_dropdown(self, element: 'VisualCell'):
        element.dropdown = self.framer.get_output_dropdown(element.images)
        element.frame = element.dropdown.v_add(element.frame)

    def bound_elements(self):
        '''Связать объекты, относящиеся к одной и тойже группе.
        
        
        '''
        for element in self.elements.values():
            for checkbox in element.checkboxs.values():
                for element2 in self.elements.values():
                    for line in element2.lines.values():
                        if checkbox.group == line.group:
                            checkbox.add_listener({id(line): line})
                    for checkbox2 in element2.checkboxs.values():
                        if checkbox.group == checkbox2.group:
                            checkbox.add_listener({id(checkbox2): checkbox2})
     
    def show(self) -> Any:
        '''Получить результат отображения.
        
        Возращает объект, отображющий все элементы в соответствии с 
        заданным расположением.
        '''
        return get_output_layout(self.categories_layout, self.elements).output


def get_output_layout(category_layout: List[Union[str, List[str]]], 
                                pre_outs: Dict[str, 'VisualCell']) -> Frame:
        '''Функции возращающая итоговую визуализацию объекта.

        Параметры:
            category_layout: List[Union[str, List[str]]]
                С помощь словоря описывается расположение элементов.
                Славарь, состоящий из строк объединяет элементы горизонтально,
                а состоящий из словорей объединяет элементы вертикально.
        
        '''
        layout_: Frame = None

        if isinstance(category_layout, list):
            for k in category_layout:
                result = get_output_layout(k, pre_outs)
                if layout_ is not None:
                    if result:
                        if isinstance(k, str):
                            layout_ = layout_.h_add(result)
                        else:
                            layout_ = layout_.v_add(result)
                else:
                    layout_ = result
        elif isinstance(category_layout, str):
            if category_layout in pre_outs:
                return pre_outs[category_layout].frame

        return layout_

class VisualCell:
    '''
    
    '''

    def __init__(self, category: str, framer: FrameMaker, frame: Frame, 
                        fig: Figure, checkboxframe: Frame) -> None:
        self.category = category
        self.framer = framer
        self.frame = frame
        self.fig = fig
        self.checkboxframe = checkboxframe
        self.dropdown: DropdownFrame = None
        self.images: Dict[str, Image] = {}
        self.lines: Dict[str, Line] = {}
        self.checkboxs: Dict[str, CheckBox] = {}
          
  
    def add_line(self, relation_entity: ViewRelation, 
                    line_properties: dict, group: Any) -> None:
        '''Добавить линию к полотну, содержащемся в соответствующей ячейке.
       
        Параметры:
            relation_entity: ViewRelation 
                Объект, из которого будут извлечена вся
                необходимая инвормация для построения графика линии.
            line_properties: Dict[str, Any]
                Свойства отображаемой линии.
            group: Any
                Описывает к какой группе относится линия. 
        '''
        name = str(relation_entity)
        line = self.fig.plot_line(*relation_entity.get_data(), 
                                    line_properties, group, name)
        checkbox = self.framer.get_checkbox(name, line.get_color(), group)
        self.lines.update({name: line})
        self.checkboxs.update({name: checkbox})
        self.checkboxframe.add_element(checkbox.checkbox)
    
    def add_image(self, image_entity: ViewSpectrogram,
                     image_properties: Dict['str', Any]) -> None:
        '''Добавить изображение к полотну, содержащемся в соответствующей ячейке.

        Параметры:
            image_entity: ViewSpectrogram 
                Объект, из которого будут извлечена вся необходимая 
                инвормация для построения изображения.
            image_properties: Dict[str, Any]
                Свойства изображения.
        '''
        name = str(image_entity)
        t = image_entity.t
        f = image_entity.f
        S = image_entity.S
        image = self.fig.plot_image(t, f, S, image_properties)
        self.images.update({name:image})
        self.dropdown.add_choise(name)