import numpy as np

def estimate_transmission_tracking(T_M, T_XA, T_XB):
    """
    Estima transmisión tracking y selecciona automáticamente la rama física.
    """

    alpha_p, alpha_m = compute_alpha(T_M, T_XA, T_XB)
    X = compute_X_matrix(T_M, T_XA, T_XB)

    alpha, S21_thru, branch = choose_alpha_automatic(alpha_p, alpha_m, X)

    return {
        'alpha': alpha,
        'S21_thru': S21_thru,
        'X': X,
        'branch': branch
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

    alpha_plus  = np.sqrt(ratio)
    alpha_minus = -alpha_plus

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

def compute_S21_thru(alpha, X):
    """
    Calcula S21 del THRU recíproco.

    Parameters
    ----------
    alpha : np.ndarray (complex)
    X : np.ndarray, shape (Nf,2,2)

    Returns
    -------
    S21 : np.ndarray (complex)
    """
    return alpha / X[:, 1, 1]

def s21_score(S21):
    mag = np.abs(S21)
    phase = np.unwrap(np.angle(S21))

    score_mag   = np.mean((mag - 1.0)**2)       # cerca de 1
    score_phase = np.mean(np.diff(phase)**2)    # suavidad
    score_gain  = np.mean(np.maximum(mag - 1.2, 0)**2)  # penaliza ganancia

    return score_mag + score_phase + 10*score_gain

def choose_alpha_automatic(alpha_p, alpha_m, X):
    S21_p = compute_S21_thru(alpha_p, X)
    S21_m = compute_S21_thru(alpha_m, X)

    score_p = s21_score(S21_p)
    score_m = s21_score(S21_m)

    if score_p < score_m:
        alpha = alpha_p
        branch = 'plus'
        S21 = S21_p
    else:
        alpha = alpha_m
        branch = 'minus'
        S21 = S21_m

    return alpha, S21, branch


