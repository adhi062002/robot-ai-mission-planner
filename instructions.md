# Robot AI Mission Planner - Instructions

This document explains how to set up and run the Robot AI Mission Planner demonstration.

---

# 1. Make the Setup Script Executable

Open a terminal in the project directory and run:

```bash
chmod +x setup.sh
```

---

# 2. Run the Setup Script

Execute the setup script:

```bash
./setup.sh
```

The setup script will:

- Install the required dependencies (if not already installed).
- Build the Docker images.
- Pull the required Ollama model (`llama3.2:latest`).
- Prepare the environment for running the simulation.

> **Note:** The setup process may take several minutes depending on your internet connection and system performance.

---

# 3. Start the Simulation

After the setup completes, start the simulation:

```bash
xhost +local:docker

docker compose up robot-sim
```

### First Startup

On the first launch, Gazebo may take some time to initialize. During this process you may see messages similar to:

```
Waiting for service /spawn_entity
Service /spawn_entity unavailable
Spawn service failed
```

This is expected during the initial startup.

Wait until Gazebo finishes loading and an **empty Gazebo world** appears.

Once Gazebo has fully opened:

1. Press **Ctrl + C** to stop the container.
2. Start it again:

```bash
docker compose up robot-sim
```

On the second launch, Gazebo initializes correctly, the TurtleBot3 robot is spawned, and RViz starts automatically.

---

# 4. Publish the Initial Pose

Open a new terminal and enter the running container:

```bash
docker exec -it $(docker compose ps -q robot-sim) bash
```

Run:

```bash
ros2 run robot_ai_mission_planner initial_pose_publisher
```

---

# 5. Start the Mission Executor

Open another terminal.

Enter the container:

```bash
docker exec -it $(docker compose ps -q robot-sim) bash
```

Run:

```bash
ros2 run robot_ai_mission_planner mission_executor
```

---

# 6. Start the Mission Planner

Open another terminal.

Enter the container:

```bash
docker exec -it $(docker compose ps -q robot-sim) bash
```

Run:

```bash
ros2 run robot_ai_mission_planner mission_planner
```

---

# 7. Execute a Mission

When prompted, enter a command such as:

```
patrol the perimeter
```

The first request may take several seconds while the Ollama model loads into memory.

The system will then:

- Interpret the natural language command.
- Generate a mission JSON.
- Validate the mission.
- Publish the mission over ROS 2.
- Execute the mission using Nav2.
- Navigate the robot through the predefined waypoint route in Gazebo.

Mission progress can be observed in the terminal windows, RViz, and the Gazebo simulation.

---

# 8. Create a Custom Route (Optional)

The project also includes a waypoint recording utility.

Run:

```bash
ros2 run robot_ai_mission_planner route_recorder
```

## Controls

| Key | Action |
|------|--------|
| **W** | Move forward |
| **A** | Turn left |
| **S** | Move backward |
| **D** | Turn right |
| **V** | Save the current waypoint |
| **Q** | Save the route and exit |

The generated waypoint file can be reused in future missions.

---

# Expected Result

A successful demonstration should show:

- Docker containers start successfully.
- Gazebo launches with the TurtleBot3 robot.
- RViz opens.
- The initial pose is published.
- The Mission Planner accepts a natural language command.
- A structured mission JSON is generated.
- The Mission Executor receives the mission.
- Nav2 executes the waypoint route.
- The robot successfully completes the requested mission.

