import numpy as np
import cmath
import os
import matplotlib.pyplot as plot

class snp():
     
    def __init__(self,file_path):
            # create class instance globals
            self.type = ""
            self.sub_type = ""
            self.frequencies =[]
            self.dbmag = [[[]*1]*1]*1
            self.linmag = [[[]*1]*1]*1
            self.phase = [[[]*1]*1]*1
            self.real = [[[]*1]*1]*1
            self.imag = [[[]*1]*1]*1
        
            self.version = ""
            self.freq_unit = ""
            self.freq_unit = ""
            self.type = ""
            self.format = ""
            self.z_reference = 0
            self.num_ports = 0
            self.file_path = file_path

            self.read_snp(self.file_path)




    def read_snp(self,file_path):

        self.file_name , self.ext = os.path.splitext(file_path)
        first_network_data = True

        with open(file_path, 'r') as file:
            for line in file:

                line = line.strip()
                is_data_section = False

                # Skip empty lines or comment lines
                if not line or line.startswith('!'):
                    continue
            
                # Process keywords
                if line.startswith('[Version]'):
                        self.version = line.split()[1]
                elif line.startswith('[Number of Ports]'):
                        self.num_ports = int(line.split()[1])
                elif line.startswith('[Network Data]'):
                    network_readf = True
                    multisection = True
                    continue
                elif line.startswith('[End]'):
                    break

                if line.startswith('#'):
                    parts = line.split()
                    self.freq_unit = parts[1].upper()
                    self.type = parts[2].upper()
                    self.format = parts[3].upper()
                    self.z_reference = int(parts[5])

                    


                else:
                    # Parse network data lines
                    network_data = list(map(float, line.split()))
                    freq = network_data[0]

                    #determine number of ports and set rows and columns of data accordingly base on number of data points in first row
                    if first_network_data == True:
                        numport = np.sqrt((len(network_data)-1)/2)
                        if numport % 1 != 0:
                            raise ValueError("Non integer number of ports detected")
                        
                        self.num_ports = int(numport)

                        for i in range(self.num_ports):
                            
                            self.dbmag.append([[]])
                            self.phase.append([[]])
                            self.linmag.append([[]])
                            self.imag.append([[]])
                            self.real.append([[]])

                            for j in range(self.num_ports-1):
                                self.dbmag[i].append([])
                                self.phase[i].append([])
                                self.linmag[i].append([])
                                self.phase[i].append([])
                                self.real[i].append([])
                                self.imag[i].append([])

                        first_network_data  = False


                    # determine file type and extract data   
                    # note:.s2p file types have different sequence than all other sNp file types (y tho???)
                    if self.ext[2] == '2':
                        if self.format == "DB":
                            self.dbmag[0][0].append(network_data[1]), self.phase[0][0].append(network_data[2])
                            self.dbmag[1][0].append(network_data[3]), self.phase[1][0].append(network_data[4])
                            self.dbmag[0][1].append(network_data[5]), self.phase[0][1].append(network_data[6])
                            self.dbmag[1][1].append(network_data[7]), self.phase[1][1].append(network_data[8])

                        elif self.format == "MA":
                            self.linmag[0][0].append(network_data[1]), self.phase[0][0].append(network_data[2])
                            self.linmag[1][0].append(network_data[3]), self.phase[1][0].append(network_data[4])
                            self.linmag[0][1].append(network_data[5]), self.phase[0][1].append(network_data[6])
                            self.linmag[1][1].append(network_data[7]), self.phase[1][1].append(network_data[8])

                        elif self.format == "RI":
                            self.real[0][0].append(network_data[1]), self.imag[0][0].append(network_data[2])
                            self.real[1][0].append(network_data[3]), self.imag[1][0].append(network_data[4])
                            self.real[0][1].append(network_data[5]), self.imag[0][1].append(network_data[6])
                            self.real[1][1].append(network_data[7]), self.imag[1][1].append(network_data[8])

                        else:
                             raise ValueError("Data Format Unsupported")
                        

                    elif self.num_ports != 0:
                        if self.format == "DB":
                            for i in range(self.num_ports):
                                for j in range(self.num_ports): 
                                    self.dbmag[i][j].append(network_data[i*self.num_ports*2 + 2*j+1]), self.phase[i][j].append(network_data[i*self.num_ports*2 + 2*j+2])


                        elif self.format == "MA":
                            for i in range(self.num_ports):
                                for j in range(self.num_ports): 
                                    self.linmag[i][j].append(network_data[i*self.num_ports*2 + 2*j+1]), self.phase[i][j].append(network_data[i*self.num_ports*2 + 2*j+2])

                        elif self.format == "RI":
                            for i in range(self.num_ports):
                                for j in range(self.num_ports): 
                                    self.real[i][j].append(network_data[i*self.num_ports*2 + 2*j+1]), self.imag[i][j].append(network_data[i*self.num_ports*2 + 2*j+2])

                        else:
                             raise ValueError("Data Format Unsupported")
                    else:
                        raise ValueError("No or unknown number of ports")
                    
                    self.frequencies.append(freq)

        #calculate all other parameters for easier data use
        if self.format =='DB':
            self.db_mag_phase_2_lin_mag_phase()
            self.lin_mag_phase_2_real_imag() 

        if self.format =='MA':
            self.lin_mag_phase_2_db_mag_phase() 
            self.lin_mag_phase_2_real_imag() 

        if self.format =='RI':
            self.lin_mag_phase_2_db_mag_phase()
            self.lin_mag_phase_2_real_imag() 
        return



    #Functions for calculating and populating different forms or s parameter representations
    def db_mag_phase_2_lin_mag_phase(self):
         for i in range(self.num_ports):
              for j in range(self.num_ports):   
                self.linmag[i][j]=[10**(float(x)/20) for x in self.dbmag[i][j]]

    def lin_mag_phase_2_db_mag_phase(self):
         for i in range(self.num_ports):
              for j in range(self.num_ports):   
                self.dbmag[i][j]=[20*np.log10(float(x)) for x in self.linmag[i][j]]

    def lin_mag_phase_2_real_imag(self):
         for i in range(self.num_ports):
              for j in range(self.num_ports):
                self.real[i][j] = [np.cos(float(x) * (np.pi/180)) for x in self.phase[i][j]]
                self.real[i][j] = [x * y for x, y in zip(self.real[i][j],self.linmag[i][j])]
                self.imag[i][j] = [np.sin(float(x) * (np.pi/180)) for x in self.phase[i][j]]
                self.imag[i][j] = [x * y for x, y in zip(self.imag[i][j],self.linmag[i][j])]
