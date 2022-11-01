from typing import Callable, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from quat import Quaternion
from Object import Object


class Runge_Kutta:
    @staticmethod
    def right_function(obj: Object,
                       q: Quaternion) -> np.array:
        return obj.state_vector(obj, q)

    @staticmethod
    def make_step(time: float,
                  step: float,
                  state: np.array,
                  func: Callable[[float, np.ndarray], np.ndarray]) -> np.array:
        k1 = func(time, state)
        k2 = func(time + step / 2, state + (step / 2) * k1)
        k3 = func(time + step / 2, state + (step / 2) * k2)
        k4 = func(time + step, state + step * k3)
        y = state + (step / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        return y

    @staticmethod
    def integrate(make_step,
                  y0: np.array,
                  time_0: float,
                  time_end: float,
                  step: float,
                  func: Callable[[float, np.ndarray], np.ndarray]) -> Tuple[List[float], List[np.ndarray]]:
        time = time_0
        times: List[float] = [time]
        result: List[np.ndarray] = [y0]
        while time < time_end:
            result.append(make_step(times[-1], step, result[-1], func))
            time = time + step
            times.append(time)
        return times, result
