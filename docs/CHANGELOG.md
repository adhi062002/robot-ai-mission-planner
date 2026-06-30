# Changelog

All notable changes to this project are documented here.

---

## Version 0.4.0 (Current)

### Added
- Project folder structure
- Git repository initialization
- GitHub repository integration using SSH
- Docker development environment (under development)
- Prompt-based mission input
- Rule-based mission parser
- Mission JSON generation
- Mission schema validation
- Deterministic mission executor
- ROS2 mission interface
- ROS2 publisher
- ROS2 subscriber test node

### Implemented Pipeline

Prompt
↓

Mission Parser

↓

Mission JSON

↓

Mission Validator

↓

Mission Executor

↓

ROS2 Publisher

↓

Mission Listener

### Documentation
- README.md
- architecture.md
- development_log.md

### Status

✅ Prompt parsing working

✅ JSON generation working

✅ Validation working

✅ Deterministic execution working

✅ ROS2 communication verified

⬜ Gazebo integration

⬜ Nav2 waypoint execution

⬜ LLM API integration

---

## Planned (Phase 5)

- Nav2 integration
- Waypoint navigation
- TurtleBot3 execution
- Gazebo simulation
