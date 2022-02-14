import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
import launch_ros


def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_sdnova = get_package_share_directory('sdnova_simulation')
    model_path = os.path.join(pkg_sdnova, 'urdf/sdnova.urdf')

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', model_path])}]
    )
    spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'sdnova', '-topic',
                   'robot_description', '-z', '0.6'],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true',
                              description='Set to "false" to run headless.'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
            ), condition=IfCondition(LaunchConfiguration('gui'))
        ),
        robot_state_publisher_node,
        spawn_entity
    ])
