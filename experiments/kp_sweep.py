import csv
import math
import time
from pathlib import Path

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig


FOLLOWER_PORT = "/dev/ttyACM0"  # Change if the follower is currently ACM1
FOLLOWER_ID = "my_awesome_follower_arm"

GAINS = [0.0, 0.5, 1.0, 1.5, 1.75, 2.0]

AMPLITUDE_DEG = 3.0
PERIOD_S = 5.0
DURATION_S = 20.0
CONTROL_HZ = 20.0

MAX_CORRECTION_DEG = 3.0
RETURN_TIME_S = 2.0
COOLDOWN_TIME_S = 3.0

RESULTS_DIR = Path("kp_sweep_results")
SUMMARY_FILE = RESULTS_DIR / "kp_sweep_summary.csv"


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def calculate_metrics(errors: list[float]) -> tuple[float, float, float]:
    if not errors:
        raise ValueError("No tracking-error samples were recorded.")

    rms_error = math.sqrt(
        sum(error**2 for error in errors) / len(errors)
    )
    mean_absolute_error = (
        sum(abs(error) for error in errors) / len(errors)
    )
    maximum_absolute_error = max(abs(error) for error in errors)

    return rms_error, mean_absolute_error, maximum_absolute_error


def run_experiment(
    robot: SO101Follower,
    initial_positions: dict[str, float],
    center_angle: float,
    kp: float,
) -> dict[str, float]:
    interval = 1.0 / CONTROL_HZ
    angular_frequency = 2.0 * math.pi / PERIOD_S

    kp_name = str(kp).replace(".", "_")
    data_file = RESULTS_DIR / f"tracking_kp_{kp_name}.csv"

    errors: list[float] = []

    print()
    print(f"Preparing Kp = {kp}")
    print(f"Raw data will be saved to: {data_file}")

    input(
        "Confirm the workspace is clear and press Enter to begin "
        "(or press Ctrl+C to stop the sweep)..."
    )

    start_time = time.perf_counter()

    with data_file.open("w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "time_s",
                "kp",
                "desired_deg",
                "actual_deg",
                "error_deg",
                "correction_deg",
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
                + AMPLITUDE_DEG
                * math.sin(angular_frequency * elapsed)
            )

            observation = robot.get_observation()
            actual = observation["shoulder_pan.pos"]
            error = desired - actual

            correction = clamp(
                kp * error,
                -MAX_CORRECTION_DEG,
                MAX_CORRECTION_DEG,
            )
            commanded = desired + correction

            action = initial_positions.copy()
            action["shoulder_pan.pos"] = commanded
            robot.send_action(action)

            errors.append(error)

            writer.writerow(
                [
                    elapsed,
                    kp,
                    desired,
                    actual,
                    error,
                    correction,
                    commanded,
                ]
            )

            print(
                f"Kp={kp:4.2f} | "
                f"t={elapsed:5.2f}s | "
                f"desired={desired:7.2f}° | "
                f"actual={actual:7.2f}° | "
                f"error={error:6.2f}° | "
                f"command={commanded:7.2f}°",
                end="\r",
            )

            elapsed_loop_time = time.perf_counter() - loop_start
            remaining = interval - elapsed_loop_time

            if remaining > 0:
                time.sleep(remaining)

    print()

    rms_error, mean_absolute_error, maximum_absolute_error = (
        calculate_metrics(errors)
    )

    print(f"Kp {kp} completed:")
    print(f"  RMS error:          {rms_error:.3f}°")
    print(f"  Mean absolute error:{mean_absolute_error:.3f}°")
    print(f"  Maximum error:      {maximum_absolute_error:.3f}°")

    return {
        "kp": kp,
        "rms_error_deg": rms_error,
        "mean_absolute_error_deg": mean_absolute_error,
        "maximum_absolute_error_deg": maximum_absolute_error,
        "samples": len(errors),
    }


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    config = SO101FollowerConfig(
        port=FOLLOWER_PORT,
        id=FOLLOWER_ID,
        use_degrees=True,
        max_relative_target=5.0,
    )

    robot = SO101Follower(config)
    initial_positions: dict[str, float] | None = None
    results: list[dict[str, float]] = []

    try:
        print("Connecting to follower arm...")
        robot.connect()

        initial_positions = {
            key: value
            for key, value in robot.get_observation().items()
            if key.endswith(".pos")
        }

        center_angle = initial_positions["shoulder_pan.pos"]

        print(f"Connected. Base center angle: {center_angle:.2f}°")
        print(f"Gains to test: {GAINS}")
        print(
            f"Trajectory: ±{AMPLITUDE_DEG:.1f}°, "
            f"{PERIOD_S:.1f}-second period"
        )

        for index, kp in enumerate(GAINS, start=1):
            print()
            print(f"Experiment {index} of {len(GAINS)}")

            result = run_experiment(
                robot=robot,
                initial_positions=initial_positions,
                center_angle=center_angle,
                kp=kp,
            )
            results.append(result)

            print("Returning to the starting position...")
            robot.send_action(initial_positions)
            time.sleep(RETURN_TIME_S)

            if index < len(GAINS):
                print(f"Cooling down for {COOLDOWN_TIME_S:.1f} seconds...")
                time.sleep(COOLDOWN_TIME_S)

    except KeyboardInterrupt:
        print("\nSweep stopped by user.")

    finally:
        if results:
            with SUMMARY_FILE.open("w", newline="") as summary_file:
                writer = csv.DictWriter(
                    summary_file,
                    fieldnames=[
                        "kp",
                        "rms_error_deg",
                        "mean_absolute_error_deg",
                        "maximum_absolute_error_deg",
                        "samples",
                    ],
                )
                writer.writeheader()
                writer.writerows(results)

            print(f"Summary saved to {SUMMARY_FILE}")

        if robot.is_connected:
            if initial_positions is not None:
                print("Returning to the starting position...")
                robot.send_action(initial_positions)
                time.sleep(RETURN_TIME_S)

            robot.disconnect()

        print("Disconnected safely.")


if __name__ == "__main__":
    main()
