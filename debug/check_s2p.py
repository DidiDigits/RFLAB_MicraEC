import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
import os
import sys
import traceback
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui.file_dialogs import select_s2p_files

def plot_s2p_comparison(raw_files, corrected_files):
    """
    Grafica comparación RAW vs CORRECTED de archivos S2P
    en magnitud y fase.

    Parámetros
    ----------
    raw_files : list[str]
    corrected_files : list[str]
    """

    if len(raw_files) != len(corrected_files):
        raise ValueError("Debe haber el mismo número de archivos RAW y CORRECTED")

    fig_mag, axs_mag = plt.subplots(2, 2, figsize=(12, 9))
    fig_phase, axs_phase = plt.subplots(2, 2, figsize=(12, 9))

    eps = 1e-15

    for raw, corr in zip(raw_files, corrected_files):

        ntwk_raw = rf.Network(raw)
        ntwk_corr = rf.Network(corr)

        freq = ntwk_raw.f / 1e9

        S_raw = ntwk_raw.s
        S_corr = ntwk_corr.s

        label = os.path.basename(raw)

        # -------- MAGNITUD --------

        S11_raw = 20*np.log10(np.abs(S_raw[:,0,0]) + eps)
        S12_raw = 20*np.log10(np.abs(S_raw[:,0,1]) + eps)
        S21_raw = 20*np.log10(np.abs(S_raw[:,1,0]) + eps)
        S22_raw = 20*np.log10(np.abs(S_raw[:,1,1]) + eps)

        S11_corr = 20*np.log10(np.abs(S_corr[:,0,0]) + eps)
        S12_corr = 20*np.log10(np.abs(S_corr[:,0,1]) + eps)
        S21_corr = 20*np.log10(np.abs(S_corr[:,1,0]) + eps)
        S22_corr = 20*np.log10(np.abs(S_corr[:,1,1]) + eps)

        axs_mag[0,0].plot(freq, S11_raw, '--', label=f"{label} RAW")
        axs_mag[0,0].plot(freq, S11_corr, label=f"{label} CORR")

        axs_mag[0,1].plot(freq, S12_raw, '--', label=f"{label} RAW")
        axs_mag[0,1].plot(freq, S12_corr, label=f"{label} CORR")

        axs_mag[1,0].plot(freq, S21_raw, '--', label=f"{label} RAW")
        axs_mag[1,0].plot(freq, S21_corr, label=f"{label} CORR")

        axs_mag[1,1].plot(freq, S22_raw, '--', label=f"{label} RAW")
        axs_mag[1,1].plot(freq, S22_corr, label=f"{label} CORR")

        # -------- FASE --------

        phase_S11_raw = np.unwrap(np.angle(S_raw[:,0,0])) * 180/np.pi
        phase_S12_raw = np.unwrap(np.angle(S_raw[:,0,1])) * 180/np.pi
        phase_S21_raw = np.unwrap(np.angle(S_raw[:,1,0])) * 180/np.pi
        phase_S22_raw = np.unwrap(np.angle(S_raw[:,1,1])) * 180/np.pi

        phase_S11_corr = np.unwrap(np.angle(S_corr[:,0,0])) * 180/np.pi
        phase_S12_corr = np.unwrap(np.angle(S_corr[:,0,1])) * 180/np.pi
        phase_S21_corr = np.unwrap(np.angle(S_corr[:,1,0])) * 180/np.pi
        phase_S22_corr = np.unwrap(np.angle(S_corr[:,1,1])) * 180/np.pi

        axs_phase[0,0].plot(freq, phase_S11_raw, '--', label=f"{label} RAW")
        axs_phase[0,0].plot(freq, phase_S11_corr, label=f"{label} CORR")

        axs_phase[0,1].plot(freq, phase_S12_raw, '--', label=f"{label} RAW")
        axs_phase[0,1].plot(freq, phase_S12_corr, label=f"{label} CORR")

        axs_phase[1,0].plot(freq, phase_S21_raw, '--', label=f"{label} RAW")
        axs_phase[1,0].plot(freq, phase_S21_corr, label=f"{label} CORR")

        axs_phase[1,1].plot(freq, phase_S22_raw, '--', label=f"{label} RAW")
        axs_phase[1,1].plot(freq, phase_S22_corr, label=f"{label} CORR")

    # ---------- Configuración Magnitud ----------

    titles = ["S11", "S12", "S21", "S22"]

    for ax, title in zip(axs_mag.flat, titles):
        ax.set_title(title)
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Magnitude (dB)")
        ax.grid(True)
        ax.set_ylim(-80, 10)
        ax.legend()

    fig_mag.suptitle("RAW vs CORRECTED - Magnitude", fontsize=14)
    fig_mag.tight_layout()

    # ---------- Configuración Fase ----------

    for ax, title in zip(axs_phase.flat, titles):
        ax.set_title(title)
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Phase (degrees)")
        ax.grid(True)
        ax.legend()

    fig_phase.suptitle("RAW vs CORRECTED - Phase", fontsize=14)
    fig_phase.tight_layout()

    plt.show()


if __name__ == "__main__":

    print("=== Comparador de archivos S2P ===")

    try:

        print("\nSelecciona archivos RAW")
        raw_files = select_s2p_files("Selecciona archivos RAW")

        print("\nSelecciona archivos CORREGIDOS")
        corrected_files = select_s2p_files("Selecciona archivos CORREGIDOS")

        plot_s2p_comparison(raw_files, corrected_files)

    except Exception as e:

        print(f"\nError fatal: {e}")
        traceback.print_exc()
        input("Presione Enter para salir...")