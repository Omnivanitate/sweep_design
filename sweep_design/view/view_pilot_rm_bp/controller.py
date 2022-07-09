from typing import Dict

from ..base_view.abc_common_framer_grapher.figure import CommonFigure
from ..base_view.abc_common_framer_grapher.frame import (
    CommonCheckBoxFrame,
    CommonDropdownFrame,
    CommonFigureFrame,
)


class InteracterPilotRmBp:
    def __init__(
        self,
        dropdown_spectrogram_frame: CommonDropdownFrame = None,
        signal_figure_frame: CommonFigureFrame[CommonFigure] = None,
        amp_spectrum_figure_frame: CommonFigureFrame[CommonFigure] = None,
        phase_spectrum_figure_frame: CommonFigureFrame[CommonFigure] = None,
        spectogramma_figura_frame: CommonFigureFrame[CommonFigure] = None,
        checkbox_signal_frame: CommonCheckBoxFrame[CommonFigure] = None,
        checkbox_type_signal_frame: CommonCheckBoxFrame[CommonFigure] = None,
    ) -> None:
        self._dropdown_spectrogram_frame = dropdown_spectrogram_frame
        self._signal_figure_frame = signal_figure_frame
        self._amp_spectrum_figure_frame = amp_spectrum_figure_frame
        self._phase_spectrum_figure_frame = phase_spectrum_figure_frame
        self._spectogram_figura_frame = spectogramma_figura_frame
        self._checkbox_signals_frame = checkbox_signal_frame
        self._checkbox_types_signals_frame = checkbox_type_signal_frame

    def set_controled_objects(
        self,
        dropdown_spectrogram_frame: CommonDropdownFrame,
        signal_figure_frame: CommonFigureFrame,
        amp_spectrum_figure_frame: CommonFigureFrame[CommonFigure],
        phase_spectrum_figure_frame: CommonFigureFrame[CommonFigure],
        spectogramma_figura_frame: CommonFigureFrame[CommonFigure],
        checkbox_signal_frame: CommonCheckBoxFrame[CommonFigure],
        checkbox_type_signal_frame: CommonCheckBoxFrame[CommonFigure],
    ) -> None:
        self._dropdown_spectrogram_frame = dropdown_spectrogram_frame
        self._signal_figure_frame = signal_figure_frame
        self._amp_spectrum_figure_frame = amp_spectrum_figure_frame
        self._phase_spectrum_figure_frame = phase_spectrum_figure_frame
        self._spectogram_figura_frame = spectogramma_figura_frame
        self._checkbox_signals_frame = checkbox_signal_frame
        self._checkbox_types_signals_frame = checkbox_type_signal_frame

    def widget_notify(self, obj):
        def listner(value: Dict):
            if obj in self._checkbox_signals_frame.get_checkboxs().values():
                self._call_checkbox_signal(obj.get_name(), value["new"])

            if obj in self._checkbox_types_signals_frame.get_checkboxs().values():
                self._call_checkbox_type_signal(obj.get_groups(), value["new"])

            if obj is self._dropdown_spectrogram_frame:
                self._call_dropdown_spectrogram_frame(value["new"], True)
                self._call_dropdown_spectrogram_frame(value["old"], False)

        return listner

    def _call_checkbox_signal(self, checkbox_name: str, value: bool) -> None:
        for lines in self._amp_spectrum_figure_frame.get_figure().get_lines_by_groups(
            checkbox_name
        ):
            lines.set_visible(value)

        for lines in self._phase_spectrum_figure_frame.get_figure().get_lines_by_groups(
            checkbox_name
        ):
            lines.set_visible(value)

        for lines in self._signal_figure_frame.get_figure().get_lines_by_groups(
            checkbox_name
        ):
            lines.set_visible(value)

        for lines in self._spectogram_figura_frame.get_figure().get_lines_by_groups(
            checkbox_name
        ):
            lines.set_visible(value)

        for images in self._spectogram_figura_frame.get_figure().get_images_by_groups(
            checkbox_name
        ):
            images.set_visible(value)

            if value:
                self._dropdown_spectrogram_frame.add_choise(images.get_name())
            else:
                self._dropdown_spectrogram_frame.remove_choise(images.get_name())

        name_checkboxes = []
        for checkbox in self._checkbox_types_signals_frame.get_checkboxs().values():
            if checkbox_name in checkbox.get_groups():
                name_checkboxes.append(checkbox.get_name())

        for name in name_checkboxes:
            if value:
                self._checkbox_types_signals_frame.return_choise(name)
            else:
                self._checkbox_types_signals_frame.remove_choise(name)

    def _call_checkbox_type_signal(self, checkbox_name: str, value: str) -> None:

        for lines in self._amp_spectrum_figure_frame.get_figure().get_lines_by_groups(
            checkbox_name
        ):
            lines.set_visible(value)

        for lines in self._phase_spectrum_figure_frame.get_figure().get_lines_by_groups(
            checkbox_name
        ):
            lines.set_visible(value)

        for lines in self._signal_figure_frame.get_figure().get_lines_by_groups(
            checkbox_name
        ):
            lines.set_visible(value)

        for lines in self._spectogram_figura_frame.get_figure().get_lines_by_groups(
            checkbox_name
        ):
            lines.set_visible(value)

    def _call_dropdown_spectrogram_frame(self, image_name: str, value: bool) -> None:
        image = self._spectogram_figura_frame.get_figure().get_image(image_name)
        if image:
            image.set_visible(value)
