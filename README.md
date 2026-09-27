# Aircraft Landing Braking Simulation

This project is a numerical and theoretical study of how an aircraft decelerates after touchdown, built as an engineering-track project. It simulates the braking distance and trajectory of an aircraft under different runway conditions (dry, wet, and hydroplaning) and quantifies the effect of airbrakes (or spoilers) on stopping performance. The goal was not just to produce a working script, but to understand, from first principles, why an aircraft behaves so differently from a car when it brakes, and to translate that understanding into a numerical model that can be tested, verified, and trusted.

## Why this problem is not as simple as it looks

At first glance, stopping an aircraft on the ground seems like a straightforward braking problem, applying the brakes and friction slows the vehicle down then it eventually stops. But an aircraft keeps its wings throughout the entire landing roll, and wings exist specifically to produce an upward force. That means that for as long as the aircraft is moving fast, part of its weight is still being carried by the air rather than by the wheels. Since the amount of friction available at the wheels depends directly on how much weight they are actually supporting, the braking force is not constant; it changes as the aircraft slows down, in a way that is coupled to the aircraft's own speed. This is the central physical subtlety of the whole problem, and it is what makes a numerical, step-by-step simulation genuinely necessary rather than just convenient.

## The physics, explained

### Lift

A wing, in cross-section, has an asymmetric shape and is tilted slightly relative to the oncoming air (angle of attack). As air flows over this shape, it gets deflected downward. By Newton's third law, the air pushes back on the wing  upward. That reaction force is lift. It scales with the square of the speed, because two separate effects each scale with speed, the mass of air encountered per second, and the speed at which that air gets deflected. Multiply the two together and you get a v² dependency, a general feature of aerodynamic forces, not a coincidence specific to lift.

On the ground, lift is no longer useful for flying; the aircraft isn't going anywhere but down the runway but it doesn't disappear. It continues to "steal" part of the aircraft's weight away from the wheels, which is precisely why it matters here even though the aircraft has already landed.

### Aerodynamic drag

The same basic air-object interaction that produces lift also produces a force that opposes forward motion directly: drag. It is the resistance you feel when you stick your hand out of a moving car window. Like lift, it scales with v². Airbrakes (spoilers) exploit this force deliberately: when deployed, they disrupt the smooth airflow over the wing. This does two useful things simultaneously, it destroys lift (so more weight returns to the wheels, restoring braking capability), and it sharply increases drag (adding direct aerodynamic braking). One mechanical action, two beneficial effects at once, which is exactly why deploying airbrakes is such an effective braking strategy immediately after touchdown.

### Wheel-to-ground friction

This is a completely different physical mechanism from the previous two, it is solid-on-solid contact, not an air interaction. When the brakes are applied, the tire tends to resist slipping against the runway surface, and that resistance is friction. Critically, the friction force does not depend on the aircraft's total weight; it depends on the reaction force actually transmitted through the wheels to the ground, which we call N. Because lift steals part of the weight away from the wheels, N is smaller than the full weight at high speed so even on a runway with excellent grip, there simply isn't much weight pressing the wheels down yet, and friction is correspondingly weak. As the aircraft slows, lift fades away (again because it depends on v²), N rises back toward the full weight, and friction becomes progressively more effective. This is the opposite of what happens in a car, where the normal force is essentially constant throughout braking.

### Wet runway and hydroplaning

On a dry runway, the tire rubber is in direct mechanical contact with the pavement's micro-texture, giving strong grip. A film of water on a wet runway gets in the way of that direct contact; some of it is squeezed away by the tire tread grooves, but as long as any film remains between rubber and asphalt, grip is reduced. This is a simple lubrication effect, nothing exotic; the same reason it's easier to slip on a wet floor.

Hydroplaning is a more extreme and more abrupt version of the same idea. Above a critical speed, the tire no longer has enough time to squeeze the water out of the way before the next section of tread arrives, a wedge of pressurized water builds up underneath the tire and can lift it completely off the runway surface. At that point there is no solid contact at all; the tire is essentially skiing on a layer of water, and the friction coefficient collapses toward zero almost immediately. This is why hydroplaning is modeled here as a threshold phenomenon rather than a gradual degradation, below the critical speed, grip behaves like an ordinary wet runway; above it, grip effectively disappears. The critical speed itself is estimated using a well-known empirical formula from aviation safety studies, relating it to tire inflation pressure, a more inflated tire resists the hydrodynamic pressure better and hydroplanes at a higher speed.

## Governing equation

Putting the vertical equilibrium (N = m·g − L(v)) together with Newton's second law projected along the direction of motion gives the equation that drives the whole simulation:

m · dv/dt = − F_drag(v) − μ(v) · N(v)

This equation is nonlinear (both aerodynamic terms scale with v²) and, once μ becomes a function of speed rather than a constant (as it does in the hydroplaning case), there is no simple closed-form solution. That is the direct justification for solving it numerically rather than analytically.

## Numerical method

The equation is integrated using the explicit Euler method: at each small time step, every force is recomputed from the current speed, the resulting acceleration is used to advance the speed and position by one step, and the process repeats until the aircraft comes to rest. Recomputing everything at every step rather than solving once and extrapolating matters precisely because the system is coupled; normal force, friction coefficient (in the hydroplaning case), and both aerodynamic forces are all functions of the instantaneous speed, which is itself changing throughout.

## Project structure

```text
aircraft-braking-simulation/
├── data/aircraft_params.json   # aircraft, aerodynamic, friction and runway parameters
├── src/
│   ├── physics.py       # individual force formulas (lift, drag, normal reaction, friction)
│   ├── solver.py         # explicit Euler integration loop
│   ├── scenarios.py       # the five comparison scenarios and their execution
│   ├── analysis.py         # metric extraction and comparison table
│   ├── plotting.py          # generates the speed/distance/deceleration figures
│   └── advisor.py            # runway safety assessment based on stopping distance vs. runway length
├── figures/                    # generated .png plots
└── main.py                     # entry point orchestrating the full pipeline
```

Each file corresponds to one distinct concern; `physics.py` holds nothing but the individual formulas, so any physical mistake can only ever be found there; `solver.py` is a "blind" numerical engine that calls those formulas without knowing anything about their physical meaning; `scenarios.py` exists purely so that adding a new comparison case never requires touching the solver itself; `analysis.py` and `plotting.py` turn raw numerical output into something a human can actually read or put in a report; and `advisor.py` sits on top of everything as an interpretation layer, translating a stopping distance into a plain safety verdict.

## Scenarios compared

1. Dry runway (airbrakes deployed)
2. Dry runway (airbrakes retracted)
3. Wet runway (airbrakes deployed)
4. Hydroplaning (airbrakes deployed)
5. Wet runway (airbrake failure)

## Results (A320-like aircraft, touchdown speed 70 m/s, 2500 m runway)

| Scenario | Stopping distance | Difference vs reference |
| --- | --- | --- |
| Dry | 413.8 m | reference |
| Dry (retracted) | 423.2 m | +2.3% |
| Wet | 801.1 m | +93.6% |
| Hydroplaning | 4728.2 m | +1042.6% |
| Wet (failure) | 836.6 m | +102.2% |

The wet-runway distance is roughly double the dry-runway distance, consistent with published aviation figures for the effect of runway contamination. The hydroplaning case is the most striking; it overshoots the available runway length by a factor of nearly two, and its deceleration curve shows a very distinctive shape almost flat for most of the landing roll (only weak aerodynamic drag is acting, since the wheels have essentially no grip above the hydroplaning threshold), followed by an abrupt jump in deceleration exactly at the moment the aircraft's speed drops back below the critical hydroplaning speed and the tires regain contact with the runway. Seeing that kink appear naturally in the simulated curves rather than being built in by hand was a good sign that the model was behaving the way the underlying physics predicted it should.

## Validation

Numerical results were not simply trusted at face value. The first two integration steps were computed by hand from the governing equation and compared against the code's output to confirm the formulas were implemented correctly. A convergence study was then run, varying the time step from 1.0 s down to 0.001 s: the stopping distance converges as expected for an explicit Euler scheme (roughly first-order error), and the time step actually used (0.01 s) already agrees with a much finer step to within 0.1%. Finally, the entire pipeline was independently reimplemented from the same equations by a second AI assistant, without sharing code between the two attempts only the underlying physics and parameter file were held in common. Both implementations produced stopping distances agreeing to within about 0.1 meter across all five scenarios, which is about as strong a cross-check as this kind of project can realistically get.

## Known limitations

The hydroplaning transition is modeled as a hard threshold rather than a gradual one; real hydroplaning onset is likely smoother than an on/off switch, and a hyperbolic-tangent transition would be a more physically defensible choice if this model were extended. The explicit Euler method itself carries an inherent first-order truncation error; a higher-order method such as fourth-order Runge-Kutta would reduce this further, though the convergence study shows it isn't a practical concern at the time step used here. The model also ignores several real effects that are outside its intended scope, dynamic front/rear load transfer during braking, tire flexibility, crosswind, and the detailed slip-dependent friction behavior captured by more advanced tire models (e.g. Pacejka curves). Finally, the normal reaction force N is clamped at zero as a numerical safeguard against an unphysical negative value; this should never actually trigger at the speeds and parameters used here, but it is left in place deliberately rather than removed.

## Running it

```bash
pip install -r requirements.txt
python main.py
```

This prints the comparison table to the console, writes the three figures (speed, distance, and deceleration over time) to `figures/`, and prints a per-scenario runway safety verdict based on the configured runway length and safety margin
