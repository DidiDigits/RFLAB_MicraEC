# MICRAEC - Microwave Error Correction
# main.py
import tkinter as tk
import time
import sys
import re
import traceback

from tkinter import filedialog
from calkit_utils import Parse_calkit

def ask_port_sex(port_num):
    while True:
        sex = input(
            f"\nIndica el sexo del conector del PUERTO {port_num} "
            "(NO el del DUT) ('m' macho, 'f' hembra): "
        ).strip().lower()

        if sex in ('m', 'f'):
            return sex

        print("Entrada no válida. Usa 'm' o 'f'.")

        
def filter_standards_by_sex(standards, sex):
    """
    sex: 'm' o 'f'
    """
    if sex not in ('m', 'f'):
        return standards

    key = 'M' if sex == 'm' else 'F'
    pattern = re.compile(rf'(-{key}-|-{key}$|\({key}\)|\b{key}\b|MALE|FEMALE)', re.IGNORECASE)
    return [std for std in standards if pattern.search(std.get('label', '') or '')]

def get_load_standards(standards):
    return [
        s for s in standards
        if 'load' in (s.get('type', '').lower() +
                      s.get('label', '').lower())
    ]

def ask_user_to_select_load(loads):
    """
    Muestra los LOADs disponibles y permite al usuario elegir uno.
    Prioriza Broadband Load como sugerencia.
    """
    if not loads:
        raise RuntimeError("No se encontraron LOADs en el calkit")

    if len(loads) == 1:
        return loads[0]

    print("\nSe encontraron múltiples LOADs en el kit:")
    default_idx = 0

    for i, s in enumerate(loads, start=1):
        label = s.get('label', 'SIN LABEL')
        fmin = float(s.get('s_min_freq', 0)) / 1e9
        fmax = float(s.get('s_max_freq', 0)) / 1e9

        is_broadband = 'broadband' in label.lower()
        if is_broadband:
            default_idx = i

        print(f"  {i}) {label}  [{fmin:.2f}–{fmax:.2f} GHz]"
              + ("  ← recomendado" if is_broadband else ""))

    while True:
        prompt = f"\nSeleccione el LOAD a usar [default {default_idx}]: "
        choice = input(prompt).strip()

        if choice == "" and default_idx > 0:
            return loads[default_idx - 1]

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(loads):
                return loads[idx - 1]

        print("Entrada no válida. Intente nuevamente.")

def select_load_for_port(standards, sex, port_num):
    standards_sex = filter_standards_by_sex(standards, sex)
    load_standards = get_load_standards(standards_sex)

    print(f"\n=== Selección de LOAD para PUERTO {port_num} ===")
    return ask_user_to_select_load(load_standards)


def main():
    #Introduction for the user
    print("=== MICRAEC: Microwave Error Correction ===")
    print("El programa corrige errores en mediciones de microondas utilizando la técnica SOLR y el archivo de definiciones de estandar proporcionado.")


    #Ask port sex tu user
    sex_p1 = ask_port_sex(1)
    sex_p2 = ask_port_sex(2)

    print(f"Puerto 1: {'Macho' if sex_p1 == 'm' else 'Hembra'}")
    print(f"Puerto 2: {'Macho' if sex_p2 == 'm' else 'Hembra'}")

    # Open file explorer to select file calkit location
    print("\nSeleccione ruta y nombre del archivo .xkt con las definiciones de estandár en la ventana emergente")
    time.sleep(1)
    root = tk.Tk()
    root.withdraw()
    
    # Select standard definitions file
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo de calibración",
        filetypes=[("Archivos .xkt", "*.xkt"), ("Todos los archivos", "*.*")]
    )

    if not file_path:
        print("No se seleccionó ningún archivo.")
        return
    
    print(f"Archivo seleccionado: {file_path}")

    # Get calibration data from file
    cal_kit = Parse_calkit(file_path)
    print(cal_kit.get('label'))
    print(cal_kit.get('description'))  
    #print(cal_kit)

    standards = cal_kit.get('standards')
    try:
        if not isinstance(standards, list):
            raise TypeError(f"expected list for 'standards', got {type(standards)!r}")

        load_p1 = select_load_for_port(standards, sex_p1, port_num=1)
        load_p2 = select_load_for_port(standards, sex_p2, port_num=2)

        print("\nResumen de LOADs seleccionados:")
        print("Puerto 1:", load_p1.get("label"))
        print("Puerto 2:", load_p2.get("label"))

        
    except Exception as e:
        print("Error al filtrar standards por sexo:", repr(e))
        print("Tipo de 'standards':", type(standards))
        try:
            labels = [s.get('label') for s in standards[:10]] if isinstance(standards, list) else None
        except Exception as e2:
            labels = f"<no se pudieron extraer labels: {e2}>"
        print("Primeros labels:", labels)
        traceback.print_exc()
        return
    


    # Get data for \Gamma_L calculation


if __name__ == "__main__":
    main()
