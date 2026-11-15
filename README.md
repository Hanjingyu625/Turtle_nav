# Turtle_nav

ROS 2 turtlesim의 거북이를 목표 좌표까지 이동시키는 Python 패키지입니다. 목표 좌표 발행, 이동 제어, 도착 상태 모니터링 노드로 구성됩니다.

## 실행 환경

- Ubuntu 24.04 / ROS 2 Jazzy (`/opt/ros/jazzy`에 설치)
- Bash 터미널 (Windows에서는 WSL Ubuntu 터미널)
- turtlesim 창을 표시할 GUI 환경 (WSL에서는 WSLg 등)

## 1. 의존성 설치

ROS 2 Jazzy가 설치된 상태에서 실행합니다.

```bash
sudo apt update
sudo apt install python3-colcon-common-extensions ros-jazzy-turtlesim ros-jazzy-geometry-msgs ros-jazzy-std-msgs ros-jazzy-rclpy ros-jazzy-launch-ros ros-jazzy-rmw-cyclonedds-cpp
```

## 2. 저장소 다운로드

처음 다운로드할 때만 실행하세요. 이미 `~/ros2_ws`에서 작업 중이라면 건너뛰세요.

```bash
git clone https://github.com/Hanjingyu625/Turtle_nav.git ~/ros2_ws
cd ~/ros2_ws
```

저장소 자체가 워크스페이스이며 패키지는 `src/turtle_nav`에 있습니다. 기존 `~/ros2_ws` 폴더가 있다면 다른 빈 경로에 클론하고 이후 명령의 경로도 바꾸세요.

## 3. 빌드

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select turtle_nav
source install/setup.bash
```

`build/`, `install/`, `log/`는 빌드 시 생성되며 Git 업로드 대상에서 제외됩니다.

## 4. 실행

새 터미널을 열 때마다 아래 환경 설정을 먼저 실행하세요. 같은 컴퓨터에서 실행하는 turtlesim을 위한 설정입니다.

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
unset FASTRTPS_DEFAULT_PROFILES_FILE FASTDDS_DEFAULT_PROFILES_FILE FASTDDS_BUILTIN_TRANSPORTS

ros2 launch turtle_nav turtle_nav.launch.py
```

turtlesim 창과 세 개의 노드가 함께 실행됩니다. 거북이는 기본 목표 `(8.0, 8.0)`으로 이동하며 터미널에 현재 좌표, 목표 거리, `MOVING` / `ARRIVED` 상태가 출력됩니다. 종료하려면 `Ctrl+C`를 누르세요.

목표 좌표를 지정하려면 기본 실행 명령 대신 다음을 사용하세요.

```bash
ros2 launch turtle_nav turtle_nav.launch.py goal_x:=3.0 goal_y:=7.0
```

목표는 turtlesim 화면 안의 좌표로 지정하세요.

## 5. 실행 중 목표 변경

다른 터미널에서 위의 환경 설정을 동일하게 적용한 뒤 실행합니다.

```bash
ros2 param set /goal_publisher goal_x 2.0
ros2 param set /goal_publisher goal_y 3.0
```

목표 좌표는 0.5초마다 다시 읽어 발행됩니다. 두 명령은 순서대로 적용되므로 잠시 중간 좌표를 향할 수 있습니다.

## 주요 노드

| 노드 | 역할 |
| --- | --- |
| `goal_publisher` | `/goal`로 목표 좌표 발행 |
| `turtle_controller` | 현재 위치와 목표를 받아 `/turtle1/cmd_vel`로 이동 명령 발행 |
| `status_monitor` | 현재 좌표, 목표 거리, 도착 상태 출력 |

## 실행이 안 될 때

- `Package 'turtle_nav' not found`: 빌드 성공 여부를 확인하고 현재 터미널에서 `source ~/ros2_ws/install/setup.bash`를 실행하세요.
- Cyclone DDS 라이브러리 오류: `ros-jazzy-rmw-cyclonedds-cpp` 설치 여부를 확인하세요.
- turtlesim 창이 뜨지 않음: GUI/WSLg 환경과 `DISPLAY` 설정을 확인하세요.
- 노드 사이 통신이 안 됨: 모든 터미널에서 동일한 ROS 및 DDS 환경 설정을 적용하세요.

`turtle_nav_local.bash`에는 작성자의 절대 경로(`/home/h8987/ros2_ws`)가 들어 있습니다. 다른 환경에서는 위의 명령을 사용하거나 스크립트 경로를 자신의 워크스페이스에 맞게 수정하세요.
