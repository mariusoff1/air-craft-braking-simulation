from typing import Dict, Any


def assess_runway_safety(stopping_distance_m: float, params: Dict[str, Any]) -> Dict[str, Any]:
    runway = params["runway"]
    runway_length = runway["length_m"]
    safety_margin = runway["safety_margin"]

    margin_used = stopping_distance_m * safety_margin

    if stopping_distance_m > runway_length:
        status = "CRITICAL"
        message = (f"Stopping distance ({stopping_distance_m:.0f} m) exceeds "
                   f"runway length ({runway_length:.0f} m). Runway excursion likely.")

    elif margin_used > runway_length:
        status = "CAUTION"
        message = (f"Stopping distance ({stopping_distance_m:.0f} m) with safety "
                   f"margin x{safety_margin:.2f} ({margin_used:.0f} m) approaches "
                   f"the runway length ({runway_length:.0f} m). Reduced margin.")

    else:
        status = "SAFE"
        message = (f"Stopping distance ({stopping_distance_m:.0f} m) with safety "
                   f"margin x{safety_margin:.2f} ({margin_used:.0f} m) stays within "
                   f"the runway length ({runway_length:.0f} m).")

    return {
        "status": status,
        "stopping_distance_m": stopping_distance_m,
        "runway_length_m": runway_length,
        "margin_used": margin_used,
        "safety_margin": safety_margin,
        "message": message,
    }


def print_safety_report(assessments: Dict[str, Dict[str, Any]]) -> None:
    print("\nRUNWAY SAFETY REPORT\n")
    for name, assessment in assessments.items():
        status = assessment["status"]
        symbol = {"SAFE": "✓", "CAUTION": "⚠", "CRITICAL": "✗"}[status]
        print(f"{symbol} {name}")
        print(f"  {assessment['message']}\n")