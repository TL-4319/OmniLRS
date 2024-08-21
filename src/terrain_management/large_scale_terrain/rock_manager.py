# This class is responsible for managing the rocks on the terrain
# There may be multiple type of rocks, each with their own properties and span.

# The whole of this framework builds on a lot of prayers and the hope that python
# passes arguments by reference.

#    def build_block_grid(self):
#        """
#        The block grid is a dictionary that keeps track of the state of each block in the
#        grid. The state of each block is represented by a dictionary with the following
#        keys:
#            - has_crater_metadata: True if the block has the crater metadata, False otherwise.
#            - has_crater_data: True if the block has the crater data, False otherwise.
#            - has_terrain_data: True if the block has the terrain data, False otherwise.
#            - is_padding: True if the block is a padding block, False otherwise.
#
#        The map_grid_block2coords is a dictionary that maps the block coordinates to the
#        grid coordinates. This is useful to quickly find the block in the grid given the
#        grid coordinates.
#
#        The block grid is generated with a padding of 1 block in each direction. This is
#        done to avoid edge cases when computing the terrain data and to have a buffer of
#        blocks to reuse when the high resolution DEM is shifted.
#        """
#
#        self.block_grid_tracker = {}
#        self.map_grid_block2coords = {}
#
#        state = {
#            "is_generated": False,
#            "is_being_processed": False,
#            "is_padding": False,
#        }
#
#        for x in range(-self.settings.block_span -1, self.settings.block_span + 2, 1):
#            x_c = x * self.settings.block_size
#            x_i = x_c + self.current_block_coord[0]
#            for y in range(-self.settings.block_span -1, self.settings.block_span + 2, 1):
#                y_c = y * self.settings.block_size
#                y_i = y_c + self.current_block_coord[1]
#                self.block_grid_tracker[(x_c, y_c)] = copy.copy(state)
#                if (x == -self.settings.block_span - 1) or (
#                    x == self.settings.block_span + 1
#                ):
#                    self.block_grid_tracker[(x_c, y_c)]["is_padding"] = True
#                elif (y == -self.settings.block_span - 1) or (
#                    y == self.settings.block_span + 1
#                ):
#                    self.block_grid_tracker[(x_c, y_c)]["is_padding"] = True
#                else:
#                    self.block_grid_tracker[(x_c, y_c)]["is_padding"] = False
#                self.map_grid_block2coords[(x_i, y_i)] = (x_c, y_c)
#
#    def shift_block_grid(self, coordinates: Tuple[float, float]) -> None:
#        """
#        Shifts the block grid to the given coordinates while preserving the state of the
#        blocks. The function will also update the map_grid_block2coords dictionary to
#        reflect the new block coordinates.
#
#        Args:
#            coordinates (Tuple[float, float]): Coordinates in meters in the low resolution
#        """
#
#        new_block_grid_tracker = {}
#        new_map_grid_block2coords = {}
#
#        state = {
#            "is_generated": False,
#            "is_being_processed": False,
#            "is_padding": False,
#        }
#
#        for x in range(-self.settings.block_span -1, self.settings.block_span + 2, 1):
#            x_c = x * self.settings.block_size
#            x_i = x_c + coordinates[0]
#            for y in range(-self.settings.block_span -1, self.settings.block_span + 2, 1):
#                y_c = y * self.settings.block_size
#                y_i = y_c + coordinates[1]
#
#                # Check if the block is new or already in the map
#                if (x_i, y_i) not in self.map_grid_block2coords:
#                    new_block_grid_tracker[(x_c, y_c)] = copy.copy(state)
#                else:
#                    new_block_grid_tracker[(x_c, y_c)] = self.block_grid_tracker[
#                        self.map_grid_block2coords[(x_i, y_i)]
#                    ]
#
#                new_map_grid_block2coords[(x_i, y_i)] = (x_c, y_c)
#                if (x == -self.settings.block_span - 1) or (
#                    x == self.settings.block_span + 1
#                ):
#                    new_block_grid_tracker[(x_c, y_c)]["is_padding"] = True
#                elif (y == -self.settings.block_span - 1) or (
#                    y == self.settings.block_span + 1
#                ):
#                    new_block_grid_tracker[(x_c, y_c)]["is_padding"] = True
#                else:
#                    new_block_grid_tracker[(x_c, y_c)]["is_padding"] = False
#
#        # Overwrite the old state with the new state
#        self.block_grid_tracker = new_block_grid_tracker
#        self.map_grid_block2coords = new_map_grid_block2coords

# Sample 2D position
# Use DEM sampler
#   Sample Height
#   Sample Normal

from typing import List, Tuple, Dict
import numpy as np
import dataclasses
import threading
import time
import copy
import os

import omni

from src.terrain_management.large_scale_terrain.rock_distribution import (
    RockSamplerCfg,
    RockSampler,
)
from src.terrain_management.large_scale_terrain.rock_database import RockDB, RockDBCfg
from WorldBuilders.pxr_utils import createInstancerAndCache, setInstancerParameters
from src.terrain_management.large_scale_terrain.utils import BoundingBox


class OGInstancer:
    """
    The Original Gangster: the point instancer.
    """

    def __init__(self, instancer_path, assets_path, seed):
        self.instancer_path = instancer_path
        self.stage = omni.usd.get_context().get_stage()
        self.assets_path = assets_path
        self.get_asset_list()
        createInstancerAndCache(self.stage, self.instancer_path, self.prototypes)
        self.rng = np.random.default_rng(seed=seed)

    def get_asset_list(self):
        self.prototypes = [
            os.path.join(self.assets_path, file)
            for file in os.listdir(self.assets_path)
            if file.endswith(".usd")
        ]

    def setInstanceParameter(
        self,
        position: np.ndarray,
        orientation: np.ndarray,
        scale: np.ndarray,
        ids: np.ndarray,
        **kwargs
    ) -> None:
        """
        Set the instancer's parameters. It sets the position, orientation, and scale of the instances.

        Args:
            position (np.ndarray): The position of the instances.
            orientation (np.ndarray): The orientation of the instances.
            scale (np.ndarray): The scale of the instances.
            ids (np.ndarray): The ids of the instances.
            **kwargs: Extra arguments.
        """

        setInstancerParameters(
            self.stage,
            self.instancer_path,
            position,
            quat=orientation,
            scale=scale,
            ids=ids,
            **kwargs,
        )


class RockGeneratorCfg:
    rock_db_cfg: RockDBCfg = dataclasses.field(default_factory=dict)
    rock_sampler_cfg: RockSamplerCfg = dataclasses.field(default_factory=dict)
    rock_assets_folder: str = dataclasses.field(default_factory=list)
    instancer_name: str = dataclasses.field(default_factory=str)
    seed: int = dataclasses.field(default_factory=int)
    block_span: int = dataclasses.field(default_factory=int)
    block_size: int = dataclasses.field(default_factory=int)

    def __post_init__(self):
        assert self.instancer_name != "", "Instancer name cannot be empty"
        assert self.block_span >= 0, "Block span must be greater or equal to 0"
        assert os.path.exists(self.rock_assets_folder), "Rock assets folder not found"

        self.rock_db_cfg = RockDBCfg(**self.rock_db_cfg)
        self.rock_sampler_cfg = RockSamplerCfg(**self.rock_sampler_cfg)


class RockGenerator:
    def __init__(
        self,
        settings: RockGeneratorCfg,
        sampling_func: function,
        map_state: Dict,
        instancer_path: str,
    ):
        self.settings = settings
        self.sampling_func = sampling_func
        self.map_state = map_state
        self.instancer_path = instancer_path
        self.is_sampling = False

    def build(self):
        self.rock_db = RockDB(self.settings.rock_db_cfg)
        self.rock_sampler = RockSampler(
            self.settings.rock_sampler_cfg,
            self.rock_db,
            map_sampling_func=self.sampling_func,
        )
        self.rock_instancer = OGInstancer(
            os.path.join(self.instancer_path, self.settings.instancer_name),
            self.settings.rock_assets_folder,
            self.settings.seed,
        )

    def cast_coordinates_to_block_space(
        self, coordinates: Tuple[float, float]
    ) -> Tuple[int, int]:
        """
        Casts the given coordinates to the block space. The block space is the space
        where the blocks are defined. The block space is defined by the block size and
        the resolution of the high resolution DEM.

        The coordinates are still expressed in meters, but they can only be an increment of
        the block size (in meters).
        """

        x, y = coordinates
        x_block = int(x // self.settings.block_size) * self.settings.block_size
        y_block = int(y // self.settings.block_size) * self.settings.block_size
        return (x_block, y_block)

    def define_region(self, coordinates: Tuple[float, float]) -> BoundingBox:
        x_low = (
            coordinates[0] - (self.settings.block_span + 1) * self.settings.block_size
        )
        x_high = (
            coordinates[0] + (self.settings.block_span + 2) * self.settings.block_size
        )
        y_low = (
            coordinates[1] - (self.settings.block_span + 1) * self.settings.block_size
        )
        y_high = (
            coordinates[1] + (self.settings.block_span + 2) * self.settings.block_size
        )

        return BoundingBox(x_min=x_low, x_max=x_high, y_min=y_low, y_max=y_high)

    def sample(self, position: Tuple[float, float]):
        self.is_sampling = True
        coordinates = self.cast_coordinates_to_block_space(position)
        region = self.define_region(coordinates)
        self.rock_sampler.sample_rocks_by_region(region)
        self.is_sampling = False

    def threaded_sample(self, position: Tuple[float, float]):
        while self.is_sampling:
            time.sleep(0.1)

        threading.Thread(target=self.sample, args=(position,)).start()


@dataclasses.dataclass
class RockManagerCfg:
    rock_gen_cfgs: List[RockGeneratorCfg] = dataclasses.field(default_factory=list)
    instancers_path: str = dataclasses.field(default_factory=str)
    seed: int = dataclasses.field(default_factory=int)

    def __post_init__(self):
        self.rock_gen_cfgs = [RockGeneratorCfg(**cfg) for cfg in self.rock_gen_cfgs]


class RockManager:
    def __init__(
        self, settings: RockManagerCfg, sampling_func: function, map_state: Dict
    ):
        self.settings = settings
        self.sampling_func = sampling_func
        self.map_state = map_state
