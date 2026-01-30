"""MICRAEC - Microwave Error Correction

This module implements a GUI-based microwave error correction tool using SOLR technique.
It guides users through calibration kit selection, standard selection, and error measurement.
"""

import tkinter as tk
import time
import traceback
import numpy as np
import skrf as rf
from tkinter import filedialog

from calkit_utils import Parse_calkit, normalize_standards
from estimate_error_SOL import estimate_error_box_SOL, build_T_XA, build_T_XB
from get_gamma import read_gamma_in, compute_Gamma_L
from estimate_transmission_tracking import estimate_transmission_tracking
from debug_compare_thru import compare_thru_S21


def main():
    """Main entry point for the MICRAEC calibration workflow.
    
    Guides user through:
    1. Port connector type selection
    2. Calibration kit file selection
    3. Load standard selection per port
    4. Calibration measurement file loading
    5. Error parameter calculation
    """
    print("=== MICRAEC: Corrección de Errores de Microondas ===")
    print("Esta herramienta corrige errores en mediciones de microondas usando técnica SOLR")
    print("con las definiciones de kit de calibración proporcionadas.\n")

    # Solicitar sexo del conector en cada puerto
    sex_p1 = ask_port_sex(1)
    sex_p2 = ask_port_sex(2)

    print(f"Puerto 1: {'Macho' if sex_p1 == 'm' else 'Hembra'}")
    print(f"Puerto 2: {'Macho' if sex_p2 == 'm' else 'Hembra'}")

    # Seleccionar archivo de definiciones de kit de calibración
    print("\nSeleccione el archivo .xkt con las definiciones de estándar")
    time.sleep(0.5)
    
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo de calibración",
        filetypes=[("Archivos .xkt", "*.xkt"), ("Todos los archivos", "*.*")]
    )
    root.destroy()

    if not file_path:
        print("No se seleccionó ningún archivo.")
        return
    
    print(f"Archivo seleccionado: {file_path}")

    # Procesar datos de calibración
    cal_kit_raw = Parse_calkit(file_path)
    print(f"\nKit: {cal_kit_raw.get('label')}")
    print(f"Descripción: {cal_kit_raw.get('description')}")

    standards = normalize_standards(cal_kit_raw.get('standards'))
    
    if not isinstance(standards, list):
        raise TypeError(f"Error en formato de estándares: se esperaba lista, se obtuvo {type(standards)!r}")

    # Seleccionar estándares para ambos puertos
    try:
        load_p1 = select_load_for_port(standards, sex_p1, port_num=1)
        open_p1 = select_standard_for_port(standards, sex_p1, std_type='OPEN', port_num=1)
        short_p1 = select_standard_for_port(standards, sex_p1, std_type='SHORT', port_num=1)

        load_p2 = select_load_for_port(standards, sex_p2, port_num=2)
        open_p2 = select_standard_for_port(standards, sex_p2, std_type='OPEN', port_num=2)
        short_p2 = select_standard_for_port(standards, sex_p2, std_type='SHORT', port_num=2)

        print("\n=== Resumen de estándares seleccionados ===")
        print(f"Puerto 1: LOAD={load_p1.get('label')}, OPEN={open_p1.get('label')}, SHORT={short_p1.get('label')}")
        print(f"Puerto 2: LOAD={load_p2.get('label')}, OPEN={open_p2.get('label')}, SHORT={short_p2.get('label')}")
    except Exception as e:
        print(f"\nError al seleccionar estándares: {e}")
        traceback.print_exc()
        return
    
    # Obtener Gamma_in y frecuencia para ambos puertos
    datos_p1 = load_port_Gamma_in(1)
    datos_p2 = load_port_Gamma_in(2)

    # Validar que ambos puertos usen el mismo vector de frecuencia
    if not np.allclose(datos_p1['freq'], datos_p2['freq'], rtol=1e-5):
        print("\n⚠️ ADVERTENCIA: Los archivos del Puerto 1 y Puerto 2 tienen vectores de frecuencia diferentes.")
        print("Esto puede causar problemas en la calibración.")
        return

    freq = datos_p1['freq']

    # Calcular coeficientes de reflexión teóricos
    print("\nCalculando estándares Gamma_L teóricos...")
    try:
        gamma_l_p1 = compute_Gamma_L(freq, load_p1, open_p1, short_p1)
        gamma_l_p2 = compute_Gamma_L(freq, load_p2, open_p2, short_p2)
    except Exception as e:
        print(f"Error al calcular Gamma_L: {e}")
        traceback.print_exc()
        return

    # Calcular parámetros de error usando técnica SOLR
    print("\nCalculando parámetros de error (SOLR)...")
    try:
        # Puerto 1
        e00_p1, e10e01_p1, e11_p1 = estimate_error_box_SOL(
            {'short': datos_p1['gamma_short'], 'open': datos_p1['gamma_open'], 'load': datos_p1['gamma_load']},
            {'short': gamma_l_p1['short'], 'open': gamma_l_p1['open'], 'load': gamma_l_p1['load']}
        )

        # Puerto 2
        e33_p2, e23e32_p2, e22_p2 = estimate_error_box_SOL(
            {'short': datos_p2['gamma_short'], 'open': datos_p2['gamma_open'], 'load': datos_p2['gamma_load']},
            {'short': gamma_l_p2['short'], 'open': gamma_l_p2['open'], 'load': gamma_l_p2['load']}
        )

        print("\n=== Parámetros de Error - Puerto 1 ===")
        print(f"e00: {e00_p1}")
        print(f"e10*e01: {e10e01_p1}")
        print(f"e11: {e11_p1}")

        print("\n=== Parámetros de Error - Puerto 2 ===")
        print(f"e33: {e33_p2}")
        print(f"e23*e32: {e23e32_p2}")
        print(f"e22: {e22_p2}")

        # Construir matrices T de error
        T_XA_p1 = build_T_XA(e00_p1, e11_p1, e10e01_p1)
        T_XB_p2 = build_T_XB(e22_p2, e33_p2, e23e32_p2)

        # Cargar medición THRU
        print("\nSeleccione el archivo s2p del THRU")
        time.sleep(0.5)
        archivo_thru = select_s2p("Archivo de THRU")
        freq_thru, T_thru = read_thru_T_matrix(archivo_thru)

        # Calcular tracking de transmisión
        result_tracking = estimate_transmission_tracking(T_thru, T_XA_p1, T_XB_p2)
        S21_thru = np.asarray(result_tracking['S21_thru'], dtype=complex)
        
        print(f"\n✓ S21 del THRU estimado (primeros 5 puntos): {S21_thru[:5]}")

        # Comparar con medición de referencia
        print("\nSeleccione el THRU de referencia medido con PNA-X")
        time.sleep(0.5)
        archivo_thru_ref = select_s2p("THRU de referencia (PNA-X)")
        compare_thru_S21(freq, S21_thru, archivo_thru_ref)

        print("\n" + "="*50)
        print("✓ ¡Calibración completada exitosamente!")
        print("="*50)

    except Exception as e:
        print(f"\nError durante la calibración: {e}")
        traceback.print_exc()
        return

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
        
        if not (np.allclose(freq_short, freq_open, rtol=1e-9) and 
                np.allclose(freq_short, freq_load, rtol=1e-9)):
            print(f"\n⚠️ ERROR: Los archivos no tienen vectores de frecuencia idénticos.")
            print(f"Por favor, seleccione nuevamente los archivos del Puerto {port_num}.\n")
            continue
        
        # Validar que todos fueron medidos desde el mismo puerto
        puerto_short = datos['SHORT']['puerto']
        puerto_open = datos['OPEN']['puerto']
        puerto_load = datos['LOAD']['puerto']
        
        if not (puerto_short == puerto_open == puerto_load):
            print(f"\n⚠️ ERROR: Los estándares no fueron medidos desde el mismo puerto.")
            print(f"Detectados: SHORT={puerto_short}, OPEN={puerto_open}, LOAD={puerto_load}")
            print(f"Por favor, seleccione nuevamente los archivos del Puerto {port_num}.\n")
            continue
        
        print(f"\n✓ Archivos del Puerto {port_num} validados correctamente (puerto detectado: {puerto_short})\n")
        
        return {
            'freq': freq_short,
            'gamma_short': datos['SHORT']['gamma'],
            'gamma_open': datos['OPEN']['gamma'],
            'gamma_load': datos['LOAD']['gamma'],
            'puerto_detectado': puerto_short
        }


def ask_port_sex(port_num):
    """Ask user to specify the connector type (male/female) for a port.
    
    Parameters
    ----------
    port_num : int
        Port number (1 or 2)
        
    Returns
    -------
    str
        'f' for female (jack), 'm' for male (plug)
    """
    while True:
        sex = input(
            f"\nIndica el sexo del conector del PUERTO {port_num} "
            "(NO el del DUT) ('m' macho, 'f' hembra): "
        ).strip().lower()

        if sex in ('m', 'f'):
            return sex

        print("Entrada no válida. Usa 'm' o 'f'.")

        
def filter_standards_by_sex(standards, sex):
    """Filter standards by connector gender.
    
    Parameters
    ----------
    standards : list
        List of standard dictionaries
    sex : str
        'm' for male or 'f' for female
        
    Returns
    -------
    list
        Filtered standards matching the specified gender
    """
    return [s for s in standards if s.get('gender') == sex]


def get_load_standards(standards):
    """Extract LOAD standards from a standards list.
    
    Parameters
    ----------
    standards : list
        List of standard dictionaries
        
    Returns
    -------
    list
        Standards with type='LOAD'
    """
    return [s for s in standards if s.get('type') == 'LOAD']


def ask_user_to_select_load(loads):
    """Allow user to select a LOAD standard from available options.
    
    Parameters
    ----------
    loads : list
        List of available LOAD standards
        
    Returns
    -------
    dict
        Selected LOAD standard
        
    Raises
    ------
    RuntimeError
        If no LOAD standards are available
    """
    if not loads:
        raise RuntimeError("No se encontraron estándares LOAD en el kit de calibración")

    if len(loads) == 1:
        print(f"\nUsando LOAD: {loads[0]['label']}")
        return loads[0]

    print("\nSe encontraron múltiples LOADs en el kit:")
    default_idx = 1

    for i, s in enumerate(loads, start=1):
        label = s['label']
        fmin = float(s['freq_min']) / 1e9 if s['freq_min'] else 0
        fmax = float(s['freq_max']) / 1e9 if s['freq_max'] else 0

        is_broadband = 'broadband' in label.lower()
        if is_broadband:
            default_idx = i

        print(f"  {i}) {label}  [{fmin:.2f}–{fmax:.2f} GHz]"
              + ("  ← recomendado" if is_broadband else ""))

    while True:
        choice = input(f"\nSeleccione el LOAD a usar [default {default_idx}]: ").strip()

        if choice == "" and default_idx > 0:
            return loads[default_idx - 1]

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(loads):
                return loads[idx - 1]

        print("Entrada no válida. Ingrese un número o presione Enter para la opción predeterminada.")


def select_load_for_port(standards, sex, port_num):
    """Guide user to select a LOAD standard for a specific port.
    
    Parameters
    ----------
    standards : list
        List of all standards from calibration kit
    sex : str
        Connector gender ('m' or 'f')
    port_num : int
        Port number (1 or 2)
        
    Returns
    -------
    dict
        Selected LOAD standard
    """
    standards_sex = filter_standards_by_sex(standards, sex)
    load_standards = get_load_standards(standards_sex)

    print(f"\n=== Selección de LOAD para PUERTO {port_num} ===")
    return ask_user_to_select_load(load_standards)


def select_standard_for_port(standards, sex, std_type, port_num):
    """Select a specific standard type (OPEN or SHORT) for a port.
    
    Parameters
    ----------
    standards : list
        List of all standards from calibration kit
    sex : str
        Connector gender ('m' or 'f')
    std_type : str
        Standard type ('OPEN' or 'SHORT')
    port_num : int
        Port number (1 or 2)
        
    Returns
    -------
    dict
        Selected standard
        
    Raises
    ------
    RuntimeError
        If no matching standard is found
    """
    matching = [s for s in standards if s.get('type') == std_type and s.get('gender') == sex]
    
    if not matching:
        raise RuntimeError(f"No se encontró estándar {std_type} para género {sex}")
    
    if len(matching) == 1:
        print(f"Puerto {port_num} - {std_type}: {matching[0].get('label')}")
        return matching[0]
    
    # Si hay múltiples, seleccionar el primero (se podría mejorar con selección del usuario)
    print(f"Puerto {port_num} - {std_type}: {matching[0].get('label')} (auto-seleccionado)")
    return matching[0]


def select_s2p(title):
    """Open file dialog to select a Touchstone S2P file.
    
    Parameters
    ----------
    title : str
        Dialog window title
        
    Returns
    -------
    str
        Full path to selected file
        
    Raises
    ------
    RuntimeError
        If user cancels the file dialog
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    archivo = filedialog.askopenfilename(
        title=title,
        filetypes=[("Touchstone files", "*.s2p"), ("All files", "*.*")]
    )

    root.destroy()

    if not archivo:
        raise RuntimeError("No se seleccionó ningún archivo")

    return archivo

def read_thru_T_matrix(s2p_file):
    """Lee un archivo THRU (.s2p) y devuelve la matriz T (ABCD).

    Parameters
    ----------
    s2p_file : str
        Ruta al archivo THRU .s2p

    Returns
    -------
    freq : np.ndarray
        Vector de frecuencia (Hz)
    T : np.ndarray
        Matriz T (ABCD), shape (Nf, 2, 2)
    """
    ntwk = rf.Network(s2p_file)
    return ntwk.f, ntwk.a

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError fatal: {e}")
        traceback.print_exc()
        input("Presione Enter para salir...")
