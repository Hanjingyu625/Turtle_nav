
import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point, Twist
from turtlesim.msg import Pose
from std_msgs.msg import Bool


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        # 현재 위치, 목표 위치, 도착 여부
        self.pose = None
        self.goal = None
        self.arrived = False

        # 거북이 이동 명령 발행
        self.cmd_pub = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        # 목표 도착 여부 발행
        self.status_pub = self.create_publisher(
            Bool, '/goal_reached', 10
        )

        # 거북이의 현재 위치 구독
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # 목표 좌표 구독
        self.goal_sub = self.create_subscription(
            Point,
            '/goal',
            self.goal_callback,
            10
        )

        # 0.05초 간격으로 제어 명령 계산 (20 Hz)
        self.timer = self.create_timer(
            0.05, self.control_loop
        )

        self.get_logger().info('Turtle controller started')

    def pose_callback(self, msg):
        # turtlesim으로부터 받은 현재 위치 저장
        self.pose = msg

    def goal_callback(self, msg):
        # 목표가 처음 들어오거나 변경되었을 때 갱신
        new_goal = (msg.x, msg.y)

        if self.goal != new_goal:
            self.goal = new_goal
            self.arrived = False

            self.get_logger().info(
                f'New goal: ({msg.x:.2f}, {msg.y:.2f})'
            )

    def control_loop(self):
        # 현재 위치나 목표를 아직 받지 못했다면 대기
        if self.pose is None or self.goal is None:
            return

        # 현재 위치와 목표 위치의 차이 계산
        dx = self.goal[0] - self.pose.x
        dy = self.goal[1] - self.pose.y

        # 목표 지점까지의 직선거리
        distance = math.hypot(dx, dy)

        # 속도 명령 메시지 생성 (초기값은 모두 0)
        cmd = Twist()

        # 0.1 이내에 들어오면 목표 도착
        reached = distance <= 0.1

        if reached:
            if not self.arrived:
                self.get_logger().info(
                    f'Goal reached! Distance: {distance:.3f}'
                )

            # 정지 명령
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        else:
            # 목표를 바라봐야 하는 방향 계산
            target_angle = math.atan2(dy, dx)

            # 현재 방향과 목표 방향의 차이
            angle_error = target_angle - self.pose.theta

            # 각도 오차를 -pi ~ pi 범위로 정규화
            angle_error = math.atan2(
                math.sin(angle_error),
                math.cos(angle_error)
            )

            # 비례 제어로 각속도 계산
            angular_speed = 4.0 * angle_error

            # 최대 회전 속도 제한
            cmd.angular.z = max(
                -2.0, min(2.0, angular_speed)
            )

            # 방향 오차가 크면 먼저 제자리 회전
            if abs(angle_error) > 0.25:
                cmd.linear.x = 0.0
            else:
                # 목표가 가까워질수록 속도 감소
                linear_speed = 1.5 * distance

                # 최대 전진 속도 제한
                cmd.linear.x = min(2.0, linear_speed)

        # 계산한 이동 명령 발행
        self.cmd_pub.publish(cmd)

        # 목표 도착 여부 발행
        status = Bool()
        status.data = reached
        self.status_pub.publish(status)

        self.arrived = reached


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
