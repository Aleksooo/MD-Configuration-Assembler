import numpy as np


def delta_pbc(box_size: np.array, point: np.array, points: np.array) -> np.array:
    delta = points - point
    idx_pbc = np.abs(delta) * 2 > box_size
    delta -= np.sign(delta) * box_size * idx_pbc
    return delta


def distance_pbc2(box_size: np.array, point1: np.array, points: np.array) -> np.array:
    return np.sum(delta_pbc(box_size, point1, points)**2, axis=1)


def distance_pbc(box_size: np.array, point1: np.array, points: np.array) -> np.array:
    return np.sqrt(distance_pbc2(box_size, point1, points))


def apply_pbc_point(box_size: np.array, points: np.array):
    points_pbc = points.copy()
    half_box_size = box_size/2
    for i in range(3):
        idx_pbc = abs(points[:, i] - half_box_size[i]) > half_box_size[i]
        points_pbc[idx_pbc, i] -= box_size[i] * np.sign(points[idx_pbc, i])


    return points_pbc

