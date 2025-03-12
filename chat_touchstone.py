import re

def parse_touchstone(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    metadata = {}
    network_data = []
    is_data_section = False
    num_ports = 0
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines or comment lines
        if not line or line.startswith('!'):
            continue
        
        # Process keywords
        if line.startswith('[Version]'):
            metadata['Version'] = line.split()[1]
        elif line.startswith('[Number of Ports]'):
            num_ports = int(line.split()[1])
            metadata['Number of Ports'] = num_ports
        elif line.startswith('[Network Data]'):
            is_data_section = True
            continue
        elif line.startswith('[End]'):
            break
        
        # Process the network data section
        if is_data_section:
            # Split the line into frequency and parameters
            data = re.split(r'\s+', line)
            frequency = float(data[0])
            parameters = list(map(float, data[1:]))
            
            # Ensure that the number of parameters corresponds to the number of ports
            if len(parameters) != num_ports ** 2:
                raise ValueError(f"Mismatch in data length for {num_ports}-port network at frequency {frequency} Hz")
            
            # Store the data
            network_data.append({'Frequency': frequency, 'Parameters': parameters})
    
    return metadata, network_data

# Example usage:
filename = "C:/Users/Miles/Downloads/Infineon-RFTransistor-SPAR/SPAR/BFP840FESD/BFP840FESD_VCE_1.8V_IC_26mA.s2p"
metadata, network_data = parse_touchstone(filename)

print("Metadata:", metadata)
print("Network Data:")
for entry in network_data:
    print(entry)