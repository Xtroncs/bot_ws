import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'my_bot'

    # 1. Robot State Publisher (with sim time)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')
        ]),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )

    # 2. Gazebo Sim (empty world by default)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        # You can add a world if you want: launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # 3. Spawn the robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'my_bot',
                   '-allow_renaming', 'false'],   # optional but good
        output='screen'
    )

    # 4. ROS <-> Gazebo Bridge  (THIS WAS MISSING - Main reason teleop not working)
    gz_bridge_node = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=[
    '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
    '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
    '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
    '/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model'
    '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
    '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
],
    output='screen',
    parameters=[
        {'use_sim_time': True},
    ]
)
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        gz_bridge_node,          
    ])
