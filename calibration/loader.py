import time
import numpy as np

from calibration.calkit_utils import Parse_calkit, normalize_standards
from calibration.gamma import read_gamma_in
from ui.file_dialogs import select_calkit, select_s2p


def load_and_validate_calkit():
    """Load calibration kit from user-selected file.

    Returns
    -------
    tuple
        (cal_kit_raw, standards) - raw kit data and normalized standards list
    """
    #print("\nSeleccione el archivo .xkt con las definiciones de estándar")
    #time.sleep(0.5)

    #file_path = select_calkit("Seleccionar archivo de calibración")
    file_path = "C:/Users/Diana/git/RFLAB_MicraEC/measurements/caltest/85052D.xkt"

    print(f"[DEBUG] Archivo seleccionado: {file_path}")

    cal_kit_raw = Parse_calkit(file_path)
    print(f"\nKit: {cal_kit_raw.get('label')}")
    print(f"Descripción: {cal_kit_raw.get('description')}")

    standards = normalize_standards(cal_kit_raw.get('standards'))
    print(f"[DEBUG]\nEstándares disponibles en el kit:",standards)   

    if not isinstance(standards, list):
        raise TypeError(
            f"Error en formato de estándares: se esperaba lista, se obtuvo {type(standards)!r}"
        )

    return cal_kit_raw, standards


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
        datos_Gamma_in = {}

        try:
            for std in standards_list:
                print(f"\nSeleccione el archivo {std} (Puerto {port_num})")
                archivo = select_s2p(f"{std} - Puerto {port_num}")

                freq, gamma = read_gamma_in(archivo, port_num)
                datos_Gamma_in[std] = {'freq': freq, 'gamma': gamma, 'puerto': port_num}
        except RuntimeError as e:
            print(f"Error: {e}")
            continue

        freq_short = datos_Gamma_in['SHORT']['freq']
        freq_open = datos_Gamma_in['OPEN']['freq']
        freq_load = datos_Gamma_in['LOAD']['freq']

        if not (
            np.allclose(freq_short, freq_open, rtol=1e-9)
            and np.allclose(freq_short, freq_load, rtol=1e-9)
        ):
            print("\nERROR: Los archivos no tienen vectores de frecuencia idénticos.")
            print(
                f"Por favor, seleccione nuevamente los archivos del Puerto {port_num}.\n"
            )
            continue

        puerto_short = datos_Gamma_in['SHORT']['puerto']
        puerto_open = datos_Gamma_in['OPEN']['puerto']
        puerto_load = datos_Gamma_in['LOAD']['puerto']

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
            'gamma_short': datos_Gamma_in['SHORT']['gamma'],
            'gamma_open': datos_Gamma_in['OPEN']['gamma'],
            'gamma_load': datos_Gamma_in['LOAD']['gamma'],
            'puerto_detectado': puerto_short,
        }
