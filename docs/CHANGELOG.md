# Changelog

All notable changes to the Robot AI Mission Planner project are documented in this file.

The project follows a simple versioning approach to record major features and improvements introduced during development.

---

## [1.0.0] - Initial Release

### Added

#### Project Foundation

- Created ROS 2 workspace and package structure.
- Configured Python package and build system.
- Added launch files for system execution.
- Organized mission and resource directories.

#### Mission Planning

- Implemented natural language mission planning.
- Integrated Ollama-based Large Language Model (LLM).
- Added rule-based planner as a fallback.
- Implemented prompt template management.
- Generated structured mission JSON.

#### Mission Validation

- Designed mission schema.
- Implemented JSON validation.
- Added validation checks for required fields and supported action types.
- Improved error handling for invalid missions.

#### ROS 2 Communication

- Implemented mission publisher.
- Implemented mission subscriber.
- Added JSON serialization and deserialization.
- Enabled topic-based communication between planning and execution components.

#### Mission Execution

- Developed Mission Executor.
- Added waypoint loading from predefined route files.
- Implemented sequential waypoint navigation.
- Integrated mission completion handling.

#### Navigation

- Integrated ROS 2 Navigation2 (Nav2).
- Added autonomous navigation goal execution.
- Connected mission execution with the Nav2 action server.

#### Route Management

- Implemented Route Recorder utility.
- Added waypoint recording.
- Enabled reusable JSON route files.

#### Simulation

- Integrated Gazebo simulation.
- Added TurtleBot3 support.
- Implemented initial pose publisher.
- Configured complete launch pipeline.

#### Documentation

- Added architecture documentation.
- Documented design decisions.
- Recorded development milestones.
- Added project progress report.
- Created future development roadmap.

---

## Current Capabilities

The current release supports:

- Natural language mission planning
- Structured mission generation
- JSON validation
- ROS 2 topic communication
- Autonomous navigation using Nav2
- Waypoint-based mission execution
- Route recording
- Gazebo simulation
- Modular ROS 2 architecture

---

## Planned Enhancements

Future releases are expected to introduce:

- Dynamic mission generation
- Multi-step missions
- Object detection integration
- Dynamic waypoint generation
- Multi-robot coordination
- Real robot deployment
- Enhanced natural language understanding
- Advanced mission planning strategies

---

## Version Summary

| Version | Description |
|----------|-------------|
| **1.0.0** | Initial public implementation of the Robot AI Mission Planner with complete end-to-end autonomous mission execution in ROS 2 and Gazebo. |
