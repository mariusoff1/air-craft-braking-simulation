import numpy as np
from typing import Tuple

from physics import portance, trainee, reaction_normale, coefficient_frottement


def simulate_braking(v0: float, dt: float, m: float, g: float, rho: float,
                     Cz: float, Cx: float, S: float, etat: str,
                     mu_dry: float, mu_wet: float,
                     tire_pressure_pa: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    t = 0.0
    x = 0.0
    v = v0

    t_list, x_list, v_list, a_list = [], [], [], []

    while v > 0.0:
        L = portance(v, rho, Cz, S)
        N = reaction_normale(v, m, g, rho, Cz, S)
        mu = coefficient_frottement(etat, v, mu_dry, mu_wet, tire_pressure_pa)
        F_aero = trainee(v, rho, Cx, S)
        F_frott = mu * N
        a = -(F_aero + F_frott) / m

        t_list.append(t)
        x_list.append(x)
        v_list.append(v)
        a_list.append(a)

        x_new = x + dt * v
        v_new = v + dt * a
        t_new = t + dt

        x, v, t = x_new, v_new, t_new

    v_list[-1] = 0.0

    return np.array(t_list), np.array(x_list), np.array(v_list), np.array(a_list)