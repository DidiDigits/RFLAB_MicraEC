"""Gamma calculation utilities for calibration standards.

This module provides functions to read gamma measurements from S2P files
and compute theoretical Gamma_L for LOAD, OPEN, and SHORT standards.
"""

import skrf as rf
import numpy as np
import matplotlib.pyplot as plt



def read_gamma_in(s2p_file, puerto):
    """
    Lee un archivo s2p y devuelve el párametro S11 o S22 (Gamma_in) dependiendo del puerto indicado.
    gamma_in es el gamma medido para los tres estándares de calibración (SHORT, OPEN, LOAD).

    Parameters
    ----------
    s2p_file : str
        Ruta al archivo Touchstone (.s2p)
    puerto : int
        Número de puerto físico (1 o 2)

    Returns
    -------
    freq : np.ndarray
        Vector de frecuencia (Hz)
    gamma_in : np.ndarray
        Coeficiente de reflexión complejo medido
    """

    if puerto not in (1, 2):
        raise ValueError("puerto debe ser 1 o 2")

    ntwk = rf.Network(s2p_file)

    freq = ntwk.f
    S = ntwk.s

    #Debug
    plt.figure()
    plt.plot(freq, 20 * np.log10(np.abs(S[:, puerto-1, puerto-1])), label=f"S{puerto}{puerto} medido")
    plt.title(f"Medición S{puerto}{puerto} (Gamma_in)")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud (dB)")
    plt.grid()  
    # Pause to view the plots
    input("\nPresione Enter para continuar...")

    idx = puerto - 1
    gamma_in = S[:, idx, idx]

    return freq, gamma_in


def compute_Gamma_L(freq, load_std, open_std, short_std):
    """
    Calcula Gamma_L teórico para LOAD, OPEN y SHORT.

    Parameters
    ----------
    freq : np.ndarray
        Vector de frecuencia (Hz)
    load_std : dict
        Estándar LOAD seleccionado por el usuario
    open_std : dict
        Estándar OPEN correspondiente al puerto
    short_std : dict
        Estándar SHORT correspondiente al puerto

    Returns
    -------
    dict
        {'load', 'open', 'short'}
    """

    from debug.debug_utils import plot_gamma
    out = {}

    # LOAD
    if load_std['model']['kind'] != 'fixed_load':
        raise NotImplementedError("Solo se soporta fixed_load por ahora")

    out['load'] = gamma_load(freq, load_std['model']['params'])
    plot_gamma(freq, out['load'], 'LOAD')

    # OPEN
    out['open'] = gamma_open(freq, open_std['model']['params'])
    plot_gamma(freq, out['open'], 'OPEN')

    # SHORT
    out['short'] = gamma_short(freq, short_std['model']['params'])
    plot_gamma(freq, out['short'], 'SHORT')

    return out


def gamma_load(freq, params):
    """
    Gamma_L para LOAD fijo
    """
    Z0 = float(params.get('offset_z0', 50.0)) if params.get('offset_z0') else 50.0
    ZL = float(params.get('ZL', 50.0)) if params.get('ZL') else 50.0

    Gamma = (ZL - Z0) / (ZL + Z0)

    return Gamma * np.ones_like(freq, dtype=complex)


def gamma_open(freq, params):
    """
    Gamma_L para OPEN con modelo capacitivo
    """

    def to_float(val, default=0.0):
        if val is None:
            return default
        return float(val)

    C0 = to_float(params.get('C0'))
    C1 = to_float(params.get('C1'))
    C2 = to_float(params.get('C2'))
    C3 = to_float(params.get('C3'))
    Z0 = to_float(params.get('offset_z0'), 50.0)

    w = 2 * np.pi * freq
    C = C0 + C1 * freq + C2 * freq**2 + C3 * freq**3

    # Evitar división por cero
    Z = np.where(C != 0, 1 / (1j * w * C), 1e20)
    return (Z - Z0) / (Z + Z0)


def gamma_short(freq, params):
    """
    Gamma_L para SHORT con modelo inductivo
    """

    def to_float(val, default=0.0):
        if val is None:
            return default
        return float(val)

    L0 = to_float(params.get('L0'))
    L1 = to_float(params.get('L1'))
    L2 = to_float(params.get('L2'))
    L3 = to_float(params.get('L3'))
    Z0 = to_float(params.get('offset_z0'), 50.0)

    w = 2 * np.pi * freq
    L = L0 + L1 * freq + L2 * freq**2 + L3 * freq**3

    Z = 1j * w * L
    return (Z - Z0) / (Z + Z0)
