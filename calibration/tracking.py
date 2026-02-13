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

    #Debug Plot S21
    from debug.debug_utils import plot_S21n
    plot_S21n(freq, S21_p)
    plot_S21n(freq, S21_m)

    from transmission import compute_group_delay

    gd_p = compute_group_delay(freq, S21_p)
    gd_m = compute_group_delay(freq, S21_m)

    print("Group Delay (p) statistics:")
    print(f"Mean     : {np.mean(gd_p)*1e12:.3f} ps")
    print(f"Median   : {np.median(gd_p)*1e12:.3f} ps")
    print(f"Min      : {np.min(gd_p)*1e12:.3f} ps")
    print(f"Max      : {np.max(gd_p)*1e12:.3f} ps")
    print(f"Std Dev  : {np.std(gd_p)*1e12:.3f} ps")

    print("Group Delay (m) statistics:")
    print(f"Mean     : {np.mean(gd_m)*1e12:.3f} ps")
    print(f"Median   : {np.median(gd_m)*1e12:.3f} ps")
    print(f"Min      : {np.min(gd_m)*1e12:.3f} ps")
    print(f"Max      : {np.max(gd_m)*1e12:.3f} ps")
    print(f"Std Dev  : {np.std(gd_m)*1e12:.3f} ps")






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

    alpha_plus  = np.sqrt(ratio)
    alpha_minus = -alpha_plus

    print(alpha_plus)
    print(alpha_minus)

    return alpha_plus, alpha_minus


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

