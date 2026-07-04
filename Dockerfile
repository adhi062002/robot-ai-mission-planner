FROM osrf/ros:humble-desktop
RUN apt-get update && apt-get install -y \
    ros-humble-turtlebot3 \
    ros-humble-turtlebot3-simulations \
    ros-humble-gazebo-ros-pkgs \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*
ENV TURTLEBOT3_MODEL=burger
ENV GAZEBO_MODEL_PATH=/opt/ros/humble/share/turtlebot3_gazebo/models
WORKDIR /root/ros2_ws
COPY ros2_ws/src ./src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN . /opt/ros/humble/setup.sh && colcon build
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "source /root/ros2_ws/install/setup.bash" >> /root/.bashrc
COPY launch_system.py /root/launch_system.py
RUN chmod +x /root/launch_system.py
ENTRYPOINT ["python3", "/root/launch_system.py"]
