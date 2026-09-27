from typing import Optional


def portance(v: float, rho: float, Cz: float, S: float) -> float:
    return 0.5 * rho * Cz * S * v**2


def trainee(v: float, rho: float, Cx: float, S: float) -> float:
    return 0.5 * rho * Cx * S * v**2


def reaction_normale(v: float, m: float, g: float, rho: float, Cz: float, S: float) -> float:
    N = m * g - portance(v, rho, Cz, S)
    return max(0.0, N)


def coefficient_frottement(etat: str, v: float, mu_dry: float, mu_wet: float, tire_pressure_pa: float) -> float:
    if etat == "sec":
        return mu_dry

    if etat == "mouille":
        return mu_wet

    if etat == "aquaplaning":
        p_psi = tire_pressure_pa / 6894.76
        v_aqua_kmh = 9.0 * (p_psi ** 0.5)
        v_kmh = v * 3.6
        return 0.02 if v_kmh >= v_aqua_kmh else mu_wet

    raise ValueError(f"État de piste inconnu : '{etat}'")