import numpy as np
from scipy.spatial.transform import Rotation
import sys
from ..geom.pbc import distance_pbc, distance_pbc2
from tqdm import tqdm

def insert_point_into_shape(
    shape, points, system_size, mol_size, mol_id,
    insertion_limit = int(1e5),
    package = 0.4
):
    overlap = True
    insertion_counter = 0

    if not mol_id:
        return shape.generate_point()

    while overlap and (insertion_counter < insertion_limit):
        insertion_counter += 1

        if 5 * insertion_counter % insertion_limit == 0:
            print(f'Please, wait ... mol #{mol_id} is tried to be inserted\n')

        new_point = shape.generate_point()
        overlap = np.sum(
            # Что насчет квадрата тут???
            distance_pbc2(new_point, points, system_size) < \
            ((2 - insertion_counter / insertion_limit) * package * mol_size)
        )

    if insertion_counter > insertion_limit:
        sys.exit('Decrease package')

    return new_point

def find_position(
    structure, new_point, mol, mol_id,
    rotation_limit = 10,
    min_dist2 = 0.08**2
):
    overlap = True
    rotation_counter = 0

    if not mol_id:
        new_mol = mol.copy()
        new_mol = new_mol.set_XYZ(rotate_random(new_mol.get_XYZ()) + new_point)

        return new_mol

    while overlap and (rotation_counter < rotation_limit):
        # overlap = False
        rotation_counter += 1

        new_mol = mol.copy()
        new_mol = new_mol.set_XYZ(rotate_random(new_mol.get_XYZ()) + new_point)

        for atom in new_mol.get_XYZ():
            overlap = np.all(distance_pbc2(atom, structure.get_XYZ(), structure.box) < min_dist2)
            if overlap:
                break

    return new_mol

def rotate_random(xyz):
    theta = np.random.random(3)* 2 * np.pi
    rot = Rotation.from_euler('xyz', theta)
    new_xyz = rot.apply(xyz.copy())

    return new_xyz
