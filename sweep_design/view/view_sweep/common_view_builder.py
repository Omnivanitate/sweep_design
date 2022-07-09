from typing import Type, Union

from ...named_signals.named_signal import NamedSignal
from ...named_signals.named_sweep import NamedSweep

from ..base_view.abc_common_framer_grapher.figure import CommonFigure, CommonFigureMaker
from ..base_view.abc_common_framer_grapher.frame import CommonFrameMaker

from .controller import InteracterPlotViewSweep


class NotCorrectDataError(Exception):
    pass


class CommonVeiwSweepBuilder:
    def __init__(
        self,
        grapher: Type[CommonFigureMaker],
        framer: Type[CommonFrameMaker[CommonFigure, InteracterPlotViewSweep]],
        properties_signal_figure,
        properties_signal_frame,
        properties_checkbox_signals_frame,
        properties_freq_amplitude_figure,
        properties_freq_amplitude_frame,
        properties_freq_phase_figure,
        properties_freq_phase_frame,
        properties_sweep_figure,
        properties_sweep_frame,
        properties_spectrogram_figure,
        properties_spectrogram_frame,
        properties_dropdown_images_spectrogram_frame,
        properties_envelop_figure,
        properties_envelop_frame,
        properties_checkbox_sweep_frame,
    ) -> None:

        self._grapher = grapher()
        self._controller = InteracterPlotViewSweep()

        signal_figure = grapher.get_figure(properties_signal_figure)
        self._signal_frame = framer.get_figure_frame(
            signal_figure, properties_signal_frame
        )

        self._checkbox_signals_frame = framer.get_checkbox_frame(
            properties_checkbox_signals_frame, self._controller
        )

        spectrum_amplitude_figure = grapher.get_figure(properties_freq_amplitude_figure)
        self._spectrum_amplitude_frame = framer.get_figure_frame(
            spectrum_amplitude_figure, properties_freq_amplitude_frame
        )

        spectrum_phase_figure = grapher.get_figure(properties_freq_phase_figure)
        self._spectrum_phase_frame = framer.get_figure_frame(
            spectrum_phase_figure, properties_freq_phase_frame
        )

        sweep_figure = grapher.get_figure(properties_sweep_figure)
        self._sweep_frame = framer.get_figure_frame(
            sweep_figure, properties_sweep_frame
        )

        spectrogram_images_figure = grapher.get_figure(properties_spectrogram_figure)
        self._spectrogram_images_frame = framer.get_figure_frame(
            spectrogram_images_figure, properties_spectrogram_frame
        )

        self._dropdown_images_spectrogram = framer.get_dropdown_frame(
            properties_dropdown_images_spectrogram_frame, self._controller
        )

        envelop_images_figure = grapher.get_figure(properties_envelop_figure)
        self._envelop_frame = framer.get_figure_frame(
            envelop_images_figure, properties_envelop_frame
        )

        self._checkbox_sweep_frame = framer.get_checkbox_frame(
            properties_checkbox_sweep_frame, self._controller
        )

        spectrum_section = self._spectrum_amplitude_frame.h_add(
            self._spectrum_phase_frame
        )
        result_frame = self._signal_frame.v_add(spectrum_section)
        result_frame = result_frame.h_add(self._checkbox_signals_frame)
        sweep_section = (
            self._sweep_frame.v_add(self._dropdown_images_spectrogram)
            .v_add(self._spectrogram_images_frame)
            .v_add(self._envelop_frame)
            .h_add(self._checkbox_sweep_frame)
        )

        result_frame = result_frame.v_add(sweep_section)

        self._result_frame = result_frame

        self._controller.set_controlled_object(
            self._signal_frame,
            self._checkbox_signals_frame,
            self._spectrum_amplitude_frame,
            self._spectrum_phase_frame,
            self._sweep_frame,
            self._dropdown_images_spectrogram,
            self._spectrogram_images_frame,
            self._envelop_frame,
            self._checkbox_sweep_frame,
        )

    def add(self, data: Union[NamedSignal, NamedSweep]):

        line_properties = self._grapher.get_next_line_properties()
        checkbox_properties = {"color": line_properties["line_color"]}
        image_properties = self._grapher.get_next_image_properties()

        name = str(data)

        if isinstance(data, NamedSweep):
            self._sweep_frame.get_figure().add_line(
                *data.get_data(), name, None, line_properties
            )

            spectrogram_figure = self._spectrogram_images_frame.get_figure()

            s = data.spectrogram
            spectrogram_figure.add_image(
                s.time, s.frequency, s.spectrogram_matrix, name, None, image_properties
            )
            spectrogram_figure.add_line(
                *data.f_t.get_data(), name, None, line_properties
            )
            self._dropdown_images_spectrogram.add_choise(name)

            self._envelop_frame.get_figure().add_line(
                *data.a_t.get_data(), name, None, line_properties
            )
            self._checkbox_sweep_frame.add_choise(
                name, None, checkbox_properties, self._controller
            )

        elif isinstance(data, NamedSignal):

            self._signal_frame.get_figure().add_line(
                *data.get_data(), name, None, line_properties
            )
            self._checkbox_signals_frame.add_choise(
                name, None, checkbox_properties, self._controller
            )

        else:
            raise NotCorrectDataError

        amplitude_spectrum = data.get_amplitude_spectrum(name=name)
        self._spectrum_amplitude_frame.get_figure().add_line(
            *amplitude_spectrum.get_data(),
            str(amplitude_spectrum),
            None,
            line_properties
        )
        phase_spectrum = data.get_phase_spectrum(name=name)
        self._spectrum_phase_frame.get_figure().add_line(
            *phase_spectrum.get_data(), str(phase_spectrum), None, line_properties
        )

    def show(self):
        return self._result_frame.get_output()
