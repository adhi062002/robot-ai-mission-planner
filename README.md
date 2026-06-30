# 🤖 Robot AI Mission Planner

An AI-powered ROS2 mission planning framework that converts natural language commands into structured robot missions.

---

## Overview

This project demonstrates how natural language commands can be translated into executable robot missions using ROS2.

The current implementation includes:

- Rule-based Natural Language Processing
- Mission JSON generation
- Mission validation
- ROS2 Publisher/Subscriber communication
- Dynamic mission execution using predefined routes

Future versions will integrate:

- Ollama LLM
- Gazebo Simulation
- Nav2
- Docker
- Autonomous Mobile Robots

---

## Features

- ✅ Natural Language Mission Planning
- ✅ Rule-Based Parser
- ✅ JSON Mission Generation
- ✅ JSON Validation
- ✅ ROS2 Publisher
- ✅ ROS2 Subscriber
- ✅ Dynamic Route Loading
- ✅ Modular ROS2 Architecture

---

## Project Architecture

```
                 User
                  │
                  ▼
      Natural Language Prompt
                  │
                  ▼
      Rule-Based Mission Planner
                  │
                  ▼
           Mission JSON
                  │
                  ▼
        Mission Validator
                  │
                  ▼
       ROS2 Mission Publisher
                  │
          /mission_command
                  │
                  ▼
      ROS2 Mission Subscriber
                  │
                  ▼
         Mission Executor
                  │
                  ▼
     Route JSON + Waypoints
```

---

## Folder Structure

```
robot_ai_mission_planner/

├── launch/
├── missions/
│   ├── inspection_loop.json
│   └── perimeter_loop.json
│
├── robot_ai_mission_planner/
│   ├── executor/
│   ├── interfaces/
│   ├── mission_llm/
│   ├── validator/
│   ├── mission_publisher.py
│   ├── mission_subscriber.py
│   ├── executor_node.py
│   └── main.py
│
├── package.xml
├── setup.py
└── README.md
```

---

## Build

```bash
cd ros2_ws

source /opt/ros/humble/setup.bash

colcon build --symlink-install

source install/setup.bash
```

---

## Run

### Terminal 1

```bash
ros2 run robot_ai_mission_planner mission_executor
```

### Terminal 2

```bash
ros2 run robot_ai_mission_planner mission_planner
```

---

## Example Command

```
Patrol the perimeter twice fast
```

Generated Mission

```json
{
  "mission": "navigation",
  "actions": [
    {
      "type": "follow_route",
      "route": "perimeter_loop",
      "laps": 2,
      "speed": 0.6
    }
  ]
}
```

---

## Technologies

- ROS2 Humble
- Python
- rclpy
- JSON
- Git
- GitHub

---

## Roadmap

### Completed

- Project Structure
- Rule-Based NLP
- JSON Validation
- Mission Executor
- ROS2 Package
- Publisher / Subscriber Architecture

### Upcoming

- Launch Files
- Gazebo Integration
- Nav2
- Ollama LLM
- Docker Deployment
- CI/CD

---

## Author

**Adithya Satheesh**

Robotics Engineer | ROS2 | AI | Autonomous Mobile Robots