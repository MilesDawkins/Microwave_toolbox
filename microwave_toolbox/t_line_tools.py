import numpy as np
import cmath as cm
from . import system_tools

class microstrip():
    def __init__(self,zo,er,sub_t,length,freqs_in = None, shunt_in = None, typem = None, zl_in = None, length_unit = None, center_freq = None):
        # create class instance globals

        self.zl = np.inf

        if typem is None:
            self.typem = "t_line"
        else:
            self.typem = typem
            if self.typem == "open":
                self.zl = np.inf
            elif self.typem == "short":
                self.zl = 0

        if zl_in is not None:
            self.zl = zl_in   
            self.typem = "loaded"  
        
        self.sub_type = "microstrip"
        self.zo=zo
        self.er=er
        self.ereff = 0
        self.sub_t=sub_t
        self.length = length
        
       
        
        # calculate initial microstrip parameters
        self.microstrip_calc(self.zo,self.er,self.sub_t)
        if  length_unit != None:
            if length_unit == "meters":
                self.length = length
            if length_unit == "lambda":
                self.length = length * self.vp_line/center_freq

        if freqs_in is not None:
            if shunt_in is not  None:
                self.create_network(freqs_in,self.length,shunt = shunt_in)
            else:
                self.create_network(freqs_in,self.length,shunt = False)

    def microstrip_calc(self,zo_in,er,sub_t):

        # calculate a and b for microstrip equations
        a=(zo_in/60)*np.sqrt((er+1)/2)+((er-1)/(er+1))*(0.23+(0.11/er))
        b=(377*np.pi)/(2*zo_in*np.sqrt(er))
        # calculate the 2 equations for stripwidth/thickness
        wsd1=(8*np.exp(a)/(np.exp(2*a)-2))
        wsd2=(2/np.pi)*(b-1-np.log(2*b-1)+((er-1)/(2*er))*(np.log(b-1)+0.39-(0.61/er)))
        
        # determine valid equation and strip width
        if(wsd1<2):
            self.width=sub_t*wsd1
            wsdf=wsd1

        elif(wsd1>=2):
            self.width=sub_t*wsd2
            wsdf=wsd2
        
        # calculate effective permitivity
        self.ereff=((er+1)/2)+(((er-1)/2)*(1/np.sqrt(1+12*(sub_t/self.width))))

        # check if zo is correct
        if(wsdf<1):
            self.zo_calc=(60/np.sqrt(self.ereff))*np.log(((8*sub_t)/self.width)+(self.width/(4*sub_t)))
        elif(wsdf>=1):
            self.zo_calc=((120*np.pi)/(np.sqrt(self.ereff)*((self.width/sub_t)+1.393+0.667*np.log((self.width/sub_t)+1.444))))
        
        # calculate parameters of waves on line
        self.vp_line=299792458/np.sqrt(self.ereff)

    def create_network(self,freqs,length, shunt):
        self.length = length
        if self.typem == "t_line":
            self.network = system_tools.network(num_ports=2,frequencies=freqs,format='ABCD')
        elif shunt:
            self.network = system_tools.network(num_ports=2,frequencies=freqs,format='ABCD')
        else:
            self.network = system_tools.network(num_ports=1,frequencies=freqs,format='MA')
        
        
        lambda_freq = self.vp_line/freqs
        beta_freq = (2*np.pi)/lambda_freq

        if self.typem == "t_line":

            #A
            a = np.cos(beta_freq * length)
            self.network.file_data[0][0]=a
            #B
            b = 1j*self.zo*np.sin(beta_freq * length)
            self.network.file_data[0][1]=b
            #C
            c = 1j*(1/self.zo)*np.sin(beta_freq * length)
            self.network.file_data[1][0]=c
            #D
            d = np.cos(beta_freq * length)
            self.network.file_data[1][1]=d

        elif shunt:
            #reference for this eq: https://my.eng.utah.edu/~cfurse/ece5320/lecture/L9b/A%20Review%20of%20ABCD%20Parameters.pdf
            adm = (1/(self.input_z(freqs,self.length,self.zl)))
            
            #A
            self.network.file_data[0][0]=np.ones(len(adm))
            #B
            self.network.file_data[0][1]=np.zeros(len(adm))
            #C
            self.network.file_data[1][0]=adm
            #D
            self.network.file_data[1][1]=np.ones(len(adm))
            
            
        else: 
            gamma_in = (self.input_z(freqs,self.length,self.zl)-50)/(self.input_z(freqs,self.length,self.zl)+50)
            #s11
            self.network.file_data=np.abs(gamma_in) + 1j*((180/np.pi)*np.angle(gamma_in))
               

    def wavelength(self,frequency):
        self.lambda_line = self.vp_line/frequency
        return self.lambda_line 
    
    def input_z(self,frequency,length,zl):
        lambda_line = self.vp_line/frequency
        
        if(((type(zl) == int) or (type(zl) == float))  and (zl == 0)):
            self.z_in = 1j*self.zo*np.tan(((2*np.pi)/lambda_line)*length)
        elif(((type(zl) == int) or (type(zl) == float))  and (zl == np.inf)):
            self.z_in = -1*1j*self.zo*1/(np.tan(((2*np.pi)/lambda_line)*length))
            
        else:
            self.z_in = self.zo*((zl+1j*self.zo*np.tan(((2*np.pi)/lambda_line)*length))/(self.zo+1j*zl*np.tan(((2*np.pi)/lambda_line)*length)))

        return self.z_in 
