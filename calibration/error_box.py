"""Error box calculation using SOL (Short-Open-Load) calibration technique.

This module implements the calculation of the 7-term error model parameters
using Short, Open, and Load standards.
"""

import numpy as np


def estimate_error_box_SOL(gamma_in_dict, gamma_L_dict):
    """
    Estima e00(f), e10e01(f), e11(f) punto a punto en frecuencia
    usando estándares SHORT, OPEN y LOAD.

    Parameters
    ----------
    gamma_in_dict : dict
        {'short': array, 'open': array, 'load': array}
    gamma_L_dict : dict
        {'short': array, 'open': array, 'load': array}

    Returns
    -------
    e00 : np.ndarray (complex)
    e10e01 : np.ndarray (complex)
    e11 : np.ndarray (complex)
    """

    keys = ['short', 'open', 'load']
    Nf = len(gamma_in_dict['short'])

    e00 = np.zeros(Nf, dtype=complex)
    e10e01 = np.zeros(Nf, dtype=complex)
    e11 = np.zeros(Nf, dtype=complex)

    for k in range(Nf):
        # y vector
        y = np.array([
            gamma_in_dict['short'][k],
            gamma_in_dict['open'][k],
            gamma_in_dict['load'][k]
        ], dtype=complex)

        # X matrix
        X = np.array([
            [1,
             gamma_L_dict['short'][k],
             gamma_L_dict['short'][k] * gamma_in_dict['short'][k]],

            [1,
             gamma_L_dict['open'][k],
             gamma_L_dict['open'][k] * gamma_in_dict['open'][k]],

            [1,
             gamma_L_dict['load'][k],
             gamma_L_dict['load'][k] * gamma_in_dict['load'][k]],
        ], dtype=complex)

        # Solve 3x3 system
        a0, a1, a2 = np.linalg.solve(X, y)

        e00[k] = a0
        e11[k] = a2
        e10e01[k] = a1 + a0 * a2

    return e00, e10e01, e11



def build_T_XA(e00, e11, e10e01):
    """
    Construye la matriz T_XA(f) para cada frecuencia.

    Parameters
    ----------
    e00 : np.ndarray (complex)
    e11 : np.ndarray (complex)
    e10e01 : np.ndarray (complex)

    Returns
    -------
    T_XA : np.ndarray
        shape (Nf, 2, 2)
    """

    e00 = np.asarray(e00, dtype=complex)
    e11 = np.asarray(e11, dtype=complex)
    e10e01 = np.asarray(e10e01, dtype=complex)

    if not (e00.shape == e11.shape == e10e01.shape):
        raise ValueError("Todos los términos de error deben tener la misma longitud")

    Delta_e = e00 * e11 - e10e01

    Nf = e00.size
    T_XA = np.zeros((Nf, 2, 2), dtype=complex)

    T_XA[:, 0, 0] = -Delta_e
    T_XA[:, 0, 1] = e00
    T_XA[:, 1, 0] = -e11
    T_XA[:, 1, 1] = 1.0

    return T_XA


def build_T_XB(e22, e33, e23e32):
    """
    Construye la matriz T_XB(f) para cada frecuencia.

    Parameters
    ----------
    e22 : np.ndarray (complex)
    e33 : np.ndarray (complex)
    e23e32 : np.ndarray (complex)

    Returns
    -------
    T_XB : np.ndarray
        shape (Nf, 2, 2)
    """

    e22 = np.asarray(e22, dtype=complex)
    e33 = np.asarray(e33, dtype=complex)
    e23e32 = np.asarray(e23e32, dtype=complex)

    if not (e22.shape == e33.shape == e23e32.shape):
        raise ValueError("Todos los términos de error deben tener la misma longitud")

    Delta_e = e22 * e33 - e23e32

    Nf = e22.size
    T_XB = np.zeros((Nf, 2, 2), dtype=complex)

    T_XB[:, 0, 0] = -Delta_e
    T_XB[:, 0, 1] = e22
    T_XB[:, 1, 0] = -e33
    T_XB[:, 1, 1] = 1.0

    return T_XB
