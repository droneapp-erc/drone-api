import numpy as np
from scipy.interpolate import RegularGridInterpolator


def read_values_from_file(file_path):
    matrix = []
    with open(file_path, "r") as file:
        for line in file:
            row = line.strip().split()
            row_float = [float(value) for value in row]
            matrix.append(row_float)
    return matrix


def calculate(illuminance: str, area: float):
    def distance_vs_velocity(distance):
        return area / distance

    area /= 0.779942  # area를 0.779942로 나누기

    dist = np.arange(1, 10.01, 1)
    vel = np.arange(0, 1.001, 0.1)

    segmented_dist = np.arange(1, 10.01, 0.1)

    file_path = "data/" + illuminance + ".txt"

    trueValues = np.array(read_values_from_file(file_path))
    interp_func = RegularGridInterpolator((vel, dist), trueValues, method="cubic")
    min_interp_value = float("inf")
    min_segmented_dist = None
    for distance in segmented_dist:
        velocity = distance_vs_velocity(distance)
        xi = [[velocity, distance]]
        try:
            interp_value = interp_func(xi)[0]
            if interp_value < min_interp_value:
                min_interp_value = interp_value
                min_segmented_dist = distance
        except ValueError:
            pass
    rounded_dist = round(min_segmented_dist)
    rounded_velocity = round(distance_vs_velocity(min_segmented_dist), 1)
    file_path_opt = "data/opt" + illuminance + ".txt"
    optValues = np.array(read_values_from_file(file_path_opt))
    result = []
    column_index = None
    for i in range(optValues.shape[1]):
        column = optValues[:, i]
        if rounded_dist == column[1] and rounded_velocity == column[0]:
            column_index = i
            break
    result = optValues[:, column_index] if column_index is not None else []
    if not isinstance(result, list):
        result = list(result)
    return result
