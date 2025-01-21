import numpy as np
import sys
import json


def main():
    t_array = np.arange(start=-270.0, stop=1300.0, step=1.0)
    V_array = np.zeros(len(t_array))
    j = 0
    for t in t_array:
        c_neg = np.array(
            [
                0.0,
                3.9450128025e1,
                2.3622373598e-2,
                -3.2858906784e-4,
                -4.9904828777e-6,
                -6.7509059173e-8,
                -5.7410327428e-10,
                -3.1088872894e-12,
                -1.0451609365e-14,
                -1.9889266878e-17,
                -1.6322697486e-20,
            ]
        )
        c_pos = np.array(
            [
                -1.7600413686e1,
                3.8921204975e1,
                1.8558770032e-2,
                -9.9457592874e-5,
                3.1840945719e-7,
                -5.6072844889e-10,
                5.6075059059e-13,
                -3.2020720003e-16,
                9.7151147152e-20,
                -1.2104721275e-23,
            ]
        )
        a_pos = np.array([1.185976e2, -1.183432e-4])
        V = 0.0
        i = 0
        if t < 0:
            for coef in c_neg:
                V += coef * (t**i)
                i += 1
        else:
            for coef in c_pos:
                V += coef * (t**i)
                i += 1
            V += a_pos[0] * np.exp(a_pos[1] * (t - 126.9686) ** 2)
        V_array[j] = V * 0.000001
        j += 1
    data = {"t, C": t_array.tolist(), "V, V": V_array.tolist()}
    with open("calibration_table_thermocouple_K.dat", "w") as filehandle:
        json.dump(data, filehandle)
    filehandle.close()


if __name__ == "__main__":
    main()
