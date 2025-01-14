import os

import jax
import jax.numpy as jnp
import optax

from nndt.math_core import grid_in_cube2
from nndt.space.loaders import load_data, preload_all_possible
from nndt.trainable_task import ApproximateSDF
from nndt.vizualize import BasicVizualization

from tqdm import tqdm

LEARNING_RATE = 0.006
EPOCHS = 9001
SHAPE = (128, 128, 128)
FLAT_SHAPE = SHAPE[0] * SHAPE[1] * SHAPE[2]
EXP_NAME = 'sdt2sdf_check'
LOG_FOLDER = f'./{EXP_NAME}/'
LEVEL_SHIFT = 0.03


if __name__ == '__main__':

    os.makedirs(LOG_FOLDER, exist_ok=True)
    folder = '../../tests/acdc_for_test'
    name_list = os.listdir(folder)
    name_list.sort()

    viz = BasicVizualization(LOG_FOLDER, EXP_NAME)
    for width in [2, 4, 8, 16, 32, 64]:
        for depth in [1, 2, 4, 8, 16, 32, 64]:
            for patient in name_list[:1]:
                try:
                    mesh_list = [f"{folder}/{patient}/colored.obj" for p in name_list]
                    sdt_list = [f"{folder}/{patient}/sdf.npy" for p in name_list]
                    sdf_list = [f"sdt2sdf_default/{depth}_{width}_{patient}.pkl" for p in name_list]
                    space = load_data(name_list, mesh_list, sdt_list, sdf_list)
                    preload_all_possible(space)

                    sampling = space[f'default/{patient}/sampling_grid'](spacing=SHAPE)
                    method1 = space[f'default/{patient}/sdt/repr/xyz2sdt']
                    method2 = space[f'default/{patient}/sdfpkl/repr/xyz2sdt']

                    viz.sdt_to_obj(f"{depth}_{width}_{patient}_sdt", method1(sampling)[:, :, :, 0], level=LEVEL_SHIFT)
                    viz.sdt_to_obj(f"{depth}_{width}_{patient}_sdf", method2(sampling)[:, :, :, 0], level=LEVEL_SHIFT)

                except:
                    pass