from setuptools import find_packages, setup

package_name = 'robot_ai_mission_planner'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Adithya Satheesh',
    maintainer_email='adithya062002@gmail.com',
    description='AI Mission Planner for ROS2 Mobile Robots',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'mission_planner = robot_ai_mission_planner.main:main',
        ],
    },
)
