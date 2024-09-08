__author__ = "Antoine Richard"
__copyright__ = "Copyright 2023-24, Space Robotics Lab, SnT, University of Luxembourg, SpaceR"
__license__ = "BSD 3-Clause"
__version__ = "2.0.0"
__maintainer__ = "Antoine Richard"
__email__ = "antoine.richard@uni.lu"
__status__ = "development"

from src.configurations.physics_confs import PhysicsSceneConf

from omni.isaac.core.physics_context.physics_context import PhysicsContext


class PhysicsSceneManager:
    def __init__(self, settings: PhysicsSceneConf) -> None:
        self.settings = settings
        self.physics_context = PhysicsContext(sim_params=self.settings.physics_scene_args)
        if self.settings.enable_ccd:
            self.physics_context.enable_ccd(True)