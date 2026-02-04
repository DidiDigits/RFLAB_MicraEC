import time

from calibration.calkit_utils import Parse_calkit, normalize_standards
from ui.file_dialogs import select_calkit


def load_and_validate_calkit():
    """Load calibration kit from user-selected file.

    Returns
    -------
    tuple
        (cal_kit_raw, standards) - raw kit data and normalized standards list
    """
    print("\nSeleccione el archivo .xkt con las definiciones de estándar")
    time.sleep(0.5)

    file_path = select_calkit("Seleccionar archivo de calibración")

    print(f"Archivo seleccionado: {file_path}")

    cal_kit_raw = Parse_calkit(file_path)
    print(f"\nKit: {cal_kit_raw.get('label')}")
    print(f"Descripción: {cal_kit_raw.get('description')}")

    standards = normalize_standards(cal_kit_raw.get('standards'))

    if not isinstance(standards, list):
        raise TypeError(
            f"Error en formato de estándares: se esperaba lista, se obtuvo {type(standards)!r}"
        )

    return cal_kit_raw, standards
