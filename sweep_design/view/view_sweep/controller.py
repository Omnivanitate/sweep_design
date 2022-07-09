from typing import Dict, Union

from ..base_view.abc_common_framer_grapher.figure import CommonFigure
from ..base_view.abc_common_framer_grapher.frame import (
    CommonCheckBox,
    CommonCheckBoxFrame,
    CommonDropdownFrame,
    CommonFigureFrame,
)

from ..base_view.abc_common_framer_grapher.controller import CommonController


class InteracterPlotViewSweep(CommonController):
    def __init__(self) -> None:
        self._signal_frame = None
        self._checkbox_signals_frame = None
        self._spectrum_amplitude_frame = None
        self._spectrum_phase_frame = None
        self._sweep_frame = None
        self._spectrogram_dropdown_frame = None
        self._spectrogram_images_frame = None
        self._envelop_frame = None
        self._checkbox_sweep_frame = None

    def set_controlled_object(
        self,
        signal_frame: CommonFigureFrame[CommonFigure],
        checkbox_signals_frame: CommonCheckBoxFrame,
        spectrum_amplitude_frame: CommonFigureFrame[CommonFigure],
        spectrum_phase_frame: CommonFigureFrame[CommonFigure],
        sweep_frame: CommonFigureFrame[CommonFigure],
        spectrogram_dropdown_frame: CommonDropdownFrame,
        spectrogram_images_frame: CommonFigureFrame[CommonFigure],
        envelop_frame: CommonFigureFrame[CommonFigure],
        checkbox_sweep_frame: CommonCheckBoxFrame,
    ) -> None:
        self._signal_frame = signal_frame
        self._checkbox_signals_frame = checkbox_signals_frame
        self._spectrum_amplitude_frame = spectrum_amplitude_frame
        self._spectrum_phase_frame = spectrum_phase_frame
        self._sweep_frame = sweep_frame
        self._spectrogram_dropdown_frame = spectrogram_dropdown_frame
        self._spectrogram_images_frame = spectrogram_images_frame
        self._envelop_frame = envelop_frame

        self._checkbox_sweep_frame = checkbox_sweep_frame

    def widget_notify(self, obj: Union[CommonCheckBox, CommonDropdownFrame]):
        def listner(value: Dict):
            if isinstance(obj, CommonCheckBox):
                self._set_line_by_checkbox(obj, value["new"])
                self._spectrogram_dropdown_frame
            if obj is self._spectrogram_dropdown_frame:
                self._set_image_spectrogram(value["new"], True)
                self._set_image_spectrogram(value["old"], False)

        return listner

    def _set_line_by_checkbox(self, check_box: CommonCheckBox, value: bool) -> None:
        fig_frames = [
            self._signal_frame,
            self._spectrum_amplitude_frame,
            self._spectrum_phase_frame,
            self._sweep_frame,
            self._spectrogram_images_frame,
            self._envelop_frame,
        ]
        for fig_frame in fig_frames:
            line = fig_frame.get_figure().get_line(check_box.get_name())
            if line:
                line.set_visible(value)

    def _set_image_spectrogram(self, image_name: str, value: bool) -> None:
        image = self._spectrogram_images_frame.get_figure().get_image(image_name)
        if image:
            image.set_visible(value)
