import time

import numpy as np
import skrf as rf

from calibration.tracking import estimate_transmission_tracking
from analysis.comparison import compare_thru_S21
from ui.file_dialogs import select_s2p


def read_thru_T_matrix(s2p_file):
    """
    Lee un archivo THRU (.s2p) y devuelve la matriz T (ABCD)
    por frecuencia.

    Parameters
    ----------
    s2p_file : str
        Ruta al archivo THRU .s2p

    Returns
    -------
    freq : np.ndarray
        Vector de frecuencia (Hz)
    TM : np.ndarray
        Matriz T por frecuencia, shape (Nf, 2, 2)
    """

    ntwk = rf.Network(s2p_file)

    freq = ntwk.f  # Hz

    # Convertir de S a T (ABCD)
    # skrf usa 'a' para ABCD
    T = ntwk.a  # shape (Nf, 2, 2)

    return freq, T


def perform_transmission_analysis(freq, error_params_p1, error_params_p2):
    """Load THRU measurements and estimate transmission tracking.

    Parameters
    ----------
    freq : np.ndarray
        Frequency vector
    error_params_p1 : dict
        Error parameters for port 1
    error_params_p2 : dict
        Error parameters for port 2
    """
    print("\nSeleccione el archivo s2p del THRU")
    time.sleep(0.5)

    archivo_thru = select_s2p("Archivo de THRU")
    _, T_thru = read_thru_T_matrix(archivo_thru)

    result_tracking = estimate_transmission_tracking(
        T_thru, error_params_p1['T_XA'], error_params_p2['T_XB']
    )
    S21_thru = np.asarray(result_tracking['S21_thru'], dtype=complex)

    print(f"\n✓ S21 del THRU estimado (primeros 5 puntos): {S21_thru[:5]}")

    print("\nSeleccione el THRU de referencia medido con PNA-X")
    time.sleep(0.5)
    archivo_thru_ref = select_s2p("THRU de referencia (PNA-X)")
    compare_thru_S21(freq, S21_thru, archivo_thru_ref)
