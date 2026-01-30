import xml.etree.ElementTree as ET

def Parse_calkit(file_path):
# Parses a calibration kit file (.xkt) and creates a dictionary (cal_kit_data) 
# containing the calibration kit's label, description, connectors, and a list of standards.
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    #Dictionary to store the parsed calibration kit data.
    cal_kit_data = {} 

    #Extract the calibration kit´s label and description from the XML file.
    cal_kit_data["label"] = root.find("CalKitLabel").text #Kit label
    cal_kit_data["description"] = root.find("CalKitDescription").text

    # Extract the list of connectors (family, gender, frequency range, and impedance).
    connectors =  []
    for connector in root.findall("ConnectorList/Coaxial"):
        connectors.append({ 
            "family": connector.find("Family").text,
            "gender": connector.find("Gender").text,
            "c_max_freq" : connector.find("MaximumFrequencyHz").text,
            "c_min_freq" : connector.find("MinimumFrequencyHz").text,
            "z0" : connector.find("SystemZ0").text
        })
    cal_kit_data["connectors"] = connectors

    # Extract the list of standards. Each standard contains its type, label, standard number, 
    # coefficients (if available), and offsets (if any).
    standards = []
    for standard in root.findall("StandardList/*"):
        std_data = { #Dictionary
            "type" : standard.tag, 
            "label" : standard.find("Label").text, 
            "StdNo" : standard.find("StandardNumber").text,
            "s_min_freq" : standard.find("MinimumFrequencyHz").text,
            "s_max_freq" : standard.find("MaximumFrequencyHz").text}

        #Extract coefficients (if they exist).
        if standard.find("C0") is not None:
            std_data["C0"] = standard.find("C0").text
        if standard.find("C1") is not None:
            std_data["C1"] = standard.find("C1").text
        if standard.find("C2") is not None:
            std_data["C2"] = standard.find("C2").text
        if standard.find("C3") is not None:
            std_data["C3"] = standard.find("C3").text
        if standard.find("L0") is not None:
            std_data["L0"] = standard.find("L0").text
        if standard.find("L1") is not None:
            std_data["L1"] = standard.find("L1").text
        if standard.find("L2") is not None:
            std_data["L2"] = standard.find("L2").text
        if standard.find("L3") is not None:
            std_data["L3"] = standard.find("L3").text

        # Extract offsets (if they exist)
        offset = standard.find("Offset")  
        if offset is not None:
            # Extrae los datos de Offset
            ofs_data = { 
                "OffsetDelay": offset.find("OffsetDelay").text,
                "OffsetLoss": offset.find("OffsetLoss").text,
                "OffsetZ0": offset.find("OffsetZ0").text}
            
            std_data["offsets"] = ofs_data

        standards.append(std_data)
    
    cal_kit_data["standards"] = standards

    # Extract the list of classes
    classes =  []
    for class_kit in root.findall("KitClasses"):
        classes.append({
            "ClassID" : class_kit.find("KitClassID").text,
            "StdList" : class_kit.find("StandardsList").text,
            "ClassLabel" : class_kit.find("KitClassLabel").text
        })
    cal_kit_data["classes"] = classes

    # Return the parsed calibration kit data
    return cal_kit_data

def normalize_standards(raw_standards):
    """
    Convierte la lista de estándares crudos del calkit
    a una estructura interna homogénea.
    """
    if isinstance(raw_standards, dict):
        raw_standards = raw_standards.get('standards', [])

    if not isinstance(raw_standards, list):
        raise TypeError(f"expected list or dict for 'raw_standards', got {type(raw_standards)!r}")

    normalized = []

    for s in raw_standards:
        if not isinstance(s, dict):
            raise TypeError(f"expected dict items in standards list, got {type(s)!r}")

        entry = {
            'label': s.get('label') or s.get('Label'),
            'description': s.get('description') or s.get('Description'),
            'port_connector': s.get('PortConnectorIDs') or s.get('port_connector'),
            'freq_min': s.get('MinimumFrequencyHz') or s.get('s_min_freq'),
            'freq_max': s.get('MaximumFrequencyHz') or s.get('s_max_freq'),
            'standard_number': s.get('StandardNumber') or s.get('StdNo'),
        }

        label = (entry.get('label') or '').upper()

        # ---------- TIPO ----------
        if 'LOAD' in label:
            entry['type'] = 'LOAD'
        elif 'OPEN' in label:
            entry['type'] = 'OPEN'
        elif 'SHORT' in label:
            entry['type'] = 'SHORT'
        elif 'THRU' in label:
            entry['type'] = 'THRU'
        else:
            fallback_type = (s.get('type') or '').upper()
            if 'LOAD' in fallback_type:
                entry['type'] = 'LOAD'
            elif 'OPEN' in fallback_type:
                entry['type'] = 'OPEN'
            elif 'SHORT' in fallback_type:
                entry['type'] = 'SHORT'
            elif 'THRU' in fallback_type:
                entry['type'] = 'THRU'
            else:
                entry['type'] = 'UNKNOWN'

        # ---------- GÉNERO ----------
        if '-M-' in label or ' MALE' in label.upper():
            entry['gender'] = 'm'
        elif '-F-' in label or ' FEMALE' in label.upper():
            entry['gender'] = 'f'
        else:
            entry['gender'] = None

        # ---------- MODELO ----------
        model = {}

        if entry['type'] == 'LOAD':
            if 'Offset1StdIndex' in s or 'Offset2StdIndex' in s or 'TerminationStdIndx' in s:
                model['kind'] = 'offset_load'
                model['refs'] = {
                    'offset1': s.get('Offset1StdIndex'),
                    'offset2': s.get('Offset2StdIndex'),
                    'termination': s.get('TerminationStdIndx')
                }
            else:
                model['kind'] = 'fixed_load'
                off = s.get('Offset') or s.get('offsets') or {}
                model['params'] = {
                    'offset_delay': off.get('OffsetDelay', 0.0),
                    'offset_loss': off.get('OffsetLoss', 0.0),
                    'offset_z0': off.get('OffsetZ0', 50.0),
                    'ZL': 50.0
                }

        elif entry['type'] == 'OPEN':
            off = s.get('Offset') or s.get('offsets') or {}
            model['kind'] = 'open'
            model['params'] = {
                'C0': s.get('C0'),
                'C1': s.get('C1'),
                'C2': s.get('C2'),
                'C3': s.get('C3'),
                'offset_delay': off.get('OffsetDelay'),
                'offset_loss': off.get('OffsetLoss'),
                'offset_z0': off.get('OffsetZ0'),
            }

        elif entry['type'] == 'SHORT':
            off = s.get('Offset') or s.get('offsets') or {}
            model['kind'] = 'short'
            model['params'] = {
                'L0': s.get('L0'),
                'L1': s.get('L1'),
                'L2': s.get('L2'),
                'L3': s.get('L3'),
                'offset_delay': off.get('OffsetDelay'),
                'offset_loss': off.get('OffsetLoss'),
                'offset_z0': off.get('OffsetZ0'),
            }

        entry['model'] = model
        normalized.append(entry)

    return normalized
