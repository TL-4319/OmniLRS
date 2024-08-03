# OmniLRS v1.0 Fork for LAGER

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
~/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh run.py environment=lunaryard_deformable_20m mode=ROS2 rendering=ray_tracing mode.bridge_name=humble
```


## TO DOs:
- [ ] Setup sim env with Lunar south pole DEM
- [ ] Figure out robot configurations
- [ ] Teleop node 

