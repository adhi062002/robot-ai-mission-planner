# Design Decisions

## Overview

This document outlines the key design decisions made during the development of the Robot AI Mission Planner. The primary objectives were to create a modular, extensible, and maintainable system that integrates natural language understanding with autonomous robot navigation in a ROS 2 environment.

---

# 1. ROS 2 as the Middleware

## Decision

ROS 2 was selected as the communication framework for the project.

## Rationale

ROS 2 provides:

- Standardized communication through topics, services, and actions
- Native support for distributed robotic systems
- Integration with the Navigation2 (Nav2) stack
- Scalability for future expansion
- A large ecosystem of robotics packages

Using ROS 2 also enables the planner, executor, and navigation components to operate independently while communicating through well-defined interfaces.

---

# 2. Modular System Architecture

## Decision

The project was divided into independent modules, each responsible for a single task.

Modules include:

- Mission Planner
- JSON Validator
- Mission Publisher
- Mission Subscriber
- Mission Executor
- Route Recorder

## Rationale

A modular architecture offers several benefits:

- Easier debugging
- Better maintainability
- Independent testing of components
- Future extensibility
- Separation of responsibilities

Changes to one module have minimal impact on the rest of the system.

---

# 3. JSON-Based Mission Representation

## Decision

Robot missions are represented using structured JSON objects.

Example:

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

## Rationale

JSON provides:

- Human-readable formatting
- Easy serialization and deserialization
- Compatibility with LLM outputs
- Simple validation
- Language-independent data exchange

Using JSON also allows missions to be stored, modified, and replayed easily.

---

# 4. LLM-Based Mission Planning

## Decision

Natural language instructions are interpreted using an LLM (Ollama), with a rule-based planner available as a fallback.

## Rationale

The LLM enables flexible interaction with the robot by allowing users to issue commands in natural language rather than predefined keywords.

The rule-based planner ensures that the system remains functional if the LLM is unavailable or if deterministic behavior is required for testing.

This hybrid approach improves both usability and reliability.

---

# 5. Validation Before Execution

## Decision

Every generated mission is validated before execution.

## Rationale

Mission validation prevents malformed or incomplete commands from reaching the robot.

Validation checks include:

- Required fields
- Data types
- Supported action types
- Overall JSON structure

This improves system robustness and reduces runtime failures.

---

# 6. ROS 2 Topic-Based Communication

## Decision

Mission planning and execution communicate through ROS 2 topics.

## Rationale

Using publish-subscribe communication provides:

- Loose coupling
- Asynchronous message passing
- Independent execution of nodes
- Easier system testing

The planner does not need direct knowledge of the executor implementation.

---

# 7. Predefined Navigation Routes

## Decision

Robot navigation is based on predefined waypoint files.

## Rationale

Instead of generating arbitrary navigation goals from natural language, the planner selects from predefined routes such as:

- warehouse_route
- inspection_loop
- perimeter_loop

This approach offers:

- Predictable robot behavior
- Simplified mission planning
- Easier testing
- Reusable navigation paths

---

# 8. Navigation2 (Nav2) for Motion Planning

## Decision

The project uses the ROS 2 Navigation Stack (Nav2) for autonomous navigation.

## Rationale

Nav2 provides:

- Global path planning
- Local path planning
- Obstacle avoidance
- Recovery behaviors
- Goal management

Using Nav2 avoids reimplementing well-established navigation algorithms and ensures compatibility with standard ROS 2 robots.

---

# 9. Route Recording Utility

## Decision

A dedicated route recorder was implemented for capturing navigation paths.

## Rationale

Recording routes directly from robot movement simplifies the creation of reusable missions and reduces manual editing of waypoint files.

This also enables rapid deployment of new routes without modifying the planner.

---

# 10. Separation of Planning and Execution

## Decision

Mission planning and mission execution are implemented as separate components.

## Rationale

Separating these responsibilities improves flexibility.

The planner focuses solely on understanding user intent and generating structured missions, while the executor is responsible for interacting with the robot and Nav2.

This separation makes it possible to replace either component independently in future versions.

---

# 11. Scalability Considerations

The architecture was designed with future expansion in mind.

Potential extensions include:

- Multi-action missions
- Dynamic waypoint generation
- Object detection integration
- Multi-robot coordination
- Manipulation tasks
- Cloud-based planning services

The modular design minimizes changes required to support these features.

---

# Summary

The design decisions prioritize:

- Modularity
- Reliability
- Maintainability
- Reusability
- Extensibility

By combining ROS 2, structured mission representation, LLM-based planning, and Nav2 navigation, the project provides a flexible foundation for autonomous mission execution while remaining straightforward to extend and maintain.
