# SO-101 Robotic Arm

![Status](https://img.shields.io/badge/Status-In%20Progress-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![LeRobot](https://img.shields.io/badge/LeRobot-Hugging%20Face-blue)

A 6-DOF robotic arm built from the open-source SO-101 platform by Hugging Face. The project covers full mechanical assembly from 3D-printed components, motor configuration, Python-based teleoperation, and imitation learning using the LeRobot framework.

## Overview

This is a personal engineering project built alongside a systems engineering internship at Saab. The goal is to develop hands-on experience with the full robotics stack — from mechanical design and hardware integration to Python control and machine learning-based task execution.

## Hardware

- 6x Feetech STS3215 serial bus servo motors
- 3D-printed structural components (PLA) — printed at Syracuse University
- Waveshare controller board
- Leader and follower arm configuration for teleoperation

## Software Stack

- Python 3.x
- Hugging Face LeRobot framework
- Feetech SDK for motor communication

## Project Phases

### Phase 1 — Mechanical Assembly
- 3D print all structural components from SO-ARM100 STL files
- Assemble 6 joints per the SO-101 build guide
- Source and install all hardware (motors, screws, cables)

### Phase 2 — Motor Configuration
- Configure unique motor IDs and baudrates via Feetech SDK
- Calibrate leader and follower arms through full range of motion

### Phase 3 — Python Control
- Install LeRobot and establish USB communication with controller board
- Implement teleoperation between leader and follower arms
- Write custom Python scripts for programmatic joint control

### Phase 4 — Imitation Learning (stretch goal)
- Record demonstration datasets using teleoperation
- Train a neural network policy using LeRobot's ACT framework
- Evaluate autonomous task execution on the follower arm

## Build Log

Updates added as the project progresses.

- **May 2026** — Repository initialized. Parts printing at Syracuse University.

## References

- [SO-101 Documentation](https://huggingface.co/docs/lerobot/en/so101)
- [SO-ARM100 Hardware Repo](https://github.com/TheRobotStudio/SO-ARM100)
- [LeRobot Framework](https://github.com/huggingface/lerobot)
