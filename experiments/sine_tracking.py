import csv
import math
import time

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig


FOLLOWER_PORT = "/dev/ttyACM0"  # Change to ACM1 if necessary
FOLLOWER_ID = "my_awesome_follower_arm"

AMPLITUDE_DEG = 3.0
PERIOD_S = 5.0
DURATION_S = 10.0
CONTROL_HZ = 20.0
CSV_FILE = "sine_tracking_5s.csv"


def main() -> None:
    config = SO101FollowerConfig(
        port=FOLLOWER_PORT,
        id=FOLLOWER_ID,
        use_degrees=True,
        max_relative_target=5.0,
    )

    robot = SO101Follower(config)
    initial_positions = None

    try:
        print("Connecting to follower...")
        robot.connect()

        initial_positions = {
            key: value
            for key, value in robot.get_observation().items()
            if key.endswith(".pos")
        }

        center_angle = initial_positions["shoulder_pan.pos"]

        print(f"Base center angle: {center_angle:.2f}°")
        print(f"Motion range: {center_angle - AMPLITUDE_DEG:.2f}° "
              f"to {center_angle + AMPLITUDE_DEG:.2f}°")
        input("Clear the workspace and press Enter to begin...")

        interval = 1.0 / CONTROL_HZ
        angular_frequency = 2.0 * math.pi / PERIOD_S
        start_time = time.perf_counter()

        with open(CSV_FILE, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["time_s", "desired_deg", "actual_deg", "error_deg"]
            )

            while True:
                loop_start = time.perf_counter()
                elapsed = loop_start - start_time

                if elapsed >= DURATION_S:
                    break

                desired_angle = (
                    center_angle
                    + AMPLITUDE_DEG
                    * math.sin(angular_frequency * elapsed)
                )

                action = initial_positions.copy()
                action["shoulder_pan.pos"] = desired_angle
                robot.send_action(action)

                observation = robot.get_observation()
                actual_angle = observation["shoulder_pan.pos"]
                error = desired_angle - actual_angle

                writer.writerow(
                    [elapsed, desired_angle, actual_angle, error]
                )

                print(
                    f"t={elapsed:5.2f}s | "
                    f"desired={desired_angle:7.2f}° | "
                    f"actual={actual_angle:7.2f}° | "
                    f"error={error:6.2f}°",
                    end="\r",
                )

                remaining = interval - (
                    time.perf_counter() - loop_start
                )
                if remaining > 0:
                    time.sleep(remaining)

        print("\nTrajectory complete.")

    except KeyboardInterrupt:
        print("\nStopped by user.")

    finally:
        if robot.is_connected:
            if initial_positions is not None:
                print("Returning to starting position...")
                robot.send_action(initial_positions)
                time.sleep(2.0)

            robot.disconnect()

        print(f"Disconnected safely. Data saved to {CSV_FILE}")


if __name__ == "__main__":
    main()
