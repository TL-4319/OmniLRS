# OmniLRS v2.0 Fork for LAGER

This is a fork from the [OmniLRS project](https://github.com/AntoineRichard/OmniLRS) for testing by UA LAGER lab workstation.

<<<<<<< HEAD
## Dependencies
=======
> [!IMPORTANT]
> This readme provides basic information on how to use the simulation. For a more complete introduction to the simulation and its inner workings please [visit our wiki](https://github.com/AntoineRichard/OmniLRS/wiki)! For specific questions or to have a chat join [our discord](https://discord.gg/NUpKtFs6)!
>>>>>>> terrain_rework

* Ubuntu 22.04
* ROS2 Humble
* NVIDIA GPU and drivers

## Running the sim

Source ROS2 for every new terminal. LAGER workstation already source ROS2 in .bashrc.

Prior to running the simulation, setup the environment of a new terminal by:

<<<<<<< HEAD
```
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lagerworkstation/.local/share/ov/pkg/isaac-sim-4.1.0/exts/omni.isaac.ros2_bridge/humble/lib
RMW_IMPLEMENTATION=rmw_fastrtps_cpp
=======
> [!NOTE]
> Please note that this is a partial release. More robots will be made available at a later date. Should you run into a bug, or would like to request a new feature, feel free to open an issue. Want to collaborate, reach out to us!

## OmniLRS in action!

First release:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/PebUZjm0WuA/0.jpg)](https://www.youtube.com/watch?v=PebUZjm0WuA)

Wheel traces:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/TpzD0h-5hv4/0.jpg)](https://www.youtube.com/watch?v=TpzD0h-5hv4)

Large Scale update:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/3m78fO5uXwA/0.jpg)](https://www.youtube.com/watch?v=3m78fO5uXwA)



## Installation

In this page we'll walk you through the installation process of our simulation. Since our simulation is built on top of Isaac, you will need an Nvidia GPU to run it.

Hardware requirement:
- An Nvidia GPU:
  - with 8+ Gb of VRAM (some scene will work on 4Gb)
  - RTX Series 2000 or above.
- A recent 12+ threads CPU.
- 32Gb of RAM. (for some scene 16Gb is enough)
- 10+ Gb of free space.

Operating System:
- Linux distros similar to Ubuntu 20.04 or 22.04.

> [!WARNING]
> Windows is not supported.

To install the simulation we strongly suggest using [docker](#docker-install). Though the install could also be done using a [native installation](#native-installation).

### Native installation

The first thing that needs to be done before we proceed with the native installation is to install Isaac. We support two version 2023.1.1 and 4.1.0. Though we'd recommend sticking to **2023.1.1** as there are some issues with renderings in 4.1.0. Our dockers currently come in the 2023.1.1 version of Isaac.

> [!TIP]
> If you're unsure on how to install Isaac sim, look-up the following: [How to install Isaac Sim.](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html)

To simplify the remainder of the installation process of the framework we provide a script that will automatically download all the assets, as well as install the required dependencies. It will not install Isaac Sim.
> [!IMPORTANT]
> Run this command at the root of the repository. 

```bash
scripts/install_native.sh
>>>>>>> terrain_rework
```

To start a sample sim, run the following command:

```
~/.local/share/ov/pkg/isaac-sim-4.1.0/python.sh run.py environment=largescale
```

There are several environment to choose from which are located in ```cfg/envronment```. Each environment yaml file define the type of environment, terrain generation params and robots. To swap to another environment e.g. defined in ```cfg/environment/lunaryard_20m.yaml```, change the above command to 

```
  ~/.local/share/ov/pkg/isaac-sim-4.1.0/python.sh run.py environment=lunaryard_20m
```

When the sim starts, stop the physics simulation and change the collision type to Separating Axis Theorem (SAT) instead of PCM in physics_scene/collision_type.

>[!NOTE] 
> Recently, IsaacSim 4.1.0 should be used over 2023.1.1 since the newer version has support for limiting publishing rate for camera and lidar


## Modify USD

To start Isaac sim without the rest of the Lunar functionalities to edit an USD. Set the environment path in a terminal with 

```
<<<<<<< HEAD
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lagerworkstation/.local/share/ov/pkg/isaac-sim-4.1.0/exts/omni.isaac.ros2_bridge/humble/lib
RMW_IMPLEMENTATION=rmw_fastrtps_cpp
=======
Then start the docker
```bash
./omnilrs.docker/run_docker.sh
```
And run the script in the docker:
```bash
scritps/install_docker.sh
```
This will download the assets from docker and it should work fine. The issue is that all the generated folder will be
owned by root. So you may want to change that afterwards by running:
```bash
chown -R $USER assets
chgrp -R $USER assets
>>>>>>> terrain_rework
```

Then start Isaac sim by

```
~/.local/share/ov/pkg/isaac-sim-4.1.0/isaac-sim.sh
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

Make new directory ```CUSTOM``` at 
```
./exts/omni.isaac.sensor/data/lidar_configs/
```

IsaacSim needs to be configure to include the path above when searching for LIDAR config file during LIDAR creation. To do so, edit ```./exts/omni.isaac.sensor/config/extension.toml```. In that file, find the setting ```app.sensors.nv.lidar.profileBaseFolder``` and add ```"${app}/../exts/omni.isaac.sensor/data/lidar_configs/CUSTOM/"```

Any custom LIDAR config .json file can be added to 

```
./exts/omni.isaac.sensor/data/lidar_configs/
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

