# System Architecture

## Overview

The Robot AI Mission Planner is a ROS 2-based autonomous mission planning system that converts natural language commands into executable robot missions. The system integrates a Large Language Model (LLM), structured mission generation, ROS 2 communication, and autonomous navigation using Nav2 within a Gazebo simulation.

Instead of manually programming robot behaviors, the user provides a high-level instruction such as:

> "Inspect the warehouse perimeter."

The system interprets the instruction, generates a structured mission in JSON format, validates it, publishes it through ROS 2, and executes the mission using predefined navigation routes.

---

# High-Level Architecture

```
                +---------------------------+
                |          User             |
                | Natural Language Command  |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |      Mission Planner      |
                |  (LLM / Rule-Based AI)    |
                +-------------+-------------+
                              |
                     Mission JSON
                              |
                              v
                +---------------------------+
                |     JSON Validator        |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |    Mission Publisher      |
                |      ROS 2 Topic          |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |   Mission Subscriber      |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |    Mission Executor       |
                +-------------+-------------+
                              |
                         Nav2 Goals
                              |
                              v
                +---------------------------+
                |        Nav2 Stack         |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |  TurtleBot3 + Gazebo      |
                +---------------------------+
```

---

# Software Components

The system is divided into multiple independent modules, each responsible for a specific stage of the mission execution pipeline.

## 1. Mission Planner

The Mission Planner is responsible for interpreting user commands.

Its responsibilities include:

- Understanding natural language instructions
- Identifying the requested task
- Selecting the appropriate navigation route
- Generating a structured mission JSON

Two planning approaches are supported:

- Ollama LLM planner
- Rule-based planner (fallback)

Output example:

```json
{
    "actions": [
        {
            "type": "navigate_route",
            "route": "warehouse_route"
        }
    ]
}
```

---

## 2. JSON Validator

Before execution, every generated mission is validated against the predefined mission schema.

Validation ensures:

- Required fields exist
- Correct data types
- Supported action types
- Proper JSON formatting

This prevents invalid missions from reaching the robot.

---

## 3. Mission Publisher

The Mission Publisher converts the validated mission into a JSON string and publishes it on a ROS 2 topic.

Responsibilities:

- Serialize mission JSON
- Publish mission message
- Decouple planning from execution

---

## 4. Mission Subscriber

The Mission Subscriber continuously listens for incoming missions.

Once a new mission is received:

1. Deserialize JSON
2. Verify message integrity
3. Pass mission to the Mission Executor

---

## 5. Mission Executor

The Mission Executor performs the actual autonomous task execution.

Responsibilities include:

- Load predefined waypoint files
- Generate navigation goals
- Send goals to Nav2
- Monitor execution status
- Continue until all waypoints are completed

The executor contains the core mission logic.

---

## 6. Route Recorder

The Route Recorder allows developers to create reusable navigation paths.

It records the robot pose while driving and saves the collected waypoints as JSON route files.

Example routes:

- warehouse_route.json
- perimeter_loop.json
- inspection_loop.json

These route files are later reused by the Mission Planner.

---

## 7. Initial Pose Publisher

The Initial Pose Publisher initializes the robot localization by publishing the robot's starting pose to the localization system.

This enables Nav2 to begin planning from the correct map location.

---

# ROS 2 Communication

The application follows a publish-subscribe architecture.

```
Mission Planner
        |
        | Publish Mission
        v
+----------------------+
|   /mission_topic     |
+----------------------+
        |
        v
Mission Subscriber
        |
        v
Mission Executor
        |
        v
Nav2 Action Server
        |
        v
Gazebo Robot
```

This architecture provides loose coupling between planning and execution, making each component independently testable and replaceable.

---

# Navigation Pipeline

Mission execution relies on the ROS 2 Navigation Stack (Nav2).

The execution sequence is:

1. Receive mission
2. Load route JSON
3. Read waypoints
4. Convert waypoints into navigation goals
5. Send goals to Nav2
6. Nav2 computes a path
7. Robot follows the path
8. Repeat until all goals are completed

---

# Mission Data Flow

```
User Prompt
      │
      ▼
LLM Planner
      │
      ▼
Mission JSON
      │
      ▼
JSON Validator
      │
      ▼
Mission Publisher
      │
      ▼
ROS 2 Topic
      │
      ▼
Mission Subscriber
      │
      ▼
Mission Executor
      │
      ▼
Route File
      │
      ▼
Nav2
      │
      ▼
Robot Motion
```

---

# Package Organization

```
robot_ai_mission_planner/

mission_llm/
    ollama_planner.py
    rule_based_planner.py
    prompts.py

executor/
    mission_executor.py

validator/
    json_validator.py

interfaces/
    mission_schema.py

mission_publisher.py
mission_subscriber.py
executor_node.py
route_recorder.py
initial_pose_publisher.py
```

Each module has a clearly defined responsibility, promoting modularity and maintainability.

---

# Design Principles

The architecture follows several software engineering principles:

- **Modularity** – Each component has a single responsibility.
- **Loose Coupling** – Planning and execution communicate only through ROS 2 topics.
- **Extensibility** – New planners, mission types, or robots can be added with minimal changes.
- **Validation First** – Every mission is validated before execution.
- **Reusability** – Navigation routes are stored separately and reused across missions.
- **ROS 2 Native** – Communication leverages standard ROS 2 publishers, subscribers, and the Nav2 navigation framework.

---

# Advantages of the Architecture

- Separates AI planning from robot control.
- Supports both LLM-based and rule-based mission generation.
- Enables reusable mission routes.
- Simplifies testing of individual components.
- Compatible with additional robots by replacing only the execution layer.
- Easily extendable to support manipulation, perception, or multi-robot coordination in future versions.
