import numpy as np

from calibration.error_box import estimate_error_box_SOL, build_T_XA, build_T_XB
from calibration.gamma import compute_Gamma_L
from debug.debug_utils import plot_multiple_gamma_smith


def validate_frequency_vectors(freq_p1, freq_p2):
    """Validate that two frequency vectors are identical.

    Raises
    ------
    RuntimeError
        If frequency vectors don't match
    """
    if not np.allclose(freq_p1, freq_p2, rtol=1e-5):
        raise RuntimeError(
            "Los archivos del Puerto 1 y Puerto 2 tienen vectores de frecuencia diferentes. "
            "Esto puede causar problemas en la calibración."
        )


def calculate_error_parameters(freq, gamma_in_p1, gamma_in_p2, standards_p1, standards_p2, zref):
    """Calculate SOL error parameters for both ports.

    Returns
    -------
    tuple
        (error_params_p1, error_params_p2) - dictionaries with error coefficients
    """
    print("\nCalculando estándares Gamma_L teóricos...")

    gamma_l_p1 = compute_Gamma_L(
        freq, standards_p1['load'], standards_p1['open'], standards_p1['short'], zref
    )
    plot_multiple_gamma_smith(freq, gamma_l_p1, puerto=1)
    
    gamma_l_p2 = compute_Gamma_L(
        freq, standards_p2['load'], standards_p2['open'], standards_p2['short'], zref
    )

    print("Calculando parámetros de error (SOL)...")

    # Puerto 1
    e00_p1, e10e01_p1, e11_p1 = estimate_error_box_SOL(
        {
            'short': gamma_in_p1['gamma_short'],
            'open': gamma_in_p1['gamma_open'],
            'load': gamma_in_p1['gamma_load'],
        },
        {
            'short': gamma_l_p1['short'],
            'open': gamma_l_p1['open'],
            'load': gamma_l_p1['load'],
        },
    )

    # Puerto 2
    e00_p2, e10e01_p2, e11_p2 = estimate_error_box_SOL(
        {
            'short': gamma_in_p2['gamma_short'],
            'open': gamma_in_p2['gamma_open'],
            'load': gamma_in_p2['gamma_load'],
        },
        {
            'short': gamma_l_p2['short'],
            'open': gamma_l_p2['open'],
            'load': gamma_l_p2['load'],
        },
    )

    # Reinterpretación física de errores del puerto 2
    rev_p2 = map_forward_to_reverse_errors(
        e00_p2,
        e10e01_p2,
        e11_p2
    )

    e22_p2    = rev_p2['e22']
    e33_p2    = rev_p2['e33']
    e23e32_p2 = rev_p2['e23e32']

    return {
        'e00': e00_p1,
        'e10e01': e10e01_p1,
        'e11': e11_p1,
        'T_XA': build_T_XA(e00_p1, e11_p1, e10e01_p1),
    }, {
        'e22': e22_p2,
        'e23e32': e23e32_p2,
        'e33': e33_p2,
        'T_XB': build_T_XB(e22_p2, e33_p2, e23e32_p2),
    }

def map_forward_to_reverse_errors(e00, e10e01, e11):
    """
    Convierte errores SOL forward al significado físico del puerto 2.
    """
    return {
        'e22': e11,
        'e33': e00,
        'e23e32': e10e01
    }