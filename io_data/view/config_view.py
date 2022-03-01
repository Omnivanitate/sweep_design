signal_window = {
    'width': 1000,
    'height': 300,
    'title': 'Signal',
    'x_axis_label': 'Time, s',
    'y_axis_label': 'Amplitude'
}

spectrum_window_amp = {
    'width': 1000,
    'height': 300,
    'title': 'Amplitude spectrum',
    'x_axis_label': 'Frequency, Hz',
    'y_axis_label': 'Amplitude'
}

spectrum_window_phase = {
    'width': 1000,
    'height': 300,
    'title': 'Phase spectrum',
    'x_axis_label': 'Frequency, Hz',
    'y_axis_label': 'Phase'
}

sweep_window = {
    'width': 1000,
    'height': 300,
    'title': 'Sweep',
    'x_axis_label': 'Time, s',
    'y_axis_label': 'Amplitude'
}

spectrogramma_window = {
    'width': 1000,
    'height': 300,
    'title': 'Speectrogram',
    'x_axis_label': 'Time, s',
    'y_axis_label': 'Frequency, Hz'
}

f_t_window = {
    'width': 1000,
    'height': 300,
    'title': 'Frequency modulation',
    'x_axis_label': 'Time, s',
    'y_axis_label': 'Frequency, Hz'
}

a_t_window = {
    'width': 1000,
    'height': 300,
    'title': 'Amplitude modulation',
    'x_axis_label': 'Time, s',
    'y_axis_label': 'Amplitude'
}

default_categories = {
    'spectrum_amp': spectrum_window_amp,
    'spectrum_phase': spectrum_window_phase,
    'signal': signal_window,
    'sweep': sweep_window,
    'spectrogram': spectrogramma_window,
    'f_t': f_t_window,
    'a_t': a_t_window,
}

default_categories_layout = [
    ['signal'],
    ['spectrum_amp'],
    ['spectrum_phase'],
    ['sweep'],
    ['dropdown'],
    ['spectrogram'],
    ['f_t'],
    ['a_t'],
]
