import csv
from pathlib import Path

import matplotlib.pyplot as plt


SUMMARY_FILE = Path("experiments/kp_sweep_results/kp_sweep_summary.csv")
OUTPUT_FILE = Path("images/kp_sweep_plot.png")


def main() -> None:
    gains = []
    rms_errors = []
    max_errors = []

    with SUMMARY_FILE.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            gains.append(float(row["kp"]))
            rms_errors.append(float(row["rms_error_deg"]))
            max_errors.append(float(row["maximum_absolute_error_deg"]))

    plt.figure()
    plt.plot(gains, rms_errors, marker="o", label="RMS error")
    plt.plot(gains, max_errors, marker="o", label="Maximum error")
    plt.xlabel("Outer-loop proportional gain, Kp")
    plt.ylabel("Tracking error (degrees)")
    plt.title("SO-101 Base-Joint Proportional Gain Sweep")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    plt.savefig(OUTPUT_FILE, dpi=200)
    plt.show()

    print(f"Saved graph to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
