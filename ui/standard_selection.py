def select_standards_for_port(standards, sex, port_num):
    """Select LOAD, OPEN, and SHORT standards for a port.

    Parameters
    ----------
    standards : list
        All available standards
    sex : str
        Port connector gender ('m' or 'f')
    port_num : int
        Port number (1 or 2)

    Returns
    -------
    dict
        Dictionary with 'load', 'open', 'short' keys
    """
    print(f"\n=== Selección de Estándares - PUERTO {port_num} ===")

    load = select_load_for_port(standards, sex, port_num)
    open_std = select_standard_for_port(standards, sex, 'OPEN', port_num)
    short_std = select_standard_for_port(standards, sex, 'SHORT', port_num)

    print(
        f"\nPuerto {port_num}: LOAD={load.get('label')}, OPEN={open_std.get('label')}, "
        f"SHORT={short_std.get('label')}"
    )

    return {'load': load, 'open': open_std, 'short': short_std}


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

        print(
            f"  {i}) {label}  [{fmin:.2f}–{fmax:.2f} GHz]"
            + ("  ← recomendado" if is_broadband else "")
        )

    while True:
        choice = input(f"\nSeleccione el LOAD a usar [default {default_idx}]: ").strip()

        if choice == "" and default_idx > 0:
            return loads[default_idx - 1]

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(loads):
                return loads[idx - 1]

        print("Entrada no válida. Ingrese un número o presione Enter para la opción predeterminada.")
