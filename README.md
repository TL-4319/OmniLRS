# OmniLRS v2.0 Fork for LAGER

This is a fork from the [OmniLRS project](https://github.com/AntoineRichard/OmniLRS) for testing by UA LAGER lab workstation.

## Dependencies

* Ubuntu 22.04
* ROS2 Humble
* NVIDIA GPU and drivers

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

There are several environment to choose from which are located in ```cfg/envronment```. Each environment yaml file define the type of environment, terrain generation params and robots. To swap to another environment e.g. defined in ```cfg/environment/lunaryard_20m.yaml```, change the above command to 

```
  ~/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh run.py environment=lunaryard_20m
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

## VIPER asset
To facilitate the research being performed at UA, a mockup of NASA's VIPER rover is developed. Although detailed design parameters are not published by NASA, the VIPER asset is constructed using whatever dimensions available. The design was made on [OnShape](https://cad.onshape.com/documents/73016347d346344bedb8834a/w/3e0c13501bf66b30f9e4bfc1/e/136367780910618495a34a9c)

The CAD files were imported to construct a robot USD asset for Isaac Sim. To reduce complexity, the active suspension and explicit steer mechanism of NASA VIPER are simplified to a skid steer robot. The navigation on the mast can articulate in pan and tilt. 

### Sensors
Some sensors were added to the USB asset and the corresponding ROS2 publisher were integrated to facilitate synthetic data generation and recording via ROS bags. Sensors include

* Stereo optical cameras
  * Configured based on specification of VIPER NASA NavCam (CMV4000 sensor + lens) - emulate resolution, FOV and stereo baseline of 40cm
  * Mounted on the mast with pan and tilt
* LIDAR
  * Mounted on the mast with pan and tilt
  * Using sample Isaac Sim flash lidar for now
  * Uses RTX based sensor so does not dependant on collision to generate ray collision - reduce computation on small rock collision mesh
* IMU 
  * Mounted near robot center of gravity

>[!NOTE] 
> The synthetic data generation of camera and LIDAR are very intensive, especially in large environments which can actually causes crashes. Currently, the asset viper_lidar_only.usd asset seems to be more stable with largescale environment. Actions during simulation including play/pause and physics engine changes need to be made slowly as to not crash the sim.

### Teleop
Teleop supports the Logitech Extreme3D joystick. Once the sim is started, start the teleop node by running the following in a new terminal with ROS2 sourced

```
ros2 launch teleop_twist_joy teleop-launch.py config_filepath:='extreme3d.config.yaml'
```

Front/back speed is control via joystick forward/backward. Left/right turn is controlled via joystick twist. The thumb stick can be used to control the navigation sensor assembly's pan/tilt

### Custom RTXLidar
Once the necessary LIDAR config .json file has been created. Add it to 
```
./exts/omni.isaac.sensor/data/lidar_configs
```

### Misc
A full ROS transformation tree is also available as topics for coordinate frame transformation and localization truthing

## TO DOs:
- [ ] Fix jitter in OmniLRSv2 (might not be fixable - unrealistic during stationary phases. Non-issue if rover is moving)
- [x] Add Blickfeld Cube lidar to RTXLidar to VIPER asset
- [x] Add imu to VIPER asset
- [x] Add CMV4000 optical camera to VIPER asset to emulate NavCam
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

