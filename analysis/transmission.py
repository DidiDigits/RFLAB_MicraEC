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
    #from debug.debug_utils import plot_detT
    #plot_detT(T, ntwk.f)

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

    #Debug
    #print(result_tracking)

    S21_thru = np.asarray(result_tracking['S21_thru'], dtype=complex)

    # Debug: Calcular tau para el THRU estimado
    from debug.debug_utils import plot_tau
    from analysis.transmission import calculate_tau
    tau = calculate_tau(freq, S21_thru)
    print(f"\n El retardo estimado: {tau} segundos")

    #plot_tau(freq, tau)

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


def calculate_tau(freq, S21_thru):
    omega = 2 * np.pi * freq
    phase_s21 = np.angle(S21_thru)  # Phase in radians
    phase_unwrapped = np.unwrap(phase_s21)
    
    # Fit a line to UNWRAPPED phase vs. ANGULAR frequency
    p = np.polyfit(omega, phase_unwrapped, 1)
    print(f"\nCoeficientes de la recta ajustada: {p}")
    tau_total = -p[0]  # Correct delay calculation (round trip -> one way)

    import matplotlib.pyplot as plt
    
    plt.figure()
    plt.plot(freq/1e9, phase_unwrapped, label='Fase Unwrapped')
    plt.plot(freq/1e9, np.polyval(p, omega), label='Ajuste Lineal', linestyle='--')
    plt.xlabel('Frecuencia [GHz]')
    plt.ylabel('Fase [rad]')
    plt.title(f'Fase Unwrapped vs. Frecuencia\nEstimación de Retardo Total: {tau_total:.2e} s')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    input("\nPresione Enter para continuar...")

    return tau_total