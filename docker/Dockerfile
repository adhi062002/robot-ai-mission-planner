FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    git \
    nano \
    vim \
    wget \
    curl \
    tree \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["bash"]
