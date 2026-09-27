from typing import Dict, Any, List
import numpy as np

from solver import simulate_braking


def build_scenarios(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    aero = params["aerodynamics"]
    aircraft = params["aircraft"]
    friction = params["friction"]
    env = params["environment"]
    sim = params["simulation"]

    common = {
        "m": aircraft["mass_kg"],
        "g": env["g"],
        "rho": env["rho"],
        "Cz": aero["Cz"],
        "S": aircraft["wing_area_m2"],
        "mu_dry": friction["mu_dry"],
        "mu_wet": friction["mu_wet"],
        "tire_pressure_pa": aircraft["tire_pressure_pa"],
        "v0": sim["v0_ms"],
        "dt": sim["dt_s"],
    }

    return [
        {"name": "Dry - airbrakes deployed", "etat": "sec", "Cx": aero["Cx_airbrakes"], "params": common},
        {"name": "Dry - airbrakes retracted", "etat": "sec", "Cx": aero["Cx_clean"], "params": common},
        {"name": "Wet - airbrakes deployed", "etat": "mouille", "Cx": aero["Cx_airbrakes"], "params": common},
        {"name": "Hydroplaning - airbrakes deployed", "etat": "aquaplaning", "Cx": aero["Cx_airbrakes"], "params": common},
        {"name": "Wet - airbrake failure (worst case)", "etat": "mouille", "Cx": aero["Cx_clean"], "params": common},
    ]


def run_scenarios(scenarios: List[Dict[str, Any]]) -> Dict[str, Dict[str, np.ndarray]]:
    results: Dict[str, Dict[str, np.ndarray]] = {}

    for sc in scenarios:
        p = sc["params"]
        t, x, v, a = simulate_braking(
            v0=p["v0"],
            dt=p["dt"],
            m=p["m"],
            g=p["g"],
            rho=p["rho"],
            Cz=p["Cz"],
            Cx=sc["Cx"],
            S=p["S"],
            etat=sc["etat"],
            mu_dry=p["mu_dry"],
            mu_wet=p["mu_wet"],
            tire_pressure_pa=p["tire_pressure_pa"],
        )
        results[sc["name"]] = {"t": t, "x": x, "v": v, "a": a}

    return results