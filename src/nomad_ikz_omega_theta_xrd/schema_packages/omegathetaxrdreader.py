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

    # metadata = parsed_data.get('Measurement', {}).get('Info', {})

    # Extract metadata from 'Info' section
    info_metadata = parsed_data.get('Measurement', {}).get('Info', {})

    # Extract metadata from 'OmegaScanRecipe' section
    omega_scan_recipe_metadata = parsed_data.get('Measurement', {}).get(
        'OmegaScanRecipe', {}
    )

    # Extract metadata from 'Result' section
    result_metadata = parsed_data.get('Measurement', {}).get('Result', {})

    metadata = {
        'Info': info_metadata,
        'OmegaScanRecipe': omega_scan_recipe_metadata,
        'Result': result_metadata,
    }
    measurements = []

    scan_data = (
        parsed_data.get('Measurement', {})
        .get('OmegaScan', {})
        .get('ScanData', {})
        .get('DataPoints', {})
        .get('text', '')
    )
    if scan_data:
        for line in scan_data.split(';'):
            if line.strip():
                angle, intensity = line.split()
                measurements.append(
                    {'2Theta': float(angle), 'Intensity': int(intensity)}
                )

    scans = parsed_data.get('Measurement', {}).get('Scans', {})

    result = {'metadata': metadata, 'measurements': measurements, 'scans': scans}
    # print(result)
    return result
