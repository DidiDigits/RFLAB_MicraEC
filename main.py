"""MICRAEC - Microwave Error Correction

This module implements a GUI-based microwave error correction tool using SOLR technique.
It guides users through calibration kit selection, standard selection, and error measurement.
"""

import traceback

from calibration.loader import load_and_validate_calkit
from calibration.loader import load_port_Gamma_in
from calibration.calculator import validate_frequency_vectors, calculate_error_parameters
from calibration.transmission import find_transmission_tracking
from ui.standard_selection import select_standards_for_port
from ui.file_dialogs import select_output_folder
from correction.correct_measure import correct_measure_s2p, save_corrected_s2p


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

    try:
        # Step 1: Get port configuration
        #sex_p1, sex_p2 = get_port_configuration()
        sex_p1 = 'f'
        sex_p2 = 'f'

        # Step 2: Load and validate calibration kit and get Z_ref
        cal_kit_raw, standards = load_and_validate_calkit()
        zref = float(cal_kit_raw['connectors'][0]['z0'])   # Impedancia de refrencia del kit (asumimos que es la misma para generos)

        # Step 3: Select standards for both ports
        standards_p1 = select_standards_for_port(standards, sex_p1, port_num=1)
        standards_p2 = select_standards_for_port(standards, sex_p2, port_num=2)

        # Step 4: Gamma (Short, Open, Load) measurements for both ports
        gamma_in_p1 = load_port_Gamma_in(1)
        gamma_in_p2 = load_port_Gamma_in(2)

        # Step 5: Validate frequency vectors (Both ports must match)
        validate_frequency_vectors(gamma_in_p1['freq'], gamma_in_p2['freq'])
        freq = gamma_in_p1['freq'] #Toma el vector de frecuencia común

        # Step 6: Calculate error parameters (e00, e11, e10*e01 for Port 1 and e33, e22, e23*e32 for Port 2)
        error_params_p1, error_params_p2 = calculate_error_parameters(
            freq, gamma_in_p1, gamma_in_p2, standards_p1, standards_p2, zref,
        )
        TXA = error_params_p1['T_XA']
        TXB = error_params_p2['T_XB']
        # plot_error_parameters(freq, error_params_p1, error_params_p2)

        # Step 7: Find transmission tracking (alpha)
        alpha = find_transmission_tracking(freq, error_params_p1, error_params_p2)

        print("¡Calibración completada exitosamente!")

        # Step 8: Apply error correction to measurements and save
        corrected = correct_measure_s2p(TXA, TXB, freq, alpha)
        output_dir = select_output_folder()
        save_corrected_s2p(corrected, output_dir)

        print("\nMediciones corregidas guardadas correctamente.")





    except Exception as e:
        print(f"\nError fatal: {e}")
        traceback.print_exc()
        return

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError fatal: {e}")
        traceback.print_exc()
        input("Presione Enter para salir...")
