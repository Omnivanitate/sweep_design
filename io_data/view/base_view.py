import logging
import copy

from compose_signals.c_relation import ComposedRelation
from compose_signals.c_signal import ComposedSignal, ComposedSpectrum
from compose_signals.c_sweep import ComposedSweep

from io_data.view.widget_pyplot_view import IpywidgetsMatplotlibView

class ViewData:

    def __init__(self, base_view=IpywidgetsMatplotlibView()) -> None:
        self.property_object_id = {}
        self.base_view = base_view  # type: IpywidgetsMatplotlibView

    def add(self, relation_entity: ComposedRelation, entity_property: dict = None):
        
        logging.debug('Add reletion entity %s', relation_entity)
        
        if id(relation_entity) not in list(self.property_object_id.keys()):
            if entity_property is None:
                entity_property = copy.deepcopy(
                    self.base_view.defualt_entity_property)

            if entity_property['color'] is None:
                entity_property['color'] = self.base_view.get_next_color()

            self.property_object_id.update(
                {id(relation_entity): entity_property})

        else:
           
            return
            # entity_property = self.property_object_id[id(relation_entity)]

        if not isinstance(relation_entity, ComposedSpectrum):
            self.base_view.add_line(relation_entity, entity_property)

        if isinstance(relation_entity, ComposedSignal):
            self.add(relation_entity.get_spectrum(), entity_property)

        if isinstance(relation_entity, ComposedSweep):
            self.base_view.add_image(relation_entity.spectrogram, str(relation_entity),
                                     entity_property)
            self.add(relation_entity.f_t, entity_property)
            self.add(relation_entity.a_t, entity_property)

        if isinstance(relation_entity, ComposedSpectrum):
           
            self.add(relation_entity.get_phase_spectrum(), entity_property)
            self.add(relation_entity.get_amp_spectrum(), entity_property)

    def show(self) -> None:
        return self.base_view.show()
