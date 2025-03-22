import numpy as np
import cmath
import os
import matplotlib.pyplot as plot

class s_param():
     
    def __init__(self,file_path = None , num_ports = None, frequencies = None):
            
            # create class instance globals
            self.type = "Network"
            self.sub_type = "S Parameter"
            self.frequencies = []
            self.freq_max = 0
            self.freq_min = 0
            self.file_data = [[[]*1]*1]*1
            self.version = ""
            self.freq_unit = ""
            self.freq_unit = ""
            self.type = ""
            self.format = ""
            self.z_reference = 50

            #Check input argumentts and intitalize accordingly
            if num_ports is not None:
                self.num_ports = num_ports
                for i in range(self.num_ports):
                    self.file_data.append([[]])
                    for j in range(self.num_ports-1):
                        self.file_data[i].append([])          
            else:
                self.num_ports = 0

            if frequencies is not None:
                self.frequencies = frequencies
                for i in range(self.num_ports):
                    for j in range(self.num_ports): 
                        for f in range(len(frequencies)):
                            self.file_data[i][j].append(None)
                            

            if file_path is not None:
                file_path = file_path.replace("\\", "/")
                self.file_path = file_path
                self.read_snp(self.file_path)

    #dynamically calculate specified attribute, lowers memory allocation of a single network class
    def __getattr__(self, attr):
        if attr=="dbmag":
            self.dbmag = self.calc_dbmag()   #This can be a long computation
        return super(s_param, self).__getattribute__(attr)

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
                    self.z_reference = float(parts[5])

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
                            self.file_data.append([[]])
                            for j in range(self.num_ports-1):
                                self.file_data[i].append([])
                                

                        first_network_data  = False


                    # determine file type and extract data   
                    # note:.s2p file types have different sequence than all other sNp file types (y tho???)
                    if self.ext[2] == '2':
                        self.file_data[0][0].append([network_data[1], network_data[2]])
                        self.file_data[1][0].append([network_data[3], network_data[4]])
                        self.file_data[0][1].append([network_data[5], network_data[6]])
                        self.file_data[1][1].append([network_data[7], network_data[8]])

                    elif self.num_ports != 0 and self.num_ports !=2:
                        for i in range(self.num_ports):
                            for j in range(self.num_ports): 
                                self.file_data[i][j].append(network_data[i*self.num_ports*2 + 2*j+1], network_data[i*self.num_ports*2 + 2*j+2])
                        else:
                             raise ValueError("Data Format Unsupported")
                    else:
                        raise ValueError("No or unknown number of ports")
                    
                    if self.freq_unit == "GHZ":
                        self.frequencies.append(1E9*freq)
                    elif self.freq_unit == "MHZ":
                        self.frequencies.append(1E6*freq)
                    elif self.freq_unit == "KHZ":
                        self.frequencies.append(1E3*freq)
                    elif self.freq_unit == "HZ":
                        self.frequencies.append(freq)
        return

    def calc_dbmag(self):
        temp = [[[]*len(self.frequencies)]*self.num_ports]*self.num_ports
        for i in range(self.num_ports):
              for j in range(self.num_ports): 
                if self.format == "DB":  
                    temp[i][j] = ([x[0] for x in self.file_data[i][j]])
                elif self.format == "RI":  
                    temp[i][j] = ([np.sqrt(x[0]**2 + x[1]**2) for x in self.file_data[i][j]])
                elif self.format == "MA":  
                    temp[i][j] = ([20*np.log10(x[0]) for x in self.file_data[i][j]])
        return temp
    

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
                self.complex[i][j] = [x+y*1j for x,y in zip(self.real[i][j],self.imag[i][j])]

    def real_imag_2_linmag_phase(self):
        for i in range(self.num_ports):
              for j in range(self.num_ports):
                    self.linmag[i][j] = [np.sqrt(x**2 + y**2) if x!=0 and y!=0 else 1 for x,y in zip(self.real[i][j],self.imag[i][j])]
                    self.phase[i][j] = [(180/np.pi)*np.arctan(y/x) if x!=0 else 180 for x,y in zip(self.real[i][j],self.imag[i][j])]

    def complex_2_real_imag(self):
        for i in range(self.num_ports):
              for j in range(self.num_ports):
                self.real[i][j] = [np.real(x) for x in self.complex[i][j]]
                self.imag[i][j] = [np.imag(x) for x in self.complex[i][j]]
    
    def lin_mag_phase_2_complex(self):            
        for i in range(self.num_ports):
            for j in range(self.num_ports):
                self.complex[i][j] = [x+y*1j for x,y in zip(self.real[i][j],self.imag[i][j])]

def s_param_cascade(s1: s_param,s2: s_param, interp_freq_step = None):
    
    if  interp_freq_step == None:
        interp_freq_step = 10E6
    #determine frequencies that cascade can be performed
    f_min = min(s1.frequencies[0],s2.frequencies[0])
    f_max = min(s1.frequencies[(len(s1.frequencies)-1)],s2.frequencies[(len(s2.frequencies)-1)])
    freq=np.arange(start=f_min,stop=f_max+interp_freq_step,step=interp_freq_step)
    

    #initialize return matrix
    s_c = s_param(num_ports=2,frequencies=freq)
                               
    #interpolate frequency points and convert both sparametrs to ABCD parameters
    for f in range(len(s_c.frequencies)):

        #interpolate value at frequency point
        s11_1 = np.interp(s_c.frequencies[f],s1.frequencies,s1.complex[0][0])
        s12_1 = np.interp(s_c.frequencies[f],s1.frequencies,s1.complex[0][1])
        s21_1 = np.interp(s_c.frequencies[f],s1.frequencies,s1.complex[1][0])
        s22_1 = np.interp(s_c.frequencies[f],s1.frequencies,s1.complex[1][1])

        s11_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex[0][0])
        s12_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex[0][1])
        s21_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex[1][0])
        s22_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex[1][1])
        
        #convert to ABCD parametersS
        a1=(((1+s11_1)*(1-s22_1)+(s12_1*s21_1))/(2*s21_1))
        b1=(s1.z_reference*((1+s11_1)*(1+s22_1)-(s12_1*s21_1))/(2*s21_1))
        c1=((1/s1.z_reference)*((1-s11_1)*(1-s22_1)-(s12_1*s21_1))/(2*s21_1))
        d1=(((1-s11_1)*(1+s22_1)+(s12_1*s21_1))/(2*s21_1))

        a2=(((1+s11_2)*(1-s22_2)+(s12_2*s21_2))/(2*s21_2))
        b2=(s2.z_reference*((1+s11_2)*(1+s22_2)-(s12_2*s21_2))/(2*s21_2))
        c2=((1/s2.z_reference)*((1-s11_2)*(1-s22_2)-(s12_2*s21_2))/(2*s21_2))
        d2=(((1-s11_2)*(1+s22_2)+(s12_2*s21_2))/(2*s21_2))
         
        #cascade network parameters using matrix multiplication
        a_c=(a1*a2+b1*c2)
        b_c=(a1*b2+b1*d2)
        c_c=(c1*a2+d1*c2)
        d_c=(c1*b2+d1*d2)

        #convert cascaded network ABCD aprameters back to s parameters
        s_c.complex[0][0][f]=(((a_c+(b_c/s1.z_reference)-(c_c*s1.z_reference)-d_c)/(a_c+(b_c/s1.z_reference)+(c_c*s1.z_reference)+d_c)))
        s_c.complex[0][1][f]=( ((2*(a_c*d_c-b_c*c_c))/(a_c+b_c/s1.z_reference+c_c*s1.z_reference+d_c)))
        s_c.complex[1][0][f]=((2/(a_c+b_c/s1.z_reference+c_c*s1.z_reference+d_c)))
        s_c.complex[1][1][f]=(((-a_c+b_c/s1.z_reference-c_c*s1.z_reference+d_c)/(a_c+b_c/s1.z_reference+c_c*s1.z_reference+d_c)))

    #convert result to all other network forms
    s_c.complex_2_real_imag()
    s_c.real_imag_2_linmag_phase()
    s_c.lin_mag_phase_2_db_mag_phase()

    return s_c

def linear_interpolation(x1, y1, x2, y2, x):
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

def closest_value(list_of_numbers, target_value):
    return min(list_of_numbers, key=lambda x: abs(x - target_value))