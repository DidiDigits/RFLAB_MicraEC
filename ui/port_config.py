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


def get_port_configuration():
    """Get port connector types from user.
    
    Returns
    -------
    tuple
        (sex_p1, sex_p2) where 'm' = male, 'f' = female
    """
    sex_p1 = ask_port_sex(1)
    sex_p2 = ask_port_sex(2)
    print(f"Puerto 1: {'Macho' if sex_p1 == 'm' else 'Hembra'}")
    print(f"Puerto 2: {'Macho' if sex_p2 == 'm' else 'Hembra'}")
    return sex_p1, sex_p2