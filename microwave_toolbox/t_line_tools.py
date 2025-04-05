import numpy as np
from . import system_tools

class microstrip():
    def __init__(self,zo,er,sub_t):
        # create class instance globals
        self.type = "t_line"
        self.sub_type = "microstrip"
        self.zo=zo
        self.zl = np.inf
        self.er=er
        self.ereff = 0
        self.sub_t=sub_t
        self.length = 0
        self.z_in = np.inf
        self.network = system_tools.network(num_ports = 2)
        # calculate initial microstrip parameters
        self.microstrip_calc(self.zo,self.er,self.sub_t)
        

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
        elif(wsd2>=2):
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

    def wavelength(self,frequency):
        self.lambda_line = self.vp_line/frequency
        return self.lambda_line 
    
    def input_z(self,frequency,length,zl):
        self.lambda_line = self.vp_line/frequency
        self.length = length
        self.zl = zl
        if(zl == 0):
            self.type = "shorted stub"
            self.z_in = 1j*self.zo*np.tan(((2*np.pi)/self.lambda_line)*length)
        elif(zl == np.inf):
            self.type = "open stub"
            self.z_in = -1*1j*self.zo*1/(np.tan(((2*np.pi)/self.lambda_line)*length))
        else:
            self.z_in = self.zo*((zl+1j*self.zo*np.tan(((2*np.pi)/self.lambda_line)*length))/(self.zo+1j*zl*np.tan(((2*np.pi)/self.lambda_line)*length)))

        return self.z_in 
