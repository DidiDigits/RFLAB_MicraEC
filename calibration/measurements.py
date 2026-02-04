import numpy as np

from calibration.gamma import read_gamma_in
from ui.file_dialogs import select_s2p


def load_port_Gamma_in(port_num):
    """Carga y valida archivos de medición de calibración (SHORT, OPEN, LOAD) para un puerto.

    Solicita archivos S2P para estándares SHORT, OPEN y LOAD y valida que:
    - Todos los archivos tengan vectores de frecuencia idénticos
    - Todos los archivos sean medidos desde el mismo puerto

    Repite si la validación falla.

    Parámetros
    ----------
    port_num : int
        Número de puerto (1 o 2)

    Retorna
    -------
    dict
        Diccionario con claves:
        - 'freq': arreglo de frecuencia (Hz)
        - 'gamma_short': arreglo de coeficiente de reflexión
        - 'gamma_open': arreglo de coeficiente de reflexión
        - 'gamma_load': arreglo de coeficiente de reflexión
        - 'puerto_detectado': número de puerto detectado
    """
    print(f"\n=== Archivos de Calibración - PUERTO {port_num} ===\n")

    standards_list = ['SHORT', 'OPEN', 'LOAD']

    while True:
        datos = {}

        try:
            for std in standards_list:
                print(f"\nSeleccione el archivo {std} (Puerto {port_num})")
                archivo = select_s2p(f"{std} - Puerto {port_num}")

                # Leer datos
                freq, gamma = read_gamma_in(archivo, port_num)
                datos[std] = {'freq': freq, 'gamma': gamma, 'puerto': port_num}
        except RuntimeError as e:
            print(f"Error: {e}")
            continue

        # Validar que todos tengan el mismo vector de frecuencia
        freq_short = datos['SHORT']['freq']
        freq_open = datos['OPEN']['freq']
        freq_load = datos['LOAD']['freq']

        if not (
            np.allclose(freq_short, freq_open, rtol=1e-9)
            and np.allclose(freq_short, freq_load, rtol=1e-9)
        ):
            print("\nERROR: Los archivos no tienen vectores de frecuencia idénticos.")
            print(
                f"Por favor, seleccione nuevamente los archivos del Puerto {port_num}.\n"
            )
            continue

        # Validar que todos fueron medidos desde el mismo puerto
        puerto_short = datos['SHORT']['puerto']
        puerto_open = datos['OPEN']['puerto']
        puerto_load = datos['LOAD']['puerto']

        if not (puerto_short == puerto_open == puerto_load):
            print("\n ERROR: Los estándares no fueron medidos desde el mismo puerto.")
            print(
                f"Detectados: SHORT={puerto_short}, OPEN={puerto_open}, LOAD={puerto_load}"
            )
            print(
                f"Por favor, seleccione nuevamente los archivos del Puerto {port_num}.\n"
            )
            continue

        print(
            f"\n✓ Archivos del Puerto {port_num} validados correctamente "
            f"(puerto detectado: {puerto_short})\n"
        )

        return {
            'freq': freq_short,
            'gamma_short': datos['SHORT']['gamma'],
            'gamma_open': datos['OPEN']['gamma'],
            'gamma_load': datos['LOAD']['gamma'],
            'puerto_detectado': puerto_short,
        }
