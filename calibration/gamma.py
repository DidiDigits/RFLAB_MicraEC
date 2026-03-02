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
    idx = puerto - 1
    gamma_in = S[:, idx, idx]

    return freq, gamma_in


def compute_Gamma_L(freq, load_std, open_std, short_std, zref):
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
    out = {}

    out['load']  = gamma_standard(freq, load_std['model']['params'],  zref, 'fixed_load')
    out['open']  = gamma_standard(freq, open_std['model']['params'],  zref, 'open')
    out['short'] = gamma_standard(freq, short_std['model']['params'], zref, 'short')

    return out

def gamma_standard(freq, params, zref, kind):

    import numpy as np

    gamma_l, Gamma1 = offset_model(freq, params, zref)

    if kind == 'short':
        ZT = ZT_short(freq, params)

    elif kind == 'open':
        ZT = ZT_open(freq, params)

    elif kind == 'fixed_load':
        ZT = ZT_load(freq, params, zref)

    else:
        raise ValueError("Tipo de estándar no soportado")

    GammaT = (ZT - zref) / (ZT + zref)

    exp_term = np.exp(-2 * gamma_l)

    numerator = Gamma1 * (1 - exp_term - Gamma1*GammaT) + GammaT*exp_term
    denominator = 1 - Gamma1 * (Gamma1*exp_term + GammaT*(1 - exp_term))

    return numerator / denominator


def ZT_load(freq, params, zref):
    """
    Impedancia de terminación del LOAD fijo.
    """
    # Si el modelo incluye un valor explícito de resistencia
    R = params.get('R')

    if R is not None:
        return float(R)

    # Si no, asumimos carga igual a zref
    return zref


def ZT_open(freq, params):
    C0 = float(params.get('C0', 0.0))
    C1 = float(params.get('C1', 0.0))
    C2 = float(params.get('C2', 0.0))
    C3 = float(params.get('C3', 0.0))

    freq = np.asarray(freq)
    C = C0 + C1*freq + C2*freq**2 + C3*freq**3

    w = 2*np.pi*freq
    return np.where(C != 0, 1/(1j*w*C), 1e20)

def ZT_short(freq, params):
    L0 = float(params.get('L0', 0.0))
    L1 = float(params.get('L1', 0.0))
    L2 = float(params.get('L2', 0.0))
    L3 = float(params.get('L3', 0.0))

    freq = np.asarray(freq)
    L = L0 + L1*freq + L2*freq**2 + L3*freq**3
    return 1j * 2*np.pi*freq * L

def offset_model(freq, params, zref):

    Z0    = float(params.get('offset_z0', 50.0))
    delay = float(params.get('offset_delay', 0.0))
    print("El delay es:", delay)
    loss  = float(params.get('offset_loss', 0.0)) / 1e9  # Ω/√GHz real

    freq = np.asarray(freq, dtype=float)
    f = np.where(freq == 0, 1e-30, freq)

    f_GHz = f / 1e9

    term = (1 - 1j) * loss / (2*np.pi*np.sqrt(f_GHz)*Z0)

    gamma_l = 1j * 2*np.pi*f*delay * np.sqrt(1 + term)
    Zc = Z0 * np.sqrt(1 + term)

    Gamma1 = (Zc - zref) / (Zc + zref)

    return gamma_l, Gamma1
