# Robot AI Mission Planner

## Objective

Develop a robotics software pipeline that converts natural language instructions into deterministic robot actions inside a simulated environment.

The architecture follows the assignment specification:

Prompt
        │
        ▼
Language Model (LLM)
        │
        ▼
Mission JSON
        │
        ▼
Mission Validator
        │
        ▼
Deterministic Executor
        │
        ▼
ROS2 / Nav2
        │
        ▼
Gazebo Simulator

---

## Architecture Philosophy

The LLM never directly controls the robot.

Instead, it only interprets the user's intent and generates a structured mission description.

The Executor is solely responsible for controlling the robot.

This ensures:

- Deterministic execution
- Safety
- Auditability
- Easy debugging

---

## Current Software Modules

src/

mission_llm/
    Converts natural language into Mission JSON.

validator/
    Validates Mission JSON.

executor/
    Executes validated missions.

interfaces/
    Stores shared schemas.

missions/
    Stores predefined robot routes.

---

## Current Mission Flow

Prompt

↓

MissionLLM

↓

Mission JSON

↓

Validator

↓

Executor

↓

Route File

↓

Waypoints

↓

(ROS2 Integration - Upcoming)

---

## Planned Final Flow

Prompt

↓

LLM API

↓

Mission JSON

↓

Validator

↓

Executor

↓

ROS2 Action Client

↓

Nav2

↓

Gazebo TurtleBot3