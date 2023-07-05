import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, EnvironmentVariable


def generate_launch_description():
    # Define launch arguments
    world_file = LaunchConfiguration(
        "world_file",
        default=os.path.join(
            get_package_share_directory("jotham_s_mobile_bot"),
            "worlds",
            "test_world_1.world",
        ),
    )

    map_file = LaunchConfiguration(
        "map_file",
        default=os.path.join(
            os.getcwd(),
            "src",
            "Jotham-Prince-Jotham-s_mobile_bot-0599f03",
            "config",
            "my_map.yaml",
        ),
    )

    # Define environment variables
    use_sim_time = EnvironmentVariable("use_sim_time", default_value="true")

    # Declare launch arguments
    declare_world_file = DeclareLaunchArgument(
        "world_file",
        default_value=world_file,
        description="/home/jotham-prince/Desktop/Robotics/dev_ws/src/Jotham-Prince-Jotham-s_mobile_bot-0599f03/worlds",
    )
    declare_map_file = DeclareLaunchArgument(
        "map_file",
        default_value=map_file,
        description="/home/jotham-prince/Desktop/Robotics/dev_ws",
    )

    # Launch teleop_twist_keyboard
    teleop_keyboard = ExecuteProcess(
        cmd=["ros2", "run", "teleop_twist_keyboard", "teleop_twist_keyboard"],
        output="screen",
    )

    # Launch jotham_s_mobile_bot
    launch_sim = ExecuteProcess(
        cmd=[
            "ros2",
            "launch",
            "jotham_s_mobile_bot",
            "launch_sim.launch.py",
            f"world:={world_file}",
        ],
        output="screen",
    )

    # Launch nav2_map_server
    map_server = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "nav2_map_server",
            "map_server",
            "--ros-args",
            "-p",
            f"yaml_filename:={map_file}",
            "-p",
            "use_sim_time:=true",
        ],
        output="screen",
    )

    # Launch nav2_map_server_activator
    map_server_activator = ExecuteProcess(
        cmd=["ros2", "run", "nav2_util", "lifecycle_bringup", "map_server"],
        output="screen",
    )

    # Launch nav2_amcl
    amcl = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "nav2_amcl",
            "amcl",
            "--ros-args",
            "-p",
            f"use_sim_time:={use_sim_time}",
        ],
        output="screen",
    )

    # Launch nav2_amcl_activator
    amcl_activator = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "nav2_util",
            "lifecycle_bringup",
            "amcl",
        ],
        output="screen",
    )

    # Launch twist_mux
    twist_mux = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "twist_mux",
            "twist_mux",
            "--ros-args",
            f"--params-file",
            "./src/Jotham-Prince-Jotham-s_mobile_bot-0599f03/config/twist_mux.yaml",
            "-r",
            "cmd_vel_out:=merged_cmd_vel",
        ],
        output="screen",
    )

    # Launch nav2_bringup
    navigation = ExecuteProcess(
        cmd=[
            "ros2",
            "launch",
            "nav2_bringup",
            "navigation_launch.py",
            f"use_sim_time:={use_sim_time}",
            "cmd_vel:=/nav2/cmd_vel",
        ],
        output="screen",
    )

    # Create launch description
    ld = LaunchDescription()

    # Add actions to the launch description
    ld.add_action(declare_world_file)
    ld.add_action(declare_map_file)
    ld.add_action(teleop_keyboard)
    ld.add_action(launch_sim)
    ld.add_action(map_server)
    ld.add_action(map_server_activator)
    ld.add_action(amcl)
    ld.add_action(amcl_activator)
    ld.add_action(twist_mux)
    ld.add_action(navigation)

    return ld


if __name__ == "__main__":
    generate_launch_description()
