# SO-101 Robotic Arm

![Status](https://img.shields.io/badge/Status-In%20Progress-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![LeRobot](https://img.shields.io/badge/LeRobot-Hugging%20Face-blue)

## Demo

![SO-101 Leader-Follower Teleoperation](images/so101_teleoperation_demo.gif)

A leader-follower robotic manipulation platform built using the open-source SO-101 architecture and Hugging Face LeRobot framework. The project covers mechanical assembly, serial bus servo configuration, arm calibration, real-time teleoperation, and learning-based robotic manipulation.

## Overview

This is a personal robotics project focused on developing hands-on experience across the robotics stack — from mechanical assembly and hardware integration to robot control, computer vision, data collection, and imitation learning.

The system consists of a manually controlled leader arm and a six-axis follower arm. Leader joint positions are communicated to the follower through LeRobot for real-time teleoperation. Future development will use teleoperated demonstrations to train autonomous manipulation policies.

## Hardware

- SO-101 leader and follower robotic arms
- Feetech STS3215 serial bus servo motors
- 3D-printed PLA structural components
- Serial bus servo controller boards
- 5V leader and 12V follower power systems
- USB serial communication

## Software Stack

- Python 3.10
- Hugging Face LeRobot
- PyTorch
- Miniforge / Conda
- Ubuntu 22.04 via WSL2

## Project Phases

### Phase 1 — Mechanical Assembly
- [x] Source and 3D print structural components
- [x] Assemble leader and follower manipulators
- [x] Install motors, servo horns, cabling, and controller hardware

### Phase 2 — Motor Configuration and Calibration
- [x] Assign unique IDs to 12 Feetech serial bus servos
- [x] Configure motor communication parameters
- [x] Calibrate six joints on the leader and follower arms through their full ranges of motion

### Phase 3 — Teleoperation
- [x] Configure LeRobot development environment
- [x] Establish USB serial communication through Ubuntu and WSL2
- [x] Implement real-time leader-follower teleoperation
- [x] Develop custom Python scripts for programmatic joint control

### Phase 4 — Control Systems

- [x] Designed and implemented a custom outer-loop proportional controller for trajectory tracking
- [x] Generated sinusoidal reference trajectories for the base joint
- [x] Logged desired vs. measured joint positions
- [x] Evaluated tracking performance using RMS, mean, and maximum error
- [x] Performed proportional gain tuning (Kp sweep)
- [x] Identified stability limit through experimental testing

### Phase 5 — Vision and Data Collection
- [ ] Integrate cameras into the manipulation workspace
- [ ] Configure OpenCV camera streams
- [ ] Record teleoperated manipulation demonstrations
- [ ] Build and visualize LeRobot datasets

### Phase 6 — Imitation Learning
- [ ] Train an ACT policy using recorded demonstrations
- [ ] Evaluate autonomous task execution
- [ ] Analyze task success rate and failure modes
- [ ] Improve policy performance through dataset iteration

## Experimental Results

### Base Joint Trajectory Tracking

A custom proportional feedback controller was implemented around the SO-101's internal servo controller to improve trajectory tracking.

The controller was evaluated by commanding a sinusoidal reference trajectory while logging desired and measured joint positions.

| Controller | RMS Error |
|------------|-----------|
| Baseline | 0.599° |
| P Controller (Kp = 2.0) | 0.212° |

The proportional controller reduced RMS tracking error by approximately **65%** before oscillatory behavior appeared at higher gains (Kp ≥ 2.25).

## Tracking Performance

![Trajectory Tracking](images/tracking_plot.png)

## Current Status

Leader and follower arms have been assembled, configured, and calibrated. Real-time teleoperation is functional, with the follower arm replicating joint motion from the leader arm.

The next development milestone is camera integration and collection of the first teleoperated manipulation dataset.

## Build Log

- **June 2026** — Repository initialized and structural components printed at Syracuse University.
- **July 2026** — Completed mechanical assembly and calibration of leader and follower SO-101 robotic arms.
- Implemented teleoperation using the Hugging Face LeRobot framework.
- Developed custom Python scripts for sinusoidal trajectory generation and trajectory tracking.
- Designed an outer-loop proportional controller and reduced RMS tracking error by approximately 65%.
- Characterized controller stability through proportional gain tuning experiments.

## References

- [SO-101 Documentation](https://huggingface.co/docs/lerobot/en/so101)
- [SO-ARM100 Hardware Repository](https://github.com/TheRobotStudio/SO-ARM100)
- [LeRobot Framework](https://github.com/huggingface/lerobot)
