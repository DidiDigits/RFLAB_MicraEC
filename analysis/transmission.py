import time

import numpy as np
import skrf as rf

from calibration.tracking import estimate_transmission_tracking
from analysis.comparison import compare_thru_S21
from ui.file_dialogs import select_s2p


def read_thru_T_matrix(s2p_file):
    ntwk = rf.Network(s2p_file)
    T = s_to_chain_T(ntwk)

    # Debug Plot T
    from debug.debug_utils import plot_detT
    plot_detT(T, ntwk.f)

    return ntwk.f, T

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
    freq, T_thru = read_thru_T_matrix(archivo_thru)

    result_tracking = estimate_transmission_tracking(
        T_thru, error_params_p1['T_XA'], error_params_p2['T_XB'], freq
    )
    S21_thru = np.asarray(result_tracking['S21_thru'], dtype=complex)

    print(f"\n✓ S21 del THRU estimado (primeros 5 puntos): {S21_thru[:5]}")

    print("\nSeleccione el THRU de referencia medido con PNA-X")
    time.sleep(0.5)
    archivo_thru_ref = select_s2p("THRU de referencia (PNA-X)")
    compare_thru_S21(freq, S21_thru, archivo_thru_ref)

def s_to_chain_T(ntwk):
    S = ntwk.s
    Nf = S.shape[0]
    T = np.zeros((Nf, 2, 2), dtype=complex)

    S11 = S[:,0,0]
    S12 = S[:,0,1]
    S21 = S[:,1,0]
    S22 = S[:,1,1]

    Delta = S11*S22 - S12*S21

    T[:,0,0] = -Delta / S21
    T[:,0,1] =  S11 / S21
    T[:,1,0] = -S22 / S21
    T[:,1,1] =  1.0 / S21

    return T

def compute_group_delay(freq, S21):
    # Fase desenrollada
    phase = np.unwrap(np.angle(S21))
    
    # Derivada numérica
    dphi_df = np.gradient(phase, freq)
    
    # Group delay
    tau = - dphi_df / (2*np.pi)
    
    return tau