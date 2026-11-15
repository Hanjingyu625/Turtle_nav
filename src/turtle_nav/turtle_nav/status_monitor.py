
import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from turtlesim.msg import Pose
from std_msgs.msg import Bool


class StatusMonitor(Node):
    def __init__(self):
        super().__init__('status_monitor')

        self.pose = None
        self.goal = None
        self.reached = False

        # 현재 위치 구독
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # 목표 위치 구독
        self.goal_sub = self.create_subscription(
            Point,
            '/goal',
            self.goal_callback,
            10
        )

        # 목표 도착 여부 구독
        self.status_sub = self.create_subscription(
            Bool,
            '/goal_reached',
            self.status_callback,
            10
        )

        # 1초마다 현재 상태 출력
        self.timer = self.create_timer(
            1.0, self.print_status
        )

        self.get_logger().info('Status monitor started')

    def pose_callback(self, msg):
        self.pose = msg

    def goal_callback(self, msg):
        self.goal = msg

    def status_callback(self, msg):
        self.reached = msg.data

    def print_status(self):
        if self.pose is None or self.goal is None:
            return

        dx = self.goal.x - self.pose.x
        dy = self.goal.y - self.pose.y

        distance = math.hypot(dx, dy)

        if self.reached:
            state = 'ARRIVED'
        else:
            state = 'MOVING'

        self.get_logger().info(
            f'Current: ({self.pose.x:.2f}, {self.pose.y:.2f}) | '
            f'Goal: ({self.goal.x:.2f}, {self.goal.y:.2f}) | '
            f'Distance: {distance:.3f} | '
            f'Status: {state}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = StatusMonitor()

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
