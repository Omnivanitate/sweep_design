from typing import Dict, Any
import logging

from viewrelation.commonview.protocols.inputdataprotocols import ViewRelation, ViewSignal, ViewSpectrum, ViewSweep
from viewrelation.commonview.viewbuilder import ViewBuilder


class View:
    '''
    The view for a data described by relations, signals, spectrums and sweep-signals.

    '''
    def __init__(self, base_view: ViewBuilder) -> None:
        self.property_object_id = {}
        self.base_view = base_view

    def add_relation(self, relation_entity: ViewRelation, 
            line_properties: Dict[str, Any] = None, group: Any = None) -> None:

        self.base_view.add_line(relation_entity, line_properties, group)

    def add_spectrum(self, spectrum_entity: ViewSpectrum, 
            line_properties: Dict[str, Any] = None, group: Any = None) -> None:

        self.add_relation(spectrum_entity.get_amp_spectrum(), 
                        line_properties, group)
        self.add_relation(spectrum_entity.get_phase_spectrum(), 
                        line_properties, group)

    def add_signal(self, signal_entity: ViewSignal, 
            line_properties: Dict[str, Any] = None, group: Any = None) -> None:

        self.add_relation(signal_entity, line_properties, group)
        self.add_spectrum(signal_entity.get_spectrum(), line_properties, group)
    
    def add_sweep(self, sweep_entity: ViewSweep, line_properties: Dict[str, Any] = None,
                image_properties: Dict[str, Any] = None, group: Any = None) -> None:
        self.add_signal(sweep_entity, line_properties, group)
        self.add_relation(sweep_entity.f_t, line_properties, group)
        self.add_relation(sweep_entity.a_t, line_properties, group)
        self.base_view.add_image(sweep_entity.spectrogram, image_properties)

    def add(self, relation_entity: ViewRelation, line_properties: Dict[str, Any] = None,
            image_properties: Dict[str, Any] = None) -> None:
        '''
        Append any data of relation entity to the view.
        
        line_properties will applay to lines related to that relation entity.
        (For instance, for a signal, this would apply to the line of amplitude 
        spectrum.)
        
        '''
        group = id(relation_entity)
        
        if line_properties is None:
            line_properties = self.base_view.grapher.get_next_line_properties()

        if image_properties is None:
            image_properties = self.base_view.grapher.get_image_properties()

        logging.debug(f"Add relation entity {relation_entity}")
        if isinstance(relation_entity, ViewSweep):
            self.add_sweep(relation_entity, line_properties, image_properties, group)
        elif isinstance(relation_entity, ViewSignal):
            self.add_signal(relation_entity, line_properties, group)
        elif isinstance(relation_entity, ViewSpectrum):
            self.add_spectrum(relation_entity, line_properties, group)
        elif isinstance(relation_entity, ViewRelation):
            self.add_relation(relation_entity, line_properties, group)
        else:
            logging.warning(f"Wrong input of add {relation_entity}")
    
    def show(self):
        return self.base_view.show()
