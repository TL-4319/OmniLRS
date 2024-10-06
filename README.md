# OmniLRS v2.0 Fork for LAGER

This is a fork from the [OmniLRS project](https://github.com/AntoineRichard/OmniLRS) for testing by UA LAGER lab workstation.

## Running the sim

Source ROS2 for every new terminal. LAGER workstation already source ROS2 in .bashrc.

Prior to running the simulation, setup the environment of a new terminal by:


```
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lagerworkstation/.local/share/ov/pkg/isaac-sim-2023.1.1/exts/omni.isaac.ros2_bridge/humble/lib
RMW_IMPLEMENTATION=rmw_fastrtps_cpp
```

To start a sample sim, run the following command:

```
~/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh run.py environment=largescale
```

When the sim starts, stop the physics simulation and change the collision type to Separating Axis Theorem (SAT) instead of PCM in physics_scene/collision_type.

## Modify USD

To start Isaac sim without the rest of the Lunar functionalities to edit an USD. Set the environment path in a terminal with 

```
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lagerworkstation/.local/share/ov/pkg/isaac-sim-2023.1.1/exts/omni.isaac.ros2_bridge/humble/lib
RMW_IMPLEMENTATION=rmw_fastrtps_cpp
```

Then start Isaac sim by

```
~/.local/share/ov/pkg/isaac-sim-2023.1.1/isaac-sim.sh
```

## Teleop
Teleop supports the Logitech Extreme3D joystick. Once the sim is started, start the teleop node by running the following in a new terminal with ROS2 sourced

```
ros2 launch teleop_twist_joy teleop-launch.py config_filepath:='extreme3d.config.yaml'
```

Front/back speed is control via joystick forward/backward. Left/right turn is controlled via joystick twist. Depress thumb button to enable teleop command.

## TO DOs:
- [ ] Fix jitter in OmniLRSv2 (might not be fixable - unrealistic during stationary phases. Non-issue if rover is moving)
- [ ] Add Blickfeld Cube lidar to RTXLidar to VIPER asset
- [ ] Add imu to VIPER asset
- [ ] Add OV2311 optical camera to VIPER asset
- [ ] Add better nav light to VIPER asset

## Directory Structure
```bash
.
├── assets
├── cfg
│   ├── environment
│   ├── mode
│   └── rendering
├── src
│   ├── configurations
│   ├── environments
│   ├── environments_wrappers
│   │   ├── ros1
│   │   ├── ros2
│   │   └── sdg
│   ├── labeling
│   ├── robots
│   ├── ros
│   └── terrain_management
└── WorldBuilders
```

