import csv
import math
import time

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig


FOLLOWER_PORT = "/dev/ttyACM0"  # Change if needed
FOLLOWER_ID = "my_awesome_follower_arm"

AMPLITUDE_DEG = 3.0
PERIOD_S = 5.0
DURATION_S = 20.0
CONTROL_HZ = 20.0

KP = 2.00
CSV_FILE = "proportional_tracking_5s.csv"


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
        robot.connect()

        initial_positions = {
            key: value
            for key, value in robot.get_observation().items()
            if key.endswith(".pos")
        }

        center_angle = initial_positions["shoulder_pan.pos"]
        omega = 2.0 * math.pi / PERIOD_S
        interval = 1.0 / CONTROL_HZ

        print(f"Outer-loop Kp: {KP}")
        input("Clear the workspace and press Enter to begin...")

        start_time = time.perf_counter()

        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "time_s",
                    "desired_deg",
                    "actual_deg",
                    "error_deg",
                    "commanded_deg",
                ]
            )

            while True:
                loop_start = time.perf_counter()
                elapsed = loop_start - start_time

                if elapsed >= DURATION_S:
                    break

                desired = (
                    center_angle
                    + AMPLITUDE_DEG * math.sin(omega * elapsed)
                )

                observation = robot.get_observation()
                actual = observation["shoulder_pan.pos"]
                error = desired - actual

                # Outer proportional correction
                commanded = desired + KP * error

                action = initial_positions.copy()
                action["shoulder_pan.pos"] = commanded
                robot.send_action(action)

                writer.writerow(
                    [elapsed, desired, actual, error, commanded]
                )

                print(
                    f"t={elapsed:5.2f}s | "
                    f"desired={desired:6.2f}° | "
                    f"actual={actual:6.2f}° | "
                    f"error={error:6.2f}° | "
                    f"command={commanded:6.2f}°",
                    end="\r",
                )

                remaining = interval - (
                    time.perf_counter() - loop_start
                )
                if remaining > 0:
                    time.sleep(remaining)

        print("\nExperiment complete.")

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        if robot.is_connected:
            if initial_positions is not None:
                robot.send_action(initial_positions)
                time.sleep(2.0)

            robot.disconnect()

        print(f"Data saved to {CSV_FILE}")


if __name__ == "__main__":
    main()
