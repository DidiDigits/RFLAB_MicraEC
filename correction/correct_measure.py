import os
import numpy as np
import skrf as rf

from calibration.loader import load_and_validate_measurement_s2p
from calibration.transmission import s_to_chain_T


def correct_measure_s2p(TXA, TXB, freq, alpha):

    measurements = load_and_validate_measurement_s2p(freq)

    freq = np.asarray(freq)
    N = len(freq)

    assert TXA.shape == (N,2,2)
    assert TXB.shape == (N,2,2)
    assert alpha.shape == (N,)

    corrected = []

    TXA_inv = np.linalg.inv(TXA)
    TXB_inv = np.linalg.inv(TXB)

    for meas in measurements:

        S = np.zeros((N,2,2),dtype=complex)
        S[:,0,0] = meas["S11"]
        S[:,0,1] = meas["S12"]
        S[:,1,0] = meas["S21"]
        S[:,1,1] = meas["S22"]

        class Dummy: pass
        ntwk = Dummy()
        ntwk.s = S

        TM = s_to_chain_T(ntwk)

        TDUT = TXA_inv @ TM @ TXB_inv
        TDUT /= alpha[:,None,None]

        corrected.append({
            "filename": meas["filename"],
            "freq": freq,
            "T": TDUT
        })

    return corrected

def chain_T_to_s(T):
    """
    Convierte matrices chain T a parámetros S.

    Parámetros
    ----------
    T : ndarray (Nfreq, 2, 2)

    Retorna
    -------
    S : ndarray (Nfreq, 2, 2)
    """

    Nf = T.shape[0]
    S = np.zeros((Nf, 2, 2), dtype=complex)

    T11 = T[:,0,0]
    T12 = T[:,0,1]
    T21 = T[:,1,0]
    T22 = T[:,1,1]

    detT = T11*T22 - T12*T21

    S[:,1,0] = 1.0 / T22
    S[:,0,0] = T12 / T22
    S[:,1,1] = -T21 / T22
    S[:,0,1] = detT / T22

    return S

def save_corrected_s2p(corrected_data, output_dir):
    """
    Guarda resultados corregidos como archivos S2P.

    Parámetros
    ----------
    corrected_data : list
        Resultado de correct_measure_s2p()

    output_dir : str
        Carpeta donde guardar archivos
    """

    os.makedirs(output_dir, exist_ok=True)

    for meas in corrected_data:

        freq = meas["freq"]
        T = meas["T"]

        S = chain_T_to_s(T)

        ntwk = rf.Network()
        ntwk.s = S
        ntwk.frequency = rf.Frequency.from_f(freq, unit="hz")

        filename = os.path.splitext(meas["filename"])[0]
        out_path = os.path.join(output_dir, filename + "_corrected.s2p")

        ntwk.write_touchstone(out_path)

        print(f"Guardado: {out_path}")