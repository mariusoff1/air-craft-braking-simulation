from typing import Dict, Any, List
import os
import matplotlib.pyplot as plt
import numpy as np


def plot_speed_time(results: Dict[str, Dict[str, np.ndarray]], filename: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, series in results.items():
        ax.plot(series["t"], series["v"], label=name, linewidth=1.5)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Speed (m/s)")
    ax.set_title("Braking — Speed evolution")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(filename, dpi=300)
    plt.close(fig)


def plot_distance_time(results: Dict[str, Dict[str, np.ndarray]], filename: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, series in results.items():
        ax.plot(series["t"], series["x"], label=name, linewidth=1.5)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Distance traveled (m)")
    ax.set_title("Braking — Distance traveled")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(filename, dpi=300)
    plt.close(fig)


def plot_deceleration_time(results: Dict[str, Dict[str, np.ndarray]], filename: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, series in results.items():
        ax.plot(series["t"], np.abs(series["a"]), label=name, linewidth=1.5)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Deceleration |a| (m/s²)")
    ax.set_title("Braking — Deceleration")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(filename, dpi=300)
    plt.close(fig)


def generate_all_figures(results: Dict[str, Dict[str, np.ndarray]], output_dir: str = "figures") -> List[str]:
    os.makedirs(output_dir, exist_ok=True)

    files = [
        (plot_speed_time, "braking_curves.png"),
        (plot_distance_time, "distance_curves.png"),
        (plot_deceleration_time, "deceleration_curves.png"),
    ]

    created = []
    for func, fname in files:
        path = os.path.join(output_dir, fname)
        func(results, path)
        created.append(path)

    return created