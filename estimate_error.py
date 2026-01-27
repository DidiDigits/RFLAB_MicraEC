import numpy as np

def estimate_error_box(gamma_in, gamma_L):
    """
    Estimates e00, e10*e01 y e11 from measurrments Gamma_in and the standard reflection coefficients Gamma_L.

    Parameters
    ----------
    gamma_in : array_like (complex)
        Gamma_in Measurements
    gamma_L : array_like (complex)
        Reflection coefficient of the load

    Returns
    -------
    e00 : complex
    e10e01 : complex
    e11 : complex
    """

    gamma_in = np.asarray(gamma_in, dtype=complex)
    gamma_L  = np.asarray(gamma_L, dtype=complex)

    if gamma_in.shape != gamma_L.shape:
        raise ValueError("Gamma_in y Gamma_L deben tener la misma longitud")

    # Vector y
    y = gamma_in

    # Matrix X
    X = np.column_stack([
        np.ones_like(gamma_L),
        gamma_L,
        gamma_L * gamma_in
    ])

    # Complex least squares
    a, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    a0, a1, a2 = a

    # Recover physical parameters
    e00 = a0
    e11 = a2
    e10e01 = a1 + a0 * a2

    return e00, e10e01, e11
