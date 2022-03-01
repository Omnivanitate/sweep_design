from scipy.io import savemat

from math_signals.math_relation import Relation


def save_mat(file_name: str, signal: Relation) -> None:
    x, y = signal.get_data()
    data = {'t': x, 'F': y}
    savemat(file_name, data)
