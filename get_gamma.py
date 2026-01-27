import skrf as rf
import numpy as np

def read_gamma_in(s2p_file):
    """
    Lee un archivo s2p y detecta automáticamente
    el coeficiente de reflexión útil (S11 o S22).

    Returns
    -------
    freq : np.ndarray
        Frecuencia en Hz (shape: N)
    gamma_in : np.ndarray
        Coeficiente de reflexión complejo (shape: N)
    puerto : str
        'S11' o 'S22'
    metricas : dict
        Métricas usadas para la detección
            Esto es porque a veces el VNA tiene efectos de incertidumbre que pueden hacer pensar que hay datos utiles donde no los hay
    """

    ntwk = rf.Network(s2p_file)

    freq = ntwk.f  # Hz, shape (N,)
    S = ntwk.s     # shape (N, 2, 2)

    candidatos = {
        "S11": S[:, 0, 0],
        "S22": S[:, 1, 1],
    }

    metricas = {}
    scores = {}

    for key, sij in candidatos.items():
        mag = np.abs(sij)

        metricas[key] = {
            "mag_media": np.mean(mag),
            "mag_std": np.std(mag),
            "energia": np.mean(mag**2),
        }

        # Reflexión útil: grande y relativamente estable
        scores[key] = metricas[key]["energia"] / (metricas[key]["mag_std"] + 1e-12)

    puerto = max(scores, key=scores.get)
    gamma_in = candidatos[puerto]

    return freq, gamma_in, puerto, metricas

if __name__ == "__main__":
    import sys

    s2p_file = sys.argv[1]

    freq, gamma_in, puerto, metricas = read_gamma_in(s2p_file)

    print(f"Puerto detectado: {puerto}")
    print("Primeras frecuencias:", freq[:5])
    print("Primeros Gamma_in:", gamma_in[:5])
    print("Métricas de detección:", metricas)