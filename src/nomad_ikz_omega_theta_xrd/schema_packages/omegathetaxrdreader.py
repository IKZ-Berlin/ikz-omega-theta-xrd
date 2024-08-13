import xml.etree.ElementTree as ET


def parse_element(element):
    """Recursively parse an XML element and convert it to a dictionary."""
    parsed = {}
    if element.attrib:
        parsed.update(element.attrib)
    if element.text and element.text.strip():
        parsed['text'] = element.text.strip()
    for child in element:
        child_parsed = parse_element(child)
        if child.tag in parsed:
            if not isinstance(parsed[child.tag], list):
                parsed[child.tag] = [parsed[child.tag]]
            parsed[child.tag].append(child_parsed)
        else:
            parsed[child.tag] = child_parsed
    return parsed


def extract_data_and_metadata(file_path):
    """Extract data and metadata from the XML file and return as a dictionary."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    parsed_data = parse_element(root)
    return parsed_data


def extract_general_info(
    xrd_dict,
):  # xrd_dict.get('MultiMeasurement',{}).get('Measurements',{}).get('Measurement')[i]) oder xrd_dict.get('MultiMeasurement',{})
    """Extract general information from the XRD data."""
    general_info = {
        'name': xrd_dict.get('Info', {}).get('Name'),
        'original_name': xrd_dict.get('Info', {}).get('OriginalName'),
        'time_stamp': xrd_dict.get('Info', {}).get('TimeStamp'),
        'user': xrd_dict.get('Info', {}).get('User'),
        'description': xrd_dict.get('Info', {}).get('Comment'),
        'scan_recipe_name': xrd_dict.get('Info', {}).get('RecipeName'),
        'type': xrd_dict.get('Info', {}).get('Type'),
        'x_pos': xrd_dict.get('Info', {}).get('XPos'),
        'y_pos': xrd_dict.get('Info', {}).get('YPos'),
        'device_serial_no': xrd_dict.get('Info', {}).get('DeviceSerialNo'),
    }
    return general_info


def extract_parameter_list(
    xrd_dict,
):  # xrd_dict.get('MultiMeasurement',{}).get('Measurements',{}).get('Measurement')[i])
    iterator = 0
    """Extract parameter list from the XRD data."""
    parameter_list = {
        #'xpos': xrd_dict.get('MultiMeasurement', {}).get('Results', {}).get('Result')[iterator].get('ParameterList', {}).get('Parameter')[3].get('Value'),
        'xpos': xrd_dict.get('Result')
        .get('ParameterList', {})
        .get('Parameter')[3]
        .get('Value'),
        'ypos': xrd_dict.get('Result')
        .get('ParameterList', {})
        .get('Parameter')[4]
        .get('Value'),
        'tilt': xrd_dict.get('Result')
        .get('ParameterList', {})
        .get('Parameter')[8]
        .get('Value'),
        'tilt_direction': xrd_dict.get('Result')
        .get('ParameterList', {})
        .get('Parameter')[9]
        .get('Value'),
        'component_0': xrd_dict.get('Result')
        .get('ParameterList', {})
        .get('Parameter')[12]
        .get('Value'),
        'component_90': xrd_dict.get('Result')
        .get('ParameterList', {})
        .get('Parameter')[13]
        .get('Value'),
        'reference_offset': xrd_dict.get('Result')
        .get('ParameterList', {})
        .get('Parameter')[14]
        .get('Value'),
        'reference_axis': xrd_dict.get('Result')
        .get('ParameterList', {})
        .get('Parameter')[15]
        .get('Value'),
    }
    return parameter_list


def extract_scan_data(
    xrd_dict,
):  # xrd_dict.get('MultiMeasurement',{}).get('Measurements',{}).get('Measurement')[i])
    """Extract scan data from the XRD data."""
    input_str_r = (
        xrd_dict.get('Scans')
        .get('Scan')
        .get('ScanCurves')
        .get('ScanCurve')[0]
        .get('text')
    )
    scanarray_omega_r = []
    scanarray_intensity_r = []
    [
        scanarray_omega_r.append(float(i.split(' ')[0]))
        for i in input_str_r.split(';')
        if i
    ]
    [
        scanarray_intensity_r.append(float(i.split(' ')[1]))
        for i in input_str_r.split(';')
        if i
    ]

    input_str_l = (
        xrd_dict.get('Scans')
        .get('Scan')
        .get('ScanCurves')
        .get('ScanCurve')[1]
        .get('text')
    )
    scanarray_omega_l = []
    scanarray_intensity_l = []
    [
        scanarray_omega_l.append(float(i.split(' ')[0]))
        for i in input_str_l.split(';')
        if i
    ]
    [
        scanarray_intensity_l.append(float(i.split(' ')[1]))
        for i in input_str_l.split(';')
        if i
    ]

    scan_data = {
        'scan_r': {
            'name': xrd_dict.get('Scans')
            .get('Scan')
            .get('ScanCurves')
            .get('ScanCurve')[0]
            .get('Name'),
            'omega': scanarray_omega_r,  # xrd_dict.get('Scans').get('Scan').get('ScanCurves').get('ScanCurve')[0].get('text').split(';')[0],
            'intensity': scanarray_intensity_r,
        },  # xrd_dict.get('Scans').get('Scan').get('ScanCurves').get('ScanCurve')[0].get('text').split(';')[1]},
        'scan_l': {
            'name': xrd_dict.get('Scans')
            .get('Scan')
            .get('ScanCurves')
            .get('ScanCurve')[1]
            .get('Name'),
            'omega': scanarray_omega_l,  # xrd_dict.get('Scans').get('Scan').get('ScanCurves').get('ScanCurve')[1].get('text').split(';')[0],
            'intensity': scanarray_intensity_l,
        },
    }
    # xrd_dict.get('Scans').get('Scan').get('ScanCurves').get('ScanCurve')[1].get('text').split(';')[1]}}}
    return scan_data

    # # metadata = parsed_data.get('Measurement', {}).get('Info', {})

    # # Extract metadata from 'Info' section
    # info_metadata = parsed_data.get('Measurement', {}).get('Info', {})

    # # Extract metadata from 'OmegaScanRecipe' section
    # omega_scan_recipe_metadata = parsed_data.get('Measurement', {}).get(
    #     'OmegaScanRecipe', {}
    # )

    # # Extract metadata from 'Result' section
    # result_metadata = parsed_data.get('Measurement', {}).get('Result', {})

    # metadata = {
    #     'Info': info_metadata,
    #     'OmegaScanRecipe': omega_scan_recipe_metadata,
    #     'Result': result_metadata,
    # }
    # measurements = []

    # scan_data = (
    #     parsed_data.get('Measurement', {})
    #     .get('OmegaScan', {})
    #     .get('ScanData', {})
    #     .get('DataPoints', {})
    #     .get('text', '')
    # )
    # if scan_data:
    #     for line in scan_data.split(';'):
    #         if line.strip():
    #             angle, intensity = line.split()
    #             measurements.append(
    #                 {'2Theta': float(angle), 'Intensity': int(intensity)}
    #             )

    # scans = parsed_data.get('Measurement', {}).get('Scans', {})

    # result = {'metadata': metadata, 'measurements': measurements, 'scans': scans}
    # # print(result)
    # return result
