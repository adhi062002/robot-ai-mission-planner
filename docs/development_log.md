# Development Log

---

## Phase 0 — Requirement Analysis

Objective

Understand the assignment and identify all required software components.

Completed

- Studied assignment pipeline.
- Identified required architecture.
- Selected TurtleBot3 simulation.
- Selected ROS2 Humble.
- Selected Nav2.
- Selected Gazebo.

Outcome

Project architecture finalized.

---

## Phase 1 — Environment Setup

Objective

Prepare development environment.

Completed

- Verified ROS2 installation.
- Verified Gazebo installation.
- Verified Nav2 packages.
- Verified TurtleBot3 packages.
- Installed Docker.
- Configured Git.

Problems

Gazebo failed to spawn TurtleBot3.

Investigation

- Checked gazebo_ros installation.
- Verified Gazebo plugins.
- Verified libgazebo_ros_factory.so.
- Manually launched gzserver.
- Confirmed /spawn_entity service.

Decision

Avoid spending additional time debugging Gazebo because of project deadline.

---

## Phase 2 — Software Architecture

Objective

Develop software pipeline independent of simulator.

Completed

Created project structure.

Implemented

MissionLLM

Validator

Executor

Interfaces

Mission JSON generation

Testing

Verified prompt parsing.

Verified JSON validation.

Verified execution pipeline.

---

## Phase 3 — Mission Redesign

Objective

Improve mission representation.

Changes

Old Mission JSON

{
    "mission_type":"patrol",
    "route":"inspection_loop"
}

New Mission JSON

{
    "mission":"navigation",
    "actions":[
        {
            "type":"follow_route",
            "route":"inspection_loop",
            "laps":2,
            "speed":0.2
        }
    ]
}

Reason

Supports future expansion.

Added

Predefined route files.

inspection_loop.json

perimeter_loop.json

warehouse_route.json

Reason

LLM should select routes instead of generating trajectories.

Current Status

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

Route Loader

↓

Waypoint List