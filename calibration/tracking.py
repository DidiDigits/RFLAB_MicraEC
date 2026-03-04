"""Transmission tracking (7th error term) estimation.

This module calculates the seventh calibration error parameter using 
THRU measurements. SOL calibration provides 6 error terms, and this
module completes the 7-term error model by estimating transmission tracking.
"""

from math import tau
import numpy as np
import matplotlib.pyplot as plt


def estimate_transmission_tracking(T_M, T_XA, T_XB, freq):
    """
    Estima transmisión tracking y selecciona automáticamente la rama física.
    """

    alpha_p, alpha_m = compute_alpha(T_M, T_XA, T_XB)
    
    # Debug Plot alpha
    #from debug.debug_utils import plot_alpha
    #plot_alpha(freq, alpha_m)
    #plot_alpha(freq, alpha_p)
    
    X = compute_X_matrix(T_M, T_XA, T_XB)
    
    #Debug Plot X
    #from debug.debug_utils import plot_X
    #plot_X(freq, X)

    # Calcular S21 para ambas ramas
    S21_p = alpha_p / X[:, 1, 1]
    S21_m = alpha_m / X[:, 1, 1]

    # Encontrar la rama física correcta usando la fase de S21
    sign = choose_alpha_sign(freq, S21_p, S21_m)
    
    if sign == +1:
        print("\n✓ Se selecciona la rama con alpha positivo")
        S21_thru = S21_p
    else:
        print("\n✓ Se selecciona la rama con alpha negativo")
        S21_thru = S21_m

    #Debug Plot S21
    from debug.debug_utils import plot_S21n
    plot_S21n(freq, S21_thru)

    return {
        'alpha': alpha_p if sign == +1 else alpha_m,
        'S21_thru': S21_thru
    }

def compute_alpha(T_M, T_XA, T_XB):
    """
    Calcula las dos soluciones de alpha(f).

    Returns
    -------
    alpha_plus : np.ndarray (complex)
    alpha_minus : np.ndarray (complex)
    """

    det_TM  = np.linalg.det(T_M)
    det_TXA = np.linalg.det(T_XA)
    det_TXB = np.linalg.det(T_XB)

    ratio = det_TM / (det_TXA * det_TXB)

    alpha = np.sqrt(ratio)

    for k in range(1, len(alpha)):
        if np.abs(alpha[k] - alpha[k-1]) > np.abs(-alpha[k] - alpha[k-1]):
            alpha[k] = -alpha[k]

    alpha_plus  = alpha
    alpha_minus = -alpha_plus

    #[DEBUG]
    #print(alpha_plus)
    #print(alpha_minus)

    return alpha_plus, alpha_minus

def choose_alpha_sign(freq, S21_plus, S21_minus, N=20):
    # Tomamos las primeras N frecuencias
    phase_plus  = np.angle(S21_plus[:N])
    phase_minus = np.angle(S21_minus[:N])

    mean_plus  = np.mean(phase_plus)
    mean_minus = np.mean(phase_minus)

    # Elegimos la que esté más cerca de 0 rad
    if abs(mean_plus) < abs(mean_minus):
        return +1
    else:
        return -1



def compute_X_matrix(T_M, T_XA, T_XB):
    """
    Calcula X(f) = T_XA^{-1} * T_M * T_XB^{-1}
    """

    Nf = T_M.shape[0]
    X = np.zeros_like(T_M, dtype=complex)

    for k in range(Nf):
        X[k] = (
            np.linalg.inv(T_XA[k]) @
            T_M[k] @
            np.linalg.inv(T_XB[k])
        )
    return X

