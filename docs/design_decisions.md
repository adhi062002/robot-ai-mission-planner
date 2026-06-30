# Design Decisions

---

## Decision 1

Use ROS2 Humble.

Reason

Stable LTS release with Navigation2 support.

---

## Decision 2

Use TurtleBot3 Burger.

Reason

Widely supported in ROS2.

Simple differential drive robot.

Large community support.

---

## Decision 3

Separate LLM from Robot Controller.

Reason

LLMs are probabilistic.

Robot control should be deterministic.

---

## Decision 4

Validate every Mission JSON.

Reason

Prevent invalid missions from reaching the robot.

---

## Decision 5

Use predefined routes.

Reason

The assignment specifies that the robot follows predefined paths.

The LLM selects routes but does not generate trajectories.

---

## Decision 6

Action-based Mission JSON.

Reason

Allows future extension.

Example

Navigation

Inspection

Docking

Pickup

Return Home

can all become actions.

---

## Decision 7

Modular Software Structure.

Reason

Independent testing.

Easy debugging.

Easy replacement of modules.

For example,

Mock LLM

↓

OpenAI API

can be replaced without changing Validator or Executor.