import csv
import math

import matplotlib.pyplot as plt


CSV_FILE = "proportional_tracking_5s.csv"


def main() -> None:
    times = []
    desired = []
    actual = []
    errors = []

    with open(CSV_FILE, newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            times.append(float(row["time_s"]))
            desired.append(float(row["desired_deg"]))
            actual.append(float(row["actual_deg"]))
            errors.append(float(row["error_deg"]))

    rms_error = math.sqrt(sum(error**2 for error in errors) / len(errors))
    max_error = max(abs(error) for error in errors)
    mean_abs_error = sum(abs(error) for error in errors) / len(errors)

    print(f"RMS tracking error:     {rms_error:.3f}°")
    print(f"Mean absolute error:    {mean_abs_error:.3f}°")
    print(f"Maximum absolute error: {max_error:.3f}°")

    plt.figure()
    plt.plot(times, desired, label="Desired angle")
    plt.plot(times, actual, label="Measured angle")
    plt.xlabel("Time (s)")
    plt.ylabel("Base angle (degrees)")
    plt.title("SO-101 Base Joint Sine-Wave Tracking")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("sine_tracking_plot.png", dpi=200)
    plt.show()

    plt.figure()
    plt.plot(times, errors)
    plt.xlabel("Time (s)")
    plt.ylabel("Tracking error (degrees)")
    plt.title("SO-101 Base Joint Tracking Error")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("sine_tracking_error_plot.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
