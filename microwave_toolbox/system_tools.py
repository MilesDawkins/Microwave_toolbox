import numpy as np
import cmath
import os
import matplotlib.pyplot as plot

class network():
     
    def __init__(self,file_path = None , num_ports = None, frequencies = None, s_user = None, format = None, zl_in = None):
            
            # create class instance globals
            self.type = "Network"
            self.sub_type = "S Parameter"
            self.frequencies = []
            self.freq_max = 0
            self.freq_min = 0
            self.file_data = []
            self.version = ""
            self.freq_unit = ""
            self.format = ""
            self.z_reference = 50
            self.reversed = False

            #Check input argumentts and intitalize accordingly
            if format is not None:
                self.format = format

            if num_ports is not None:
                self.num_ports = num_ports
                if num_ports != 1:
                    for i in range(self.num_ports):
                        self.file_data.append([[None,None]])
                        for j in range(self.num_ports-1):
                            self.file_data[i].append([None,None])
                else:
                    self.file_data = None
                    self.file_data = [[None,None]]                  
            else:
                self.num_ports = 0


            if frequencies is not None:
                self.frequencies = frequencies
                if num_ports != 1:
                    for i in range(self.num_ports):
                        for j in range(self.num_ports): 
                            for f in range(len(frequencies)):
                                if f == 0:
                                    if s_user is not None:
                                        self.file_data[i][j]=s_user[i][j][0]
                                    else:
                                       
                                        self.file_data[i][j]=[[None,None]]
                                        
                                else:
                                    if s_user is not None:
                                        self.file_data[i][j].append(s_user[i][j][f])
                                    else:
                                        self.file_data[i][j].append([None,None])

                else:
                    for f in range(len(frequencies)):
                        if f == 0:
                            if s_user is not None:
                                self.file_data[0]=[s_user[f]]
                            else:
                                self.file_data[0]=[None,None]
                        else:
                            if s_user is not None:
                                self.file_data.append(s_user[f])
                            else:
                                self.file_data.append([None,None])
                            
            
            if file_path is not None:
                file_path = file_path.replace("\\", "/")
                self.file_path = file_path
                self.read_snp(self.file_path)

    #dynamically calculate specified attribute, lowers memory allocation of a single network class
    def __getattr__(self, attr):
        if attr=="network_data":
            self.network_data = np.array(self.file_data)
        if attr=="dbmag":
            self.dbmag = self.calc_dbmag()
        if attr=="linmag":
            self.linmag = self.calc_linmag()
        if attr=="phase":
            self.phase = self.calc_phase()
        if attr=="complex":
            self.complex = self.calc_complex()
        if attr=="impedance":
            self.impedance = self.calc_input_impedance()
        if attr=="abcd":
            self.abcd = self.calc_abcd()
        return super(network, self).__getattribute__(attr)

    def read_snp(self,file_path):

        self.file_name , self.ext = os.path.splitext(file_path)
        first_file_line = True

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
                    file_line = list(map(float, line.split()))
                    freq = file_line[0]

                    #determine number of ports and set rows and columns of data accordingly base on number of data points in first row
                    if first_file_line == True:
                        numport = np.sqrt((len(file_line)-1)/2)
                        if numport % 1 != 0:
                            raise ValueError("Non integer number of ports detected")
                        
                        self.num_ports = int(numport)

                        for i in range(self.num_ports):
                            self.file_data.append([[]])
                            for j in range(self.num_ports-1):
                                self.file_data[i].append([])
                                

                        first_file_line  = False


                    # determine file type and extract data   
                    # note:.s2p file types have different sequence than all other sNp file types (y tho???)
                    #this exploits the complex datas type to store 2 variables for fast computation later on
                    if self.ext[2] == '2':
                        self.file_data[0][0].append(file_line[1]+1j*file_line[2])
                        self.file_data[1][0].append(file_line[3]+1J*file_line[4])
                        self.file_data[0][1].append(file_line[5]+1J*file_line[6])
                        self.file_data[1][1].append(file_line[7]+1J*file_line[8])

                    elif self.num_ports != 0 and self.num_ports !=2:
                        for i in range(self.num_ports):
                            for j in range(self.num_ports): 
                                self.file_data[i][j].append(file_line[i*self.num_ports*2 + 2*j+1]+1J*file_line[i*self.num_ports*2 + 2*j+2])
                    else:
                        raise ValueError("Data Format Unsupported")

                    if self.freq_unit == "GHZ":
                        self.frequencies.append(1E9*freq)
                    elif self.freq_unit == "MHZ":
                        self.frequencies.append(1E6*freq)
                    elif self.freq_unit == "KHZ":
                        self.frequencies.append(1E3*freq)
                    elif self.freq_unit == "HZ":
                        self.frequencies.append(freq)

        #convert to np.array
        self.network_data = np.array(self.file_data)

        return

    def calc_dbmag(self):

        temp = np.empty((self.num_ports,self.num_ports,len(self.frequencies)))

        if self.num_ports != 1:
            if self.format == "DB":  
                temp = np.real(self.network_data)
            elif self.format == "RI":  
                temp = 20*np.log10(np.abs(self.network_data))
            elif self.format == "MA":  
                temp=20*np.log10(np.real(self.network_data))
                
            elif self.format == "ABCD":
                temp=20*np.log10(np.abs(self.complex))
        return temp
    
    def calc_linmag(self):

        temp = np.empty((self.num_ports,self.num_ports,len(self.frequencies)))

        if self.format == "DB":  
            temp=10**(np.real(self.network_data)/20)
        elif self.format == "RI":  
            temp = np.abs(self.network_data)
        elif self.format == "MA":  
            temp = np.real(self.network_data)
        elif self.format == "ABCD":
            temp = np.abs(self.complex)

        return temp
    
    def calc_phase(self):
 
        temp = np.empty((self.num_ports,self.num_ports,len(self.frequencies)))

        if self.format == "DB":  
            temp = np.real(self.network_data)
        elif self.format == "RI":  
            temp=np.angle(self.file_data)
        elif self.format == "MA":   
            temp = np.imag(self.network_data)
        elif self.format == "ABCD":
            temp = np.angle(self.complex)

        return temp
    
    def calc_complex(self):
        temp = np.empty((self.num_ports,self.num_ports,len(self.frequencies)))
        
        if self.format != "ABCD":
            if self.format == "DB":  
                temp = (10**(np.real(self.network_data)/20))*np.cos(np.imag(self.network_data) * (np.pi/180)) + 1j*((10**(np.real(self.network_data)/20))*np.sin(np.imag(self.network_data) * (np.pi/180)))
            elif self.format == "RI":  
                temp = self.network_data
            elif self.format == "MA": 
                temp = ((np.real(self.network_data)*np.cos(np.imag(self.network_data) * (np.pi/180))) + 1j*(np.real(self.network_data)*np.sin(np.imag(self.network_data) * (np.pi/180)))) 
        else:
            temp = self.abcd_to_complex_s()

        return temp
    
    def calc_input_impedance(self):
        temp = np.empty((self.num_ports,self.num_ports,len(self.frequencies)))

        temp = self.z_reference*((1+self.complex)/(1-self.complex)) 

        return temp
    
    def calc_abcd(self):
        #currently relies on complex data being available
        temp = np.empty((self.num_ports,self.num_ports,len(self.frequencies)))
        if self.num_ports != 1:

            if self.format != "ABCD":
                temp[0,0]=(((1+self.complex[0,0])*(1-self.complex[1,1])+(self.complex[0,1]*self.complex[1,0]))/(2*self.complex[1,0]))
                temp[0,1]=(self.z_reference*((1+self.complex[0,0])*(1+self.complex[1,1])-(self.complex[0,1]*self.complex[1,0]))/(2*self.complex[1,0]))
                temp[1,0]=((1/self.z_reference)*((1-self.complex[0,0])*(1-self.complex[1,1])-(self.complex[0,1]*self.complex[1,0]))/(2*self.complex[1,0]))
                temp[1,1]=(((1-self.complex[0,0])*(1+self.complex[1,1])+(self.complex[0,1]*self.complex[1,0]))/(2*self.complex[1,0]))
            else:
                
                temp[0,0]=self.network_data[0,0]
                temp[0,1]=self.network_data[0,1]
                temp[1,0]=self.network_data[1,0]
                temp[1,1]=self.network_data[1,1]

        else:
            SyntaxError("Cannot compute ABCD for 1 port networks, consider changing to shunt element")
        
        return temp
    
    def abcd_to_complex_s(self): 

        temp = np.empty((2,2,len(self.frequencies)))
       
        a = self.abcd[0,0]
        b = self.abcd[0,1]
        c = self.abcd[1,0]
        d = self.abcd[1,1]

        temp[0,0] = ((a+(b/self.z_reference)-(c*self.z_reference)-d)/((a+b/self.z_reference)+(c*self.z_reference)+d))
        temp[0,1] = ((2*(a*d-b*c))/((a+b/self.z_reference)+(c*self.z_reference)+d))
        temp[1,0] = ((2)/((a+b/self.z_reference)+(c*self.z_reference)+d))
        temp[1,1] = ((-1*a+(b/self.z_reference)-c*self.z_reference+d)/((a+b/self.z_reference)+(c*self.z_reference)+d))
            
        return temp
    
    def __pow__(self, other):
        return network_cascade(self,other)

def reverse_network(s1: network):
   temp1 =  s1.file_data[0][0]
   temp2 = s1.file_data[1][0]
   s1.file_data[0][0] = [x for x in s1.file_data[1][1]]
   s1.file_data[1][1] = [x for x in temp1]
   s1.file_data[1][0] = [x for x in s1.file_data[0][1]]
   s1.file_data[0][1] = [x for x in temp2]
   s1.reversed = True

def gamma_2_impedance(z_ref,g_in):
    out = z_ref*((1+g_in)/(1-g_in))
    return out

def network_cascade(s1: network,s2: network, interp_freq_step = None):
    if s1.num_ports == 1:
        SyntaxError("Cannot series cascade a 1 port onto another network, reverse order of inputs or check input network parameters")

    if  interp_freq_step == None:
        interp_freq_step = 10E6
    #determine frequencies that cascade can be performed
    f_min = max(min(s1.frequencies),min(s2.frequencies))
    f_max = min(s1.frequencies[(len(s1.frequencies)-1)],s2.frequencies[(len(s2.frequencies)-1)])
    freq=np.arange(start=f_min,stop=f_max+interp_freq_step,step=interp_freq_step)
    

    #initialize return matrix
    if s2.num_ports == 1:
        s_c = network(num_ports=1,frequencies=freq)
    else:
        s_c = network(num_ports=2,frequencies=freq)
                               
    #interpolate frequency points and convert both sparametrs to ABCD parameters
    for f in range(len(s_c.frequencies)):
        s_c.format = "RI"

        #interpolate value at frequency point
        s11_1 = np.interp(s_c.frequencies[f],s1.frequencies,s1.complex[0,0])
        s12_1 = np.interp(s_c.frequencies[f],s1.frequencies,s1.complex[0,1])
        s21_1 = np.interp(s_c.frequencies[f],s1.frequencies,s1.complex[1,0])
        s22_1 = np.interp(s_c.frequencies[f],s1.frequencies,s1.complex[1,1])
           
        if s2.num_ports == 1:
            
            s11_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex)
            temp = s11_1 + ((s21_1*s12_1*s11_2)/(1-s22_1*s11_2))
            s_c.file_data[f]=[np.real(temp), np.imag(temp)]
            
        if s2.num_ports == 2:
            
            #interpolate value at frequency point
            s11_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex[0,0])
            s12_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex[0,1])
            s21_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex[1,0])
            s22_2 = np.interp(s_c.frequencies[f],s2.frequencies,s2.complex[1,1])
            
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
            temp = (((a_c+(b_c/s1.z_reference)-(c_c*s1.z_reference)-d_c)/(a_c+(b_c/s1.z_reference)+(c_c*s1.z_reference)+d_c)))
            s_c.file_data[0][0][f]=[np.real(temp) + 1J*np.imag(temp)]
            temp = (((2*(a_c*d_c-b_c*c_c))/(a_c+b_c/s1.z_reference+c_c*s1.z_reference+d_c)))
            s_c.file_data[0][1][f]=[np.real(temp) + 1J*np.imag(temp)]
            temp = ((2/(a_c+b_c/s1.z_reference+c_c*s1.z_reference+d_c)))
            s_c.file_data[1][0][f]=[np.real(temp) + 1J*np.imag(temp)]
            temp = (((-a_c+b_c/s1.z_reference-c_c*s1.z_reference+d_c)/(a_c+b_c/s1.z_reference+c_c*s1.z_reference+d_c)))
            s_c.file_data[1][1][f]=[np.real(temp) + 1j*np.imag(temp)]


    return s_c

def linear_interpolation(x1, y1, x2, y2, x):
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

def closest_value(list_of_numbers, target_value):
    return min(list_of_numbers, key=lambda x: abs(x - target_value))