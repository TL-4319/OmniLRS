import omni
import copy
import math
import os

from omni.isaac.kit import SimulationApp


cfg = {
    "headless": False,
}
simulation_app = SimulationApp(cfg)

RDBCfg_D = {
    "block_size": 50,
    "max_blocks": int(1e7),
    "save_to_disk": False,
    "write_to_disk_interval": 1000,
}
RSCfg_1_D = {
    "block_size": 50,
    "rock_dist_cfg": {
        "position_distribution": {
            "name": "thomas_point_process",
            "parent_density": 0.04,
            "child_density": 100,
            "sigma": 3,
            "seed": 42,
        },
        "scale_distribution": {
            "name": "uniform",
            "min": 0.02,
            "max": 0.05,
            "seed": 42,
        },
        "seed": 42,
        "num_rock_id": 50,
    },
}
RSCfg_2_D = {
    "block_size": 50,
    "rock_dist_cfg": {
        "position_distribution": {
            "name": "thomas_point_process",
            "parent_density": 0.01,
            "child_density": 25,
            "sigma": 3,
            "seed": 42,
        },
        "scale_distribution": {
            "name": "uniform",
            "min": 0.05,
            "max": 0.2,
            "seed": 42,
        },
        "seed": 43,
        "num_rock_id": 50,
    },
}
RGCfg_1_D = {
    "rock_db_cfg": RDBCfg_D,
    "rock_sampler_cfg": RSCfg_1_D,
    "rock_assets_folder": "assets/USD_Assets/rocks/small",
    "instancer_name": "very_small_rock_instancer",
    "seed": 42,
    "block_span": 0,
    "block_size": 50,
}
RGCfg_2_D = {
    "rock_db_cfg": RDBCfg_D,
    "rock_sampler_cfg": RSCfg_2_D,
    "rock_assets_folder": "assets/USD_Assets/rocks/small",
    "instancer_name": "large_rock_instancer",
    "seed": 42,
    "block_span": 1,
    "block_size": 50,
}
RMCfg_D = {
    "rock_gen_cfgs": [RGCfg_1_D, RGCfg_2_D],
    "instancers_path": "/World/rock_instancers",
    "seed": 42,
}


if __name__ == "__main__":
    from omni.isaac.core import World
    from omni.usd import get_context
    from pxr import UsdLux, UsdGeom, Gf, UsdShade

    from WorldBuilders.pxr_utils import setDefaultOps, addDefaultOps
    import numpy as np

    from src.terrain_management.large_scale_terrain.rock_manager import (
        RockManagerCfg,
        RockManager,
    )
    from src.terrain_management.large_scale_terrain.rock_distribution import mock_call

    def is_map_done():
        return True

    def bindMaterial(stage, mtl_prim_path, prim_path):
        mtl_prim = stage.GetPrimAtPath(mtl_prim_path)
        prim = stage.GetPrimAtPath(prim_path)
        shade = UsdShade.Material(mtl_prim)
        UsdShade.MaterialBindingAPI(prim).Bind(
            shade, UsdShade.Tokens.strongerThanDescendants
        )

    world = World(stage_units_in_meters=1.0)
    stage = get_context().get_stage()
    asset_path = os.path.join(os.getcwd(), "assets")

    # Let there be light
    light = UsdLux.DistantLight.Define(stage, "/World/sun")
    light.CreateIntensityAttr(3000.0)
    addDefaultOps(light.GetPrim())
    setDefaultOps(light.GetPrim(), (0, 0, 0), (0.65, 0, 0, 0.76), (1, 1, 1))

    C = 0
    R = 500 * 5
    max_displacement = 2.0 / 30
    acquisition_rate = 1
    perimeter = 2 * np.pi * R
    rotation_rate = int(perimeter / max_displacement)
    spiral_rate = 0.0 / rotation_rate
    theta = np.linspace(0, 2 * np.pi, rotation_rate)
    i = 0
    i2 = 1.0
    print(rotation_rate)

    x = C + i2 * R * math.cos(theta[i])
    y = C + i2 * R * math.sin(theta[i])

    initial_position = (x, y)

    rm_settings = RockManagerCfg(**RMCfg_D)
    RM = RockManager(rm_settings, mock_call, is_map_done)
    RM.build()
    RM.sample((0, 0))

    timeline = omni.timeline.get_timeline_interface()
    timeline.play()

    i3 = 0
    target = R * 2 * math.pi / max_displacement / acquisition_rate
    target = target / 8
    target += 10
    Q_camera4 = None
    while True:
        # x_new = C + i2 * R * math.cos(theta[i])
        # y_new = C + i2 * R * math.sin(theta[i])
        # x_delta = x_new - x
        # y_delta = y_new - y
        # coords = (x_delta, y_delta)
        # Q_camera2 = quat_mul(heading_to_quat(theta[i]), Q_camera)
        # Q_terrain = LSTM.get_normal_local(coords)
        # Q_camera3 = quat_mul(Q_terrain, Q_camera2)
        # if Q_camera4 is None:
        #    Q_camera4 = copy.copy(Q_camera3)
        # else:
        #    Q_camera4 = EMAquat(Q_camera4, Q_camera3, 0.0333)
        # LSTM.update_visual_mesh(coords)
        # setDefaultOps(
        #    camera.GetPrim(),
        #    (x_delta, y_delta, LSTM.get_height_local(coords) + 0.5),
        #    Q_camera4,
        #    (1, 1, 1),
        # )
        world.step(render=True)
        # i = (i + 1) % rotation_rate
        # if i % acquisition_rate == 0:
        #    try:
        #        AL.record()
        #        i3 += 1
        #    except Exception as e:
        #        print(e)
    #    i2 += spiral_rate
    timeline.stop()
    simulation_app.close()