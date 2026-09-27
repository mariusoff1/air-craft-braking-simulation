import json
import os
import sys
from typing import Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from scenarios import build_scenarios, run_scenarios
from analysis import extract_metrics, compute_comparison, print_comparison_table
from plotting import generate_all_figures
from advisor import assess_runway_safety, print_safety_report


def load_params(filepath: str = "data/aircraft_params.json") -> Dict[str, Any]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    params = load_params()

    scenarios = build_scenarios(params)
    results = run_scenarios(scenarios)

    metrics_list = []
    for name, series in results.items():
        m = extract_metrics(name, series, params)
        metrics_list.append(m)

    reference = "Dry - airbrakes deployed"
    metrics_list = compute_comparison(metrics_list, reference)

    print_comparison_table(metrics_list, reference)

    created_files = generate_all_figures(results, output_dir="figures")
    print(f"Figures generated: {created_files}")

    assessments = {}
    for m in metrics_list:
        assessments[m["scenario"]] = assess_runway_safety(m["stopping_distance_m"], params)

    print_safety_report(assessments)


if __name__ == "__main__":
    main()