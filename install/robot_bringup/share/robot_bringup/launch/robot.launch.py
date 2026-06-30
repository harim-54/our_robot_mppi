import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # 설정 파일 경로
    mppi_params = os.path.join(
        get_package_share_directory('robot_bringup'),
        'config', 'our_mppi_params.yaml')

    ekf_params = os.path.join(
        get_package_share_directory('robot_bringup'),
        'config', 'ekf_params.yaml')

    return LaunchDescription([

        # 1. CAN 드라이버 노드
        Node(
            package='our_can_driver',
            executable='can_driver_node',
            name='can_driver',
            parameters=[{
                'can_interface': 'can0',
                'left_motor_id': 1,
                'right_motor_id': 2,
                'track_width': 0.4904,
                'wheel_radius': 0.225,
                'gear_ratio': 6.0,
            }],
            output='screen',
        ),

        # 2. 휠 오도메트리 노드
        Node(
            package='our_can_driver',
            executable='wheel_odom_node',
            name='wheel_odom',
            parameters=[{
                'track_width': 0.4904,
                'wheel_radius': 0.225,
                'gear_ratio': 6.0,
            }],
            output='screen',
        ),

        # 3. EKF 노드 (robot_localization)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_node',
            parameters=[ekf_params],
            output='screen',
        ),

        # 4. Nav2 MPPI 컨트롤러
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            parameters=[mppi_params],
            output='screen',
        ),

    ])