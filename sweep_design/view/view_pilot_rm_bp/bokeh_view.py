from ...named_signals.named_sweep import NamedSweep

from ..framemakers.ipywidgetframer.default_ipywidget_properties import (
    get_checkbox_frame,
    get_dropdown_frame,
    get_figure_frame,
)

from ..framemakers.ipywidgetframer.figwidget.bokehfig import (
    BokehFigureMaker,
    color_palette,
    default_image_properties,
    default_line_property,
)

from ..framemakers.ipywidgetframer.figwidget.default_bokeh_properties import (
    get_figure_window,
)

from ..framemakers.ipywidgetframer.ipywidgetframe import WidgetFrameMaker
from .pilor_bp_rm_view_builder import PilotRmBpViewBuilder


class PilotRMBPBokehView:
    def __init__(self, k_width=1.0, k_height=1.0) -> None:

        figure_frame_amplitude_phase_spectrum = get_figure_frame(
            k_width * 0.4, k_height * 0.3
        )
        figure_window_amp_spectrum = get_figure_window(
            "Amplitude spectrum",
            "Frequency, Hz",
            "Amlitude, N",
            k_width * 0.4,
            k_height * 0.3,
        )

        figure_window_phase_spectrum = get_figure_window(
            "Phase spectrum", "Frequency, Hz", "Phase", k_width * 0.4, k_height * 0.3
        )

        checkbox_signals_frame = get_checkbox_frame(
            "Signals:", "", k_width * 0.4, k_height * 0.3
        )
        checkbox_types_signals_frame = get_checkbox_frame(
            "Types signals:", "", k_width * 0.4, k_height * 0.3
        )

        figure_frame_main_sweep_spectrogram = get_figure_frame(
            k_width * 0.8, k_height * 0.4
        )
        figure_window_main_sweep = get_figure_window(
            "Sweep", "Time, s", "Force, N", k_width * 0.8, k_height * 0.3
        )

        figure_window_spectrogram = get_figure_window(
            "Spectrum", "Time, s", "Frequency, Hz", k_width * 0.8, k_height * 0.3
        )

        dropdown_spectrogram_frame = get_dropdown_frame(
            "Specrograms:", "No spectrogram!"
        )

        self._view_builder = PilotRmBpViewBuilder(
            BokehFigureMaker,
            WidgetFrameMaker,
            figure_frame_amplitude_phase_spectrum,
            figure_window_amp_spectrum,
            figure_frame_amplitude_phase_spectrum,
            figure_window_phase_spectrum,
            checkbox_signals_frame,
            checkbox_types_signals_frame,
            figure_frame_main_sweep_spectrogram,
            figure_window_main_sweep,
            dropdown_spectrogram_frame,
            figure_frame_main_sweep_spectrogram,
            figure_window_spectrogram,
        )

    def add_pilot_rm_bp(
        self, pilot: NamedSweep, reaction_mass: NamedSweep, base_plate: NamedSweep
    ) -> None:

        line_properties = default_line_property
        line_properties["line_color"] = next(color_palette)

        self._view_builder.add_choise_sweep(
            f"{str(pilot)}_pilot",
            f"{str(pilot)}_pilot",
            {"color": line_properties["line_color"]},
        )

        time_spectrogram, frequency_spectrogram = pilot.f_t.get_data()
        self._view_builder.add_line_spectrogram(
            time_spectrogram,
            frequency_spectrogram,
            str(pilot),
            set([str(pilot), f"{str(pilot)}_pilot"]),
            line_properties,
        )

        for signal in [pilot, reaction_mass, base_plate]:

            self._view_builder.add_choise_type_signal(
                str(signal),
                set([str(signal), f"{str(pilot)}_pilot"]),
                {"color": line_properties["line_color"]},
            )

            frequency, amplitude_spectrum = (
                signal.get_spectrum().get_amp_spectrum().get_data()
            )
            self._view_builder.add_amp_spectrum(
                frequency,
                amplitude_spectrum,
                str(signal),
                set([str(signal), f"{str(pilot)}_pilot"]),
                line_properties,
            )

            frequency_phase, phase_spectrum = (
                signal.get_spectrum().get_phase_spectrum().get_data()
            )
            self._view_builder.add_phase_sepctrum(
                frequency_phase,
                phase_spectrum,
                str(signal),
                set([str(signal), f"{str(pilot)}_pilot"]),
                line_properties,
            )

            time, amplitude = signal.get_data()
            self._view_builder.add_main_sweep_signals(
                time,
                amplitude,
                str(signal),
                set([str(signal), f"{str(pilot)}_pilot"]),
                line_properties,
            )

            spectrogram = signal.spectrogram
            time_spectrogram, frequency_spectrogram, spectrogram = (
                spectrogram.time,
                spectrogram.frequency,
                spectrogram.spectrogram_matrix,
            )

            self._view_builder.add_image_spectrogram(
                time_spectrogram,
                frequency_spectrogram,
                spectrogram,
                str(signal),
                set([str(signal), str(pilot), f"{str(pilot)}_pilot"]),
                default_image_properties,
            )
            self._view_builder.add_choise_dropdown_spectrogram(str(signal))
            line_properties["line_color"] = next(color_palette)

    def show(self):
        return self._view_builder.show()


def get_pilot_rm_bp_view_bokeh_ipywidget(k_width=1.0, k_height=1.0):
    return PilotRMBPBokehView(k_width, k_height)
