
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point


class GoalPublisher(Node):
    def __init__(self):
        super().__init__('goal_publisher')

        # 목표 좌표를 ROS 2 파라미터로 선언
        self.declare_parameter('goal_x', 8.0)
        self.declare_parameter('goal_y', 8.0)

        self.goal_x = float(self.get_parameter('goal_x').value)
        self.goal_y = float(self.get_parameter('goal_y').value)

        # /goal 토픽에 Point 메시지를 발행할 Publisher
        self.publisher = self.create_publisher(
            Point, '/goal', 10
        )

        # 0.5초마다 목표 좌표 발행
        self.timer = self.create_timer(
            0.5, self.publish_goal
        )

        self.get_logger().info(
            f'Goal set to ({self.goal_x:.2f}, {self.goal_y:.2f})'
        )

    def publish_goal(self):
        # Read current parameters so runtime changes reach the goal topic.
        self.goal_x = float(self.get_parameter('goal_x').value)
        self.goal_y = float(self.get_parameter('goal_y').value)
        msg = Point()

        msg.x = self.goal_x
        msg.y = self.goal_y
        msg.z = 0.0

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GoalPublisher()

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
