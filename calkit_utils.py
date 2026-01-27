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