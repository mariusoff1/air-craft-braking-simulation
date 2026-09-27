from typing import Dict, Any, List
import numpy as np


def extract_metrics(scenario_name: str, series: Dict[str, np.ndarray], params: Dict[str, Any]) -> Dict[str, Any]:
    t, x, v, a = series["t"], series["x"], series["v"], series["a"]

    stopping_distance = float(x[-1])
    stopping_time = float(t[-1])
    mean_deceleration = float(np.mean(np.abs(a)))
    peak_deceleration = float(abs(np.min(a)))

    hydroplaning_occurred = False
    if "hydroplaning" in scenario_name.lower():
        p_psi = params["aircraft"]["tire_pressure_pa"] / 6894.76
        v_threshold_kmh = 9.0 * (p_psi ** 0.5)
        v_threshold_ms = v_threshold_kmh / 3.6
        hydroplaning_occurred = bool(np.max(v) >= v_threshold_ms)

    return {
        "scenario": scenario_name,
        "stopping_distance_m": stopping_distance,
        "stopping_time_s": stopping_time,
        "mean_deceleration_ms2": mean_deceleration,
        "peak_deceleration_ms2": peak_deceleration,
        "hydroplaning_occurred": hydroplaning_occurred,
    }


def compute_comparison(metrics_list: List[Dict[str, Any]], reference_name: str) -> List[Dict[str, Any]]:
    ref = None
    for m in metrics_list:
        if m["scenario"] == reference_name:
            ref = m
            break

    if ref is None:
        raise ValueError(f"Reference scenario '{reference_name}' not found.")

    ref_distance = ref["stopping_distance_m"]
    ref_time = ref["stopping_time_s"]

    for m in metrics_list:
        m["distance_vs_ref_pct"] = ((m["stopping_distance_m"] - ref_distance) / ref_distance) * 100.0
        m["time_vs_ref_pct"] = ((m["stopping_time_s"] - ref_time) / ref_time) * 100.0

    return metrics_list


def print_comparison_table(metrics_list: List[Dict[str, Any]], reference_name: str) -> None:
    header = (f"{'Scenario':<45} {'Dist (m)':>10} {'Time (s)':>10} "
              f"{'Mean decel (m/s2)':>18} {'Peak decel (m/s2)':>18} "
              f"{'Delta dist vs ref (%)':>22}")
    separator = "-" * len(header)

    print(f"\nComparison table — reference: {reference_name}\n")
    print(header)
    print(separator)

    for m in metrics_list:
        flag = " [HYDROPLANING]" if m["hydroplaning_occurred"] else ""
        print(f"{m['scenario']:<45} "
              f"{m['stopping_distance_m']:>10.1f} "
              f"{m['stopping_time_s']:>10.2f} "
              f"{m['mean_deceleration_ms2']:>18.3f} "
              f"{m['peak_deceleration_ms2']:>18.3f} "
              f"{m['distance_vs_ref_pct']:>+22.1f}"
              f"{flag}")

    print(separator)
    print()