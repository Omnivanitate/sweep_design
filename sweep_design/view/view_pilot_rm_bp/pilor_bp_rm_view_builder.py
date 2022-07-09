from typing import Any, Dict

import numpy as np

from ..base_view.abc_common_framer_grapher.frame import CommonFrameMaker
from ..base_view.abc_common_framer_grapher.figure import CommonFigureMaker, CommonFigure

from ..view_pilot_rm_bp.controller import InteracterPilotRmBp


class PilotRmBpViewBuilder:
    def __init__(
        self,
        grapher: CommonFigureMaker,
        framer: CommonFrameMaker[CommonFigure, InteracterPilotRmBp],
        properties_freq_amp_frame: Dict[str, Any],
        properties_freq_amp_figure: Dict[str, Any],
        properties_freq_phase_frame: Dict[str, Any],
        properties_freq_phase_figure: Dict[str, Any],
        properties_checkbox_signals_frame: Dict[str, Any],
        properties_checkbox_type_signals_frame: Dict[str, Any],
        properties_main_sweep_frame: Dict[str, Any],
        properties_main_sweep_figure: Dict[str, Any],
        properties_dropdown_images_spectrogram_frame: Dict[str, Any],
        properties_spectrogram_frame: Dict[str, Any],
        properties_spectrogram_figure: Dict[str, Any],
    ) -> None:

        controller = InteracterPilotRmBp()

        spectrum_amplitude_figure = grapher.get_figure(properties_freq_amp_figure)
        self._spectrum_amp_frame = framer.get_figure_frame(
            spectrum_amplitude_figure, properties_freq_amp_frame
        )

        spectrum_phase_figure = grapher.get_figure(properties_freq_phase_figure)
        self._spectrum_phase_frame = framer.get_figure_frame(
            spectrum_phase_figure, properties_freq_phase_frame
        )

        self._checkbox_signals_frame = framer.get_checkbox_frame(
            properties_checkbox_signals_frame, controller
        )
        self._checkbox_types_signals_frame = framer.get_checkbox_frame(
            properties_checkbox_type_signals_frame, controller
        )

        main_sweep_figure = grapher.get_figure(properties_main_sweep_figure)
        self._main_sweep_frame = framer.get_figure_frame(
            main_sweep_figure, properties_main_sweep_frame
        )

        self._dropdown_images_spectrogram = framer.get_dropdown_frame(
            properties_dropdown_images_spectrogram_frame, controller
        )

        spectrogram_images_figure = grapher.get_figure(properties_spectrogram_figure)
        self._spectrogram_images_frame = framer.get_figure_frame(
            spectrogram_images_figure, properties_spectrogram_frame
        )

        result_frame = self._spectrum_amp_frame.h_add(self._spectrum_phase_frame)
        checkbox_section = self._checkbox_signals_frame.h_add(
            self._checkbox_types_signals_frame
        )
        result_frame = result_frame.v_add(checkbox_section)
        result_frame = result_frame.v_add(self._main_sweep_frame)
        result_frame = result_frame.v_add(self._dropdown_images_spectrogram)
        result_frame = result_frame.v_add(self._spectrogram_images_frame)

        self._result_frame = result_frame

        controller.set_controled_objects(
            self._dropdown_images_spectrogram,
            self._main_sweep_frame,
            self._spectrum_amp_frame,
            self._spectrum_phase_frame,
            self._spectrogram_images_frame,
            self._checkbox_signals_frame,
            self._checkbox_types_signals_frame,
        )

        self._controller = controller

    def add_amp_spectrum(
        self,
        frequency: np.ndarray,
        amp_spectrum: np.ndarray,
        name: str,
        group: str,
        line_properties: Dict[str, Any],
    ) -> None:
        figure = self._spectrum_amp_frame.get_figure()
        figure.add_line(frequency, amp_spectrum, name, group, line_properties)

    def add_phase_sepctrum(
        self,
        frequency: np.ndarray,
        phase_spectrum: np.ndarray,
        name: str,
        group: str,
        line_properties: Dict[str, Any],
    ) -> None:

        figure = self._spectrum_phase_frame.get_figure()
        figure.add_line(frequency, phase_spectrum, name, group, line_properties)

    def add_choise_sweep(
        self, choise_name: str, group: str, choise_properties: Dict[str, Any]
    ) -> None:

        self._checkbox_signals_frame.add_choise(
            choise_name, group, choise_properties, self._controller
        )

    def add_choise_type_signal(
        self, choise_name: str, group: str, choise_properties: Dict[str, Any]
    ) -> None:
        self._checkbox_types_signals_frame.add_choise(
            choise_name, group, choise_properties, self._controller
        )

    def add_main_sweep_signals(
        self,
        time: np.ndarray,
        amplitude: np.ndarray,
        name: str,
        group: str,
        line_properties: Dict[str, Any],
    ) -> None:

        figure = self._main_sweep_frame.get_figure()
        figure.add_line(time, amplitude, name, group, line_properties)

    def add_choise_dropdown_spectrogram(self, choise_name: str) -> None:
        self._dropdown_images_spectrogram.add_choise(choise_name)

    def add_line_spectrogram(
        self,
        time_spectrogram: np.ndarray,
        frequency_spectrogram: np.ndarray,
        line_name: str,
        group: str,
        line_properties: Dict[str, Any],
    ) -> None:

        figure = self._spectrogram_images_frame.get_figure()
        figure.add_line(
            time_spectrogram, frequency_spectrogram, line_name, group, line_properties
        )

    def add_image_spectrogram(
        self,
        time: np.ndarray,
        frequency: np.ndarray,
        spectrogram: np.ndarray,
        name: str,
        group: str,
        image_properties: Dict[str, Any],
    ) -> None:

        figure = self._spectrogram_images_frame.get_figure()
        figure.add_image(time, frequency, spectrogram, name, group, image_properties)

    def show(self) -> Any:
        return self._result_frame.get_output()
