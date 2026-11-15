
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # 실행할 때 지정할 수 있는 목표 좌표
    goal_x = LaunchConfiguration('goal_x')
    goal_y = LaunchConfiguration('goal_y')

    return LaunchDescription([
        # 목표 좌표 기본값
        DeclareLaunchArgument(
            'goal_x',
            default_value='8.0',
            description='Target X coordinate'
        ),

        DeclareLaunchArgument(
            'goal_y',
            default_value='8.0',
            description='Target Y coordinate'
        ),

        # 1. turtlesim 실행
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),

        # 2. 목표 좌표 발행 노드
        Node(
            package='turtle_nav',
            executable='goal_publisher',
            name='goal_publisher',
            parameters=[{
                'goal_x': ParameterValue(
                    goal_x, value_type=float
                ),
                'goal_y': ParameterValue(
                    goal_y, value_type=float
                )
            }],
            output='screen'
        ),

        # 3. 거북이 제어 노드
        Node(
            package='turtle_nav',
            executable='turtle_controller',
            name='turtle_controller',
            output='screen'
        ),

        # 4. 상태 모니터 노드
        Node(
            package='turtle_nav',
            executable='status_monitor',
            name='status_monitor',
            output='screen'
        )
    ])
