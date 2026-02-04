"""THRU comparison and visualization utilities.

This module provides functions to compare calibrated THRU measurements
against reference measurements and visualize the results.
"""

import numpy as np
import skrf as rf
import matplotlib.pyplot as plt


import numpy as np
import skrf as rf
import matplotlib.pyplot as plt


def compare_thru_S21(freq_est, S21_est, s2p_ref):
    """
    Compara S21 estimado del THRU (SOLR) con un THRU medido (PNA-X).

    Parameters
    ----------
    freq_est : np.ndarray
        Frecuencia del S21 estimado (Hz)
    S21_est : np.ndarray (complex)
        S21 estimado por SOLR
    s2p_ref : str
        Archivo s2p del THRU medido con PNA-X
    """

    # Leer THRU de referencia
    ntwk_ref = rf.Network(s2p_ref)
    freq_ref = ntwk_ref.f
    S21_ref = ntwk_ref.s[:, 1, 0]  # S21

    # Interpolar referencia al eje de frecuencia estimado (por seguridad)
    S21_ref_i = np.interp(
        freq_est,
        freq_ref,
        S21_ref.real
    ) + 1j * np.interp(
        freq_est,
        freq_ref,
        S21_ref.imag
    )

    # Magnitud y fase
    mag_est = 20 * np.log10(np.abs(S21_est))
    mag_ref = 20 * np.log10(np.abs(S21_ref_i))

    phase_est = np.unwrap(np.angle(S21_est)) * 180 / np.pi
    phase_ref = np.unwrap(np.angle(S21_ref_i)) * 180 / np.pi

    freq_GHz = freq_est / 1e9

    # ---- PLOTS ----
    plt.figure(figsize=(10, 7))

    # Magnitud
    plt.subplot(2, 1, 1)
    plt.plot(freq_GHz, mag_est, label="SOLR THRU estimado", linewidth=2)
    plt.plot(freq_GHz, mag_ref, '--', label="THRU medido (PNA-X)")
    plt.ylabel("|S21| [dB]")
    plt.grid(True)
    plt.legend()

    # Fase
    plt.subplot(2, 1, 2)
    plt.plot(freq_GHz, phase_est, label="SOLR THRU estimado", linewidth=2)
    plt.plot(freq_GHz, phase_ref, '--', label="THRU medido (PNA-X)")
    plt.ylabel("Fase [deg]")
    plt.xlabel("Frecuencia [GHz]")
    plt.grid(True)
    plt.legend()

    plt.suptitle("Comparación S21 del THRU (SOLR vs PNA-X)", fontsize=14)
    plt.tight_layout()
    plt.show()