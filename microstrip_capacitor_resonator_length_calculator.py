import numpy as np
import matplotlib.pyplot as mat

#calculates the microstrip length required to make a resonator with a given capacitance and f_o

#input variables
zo_in = 50
er=4.4
sub_t = 1.6
f_0=3.409E9
capacitance = 40E-12

def microstrip_calc(zo_in,er,sub_t,frequency):

    # calculate a and b for microstrip equations
    a=(zo_in/60)*np.sqrt((er+1)/2)+((er-1)/(er+1))*(0.23+(0.11/er))
    b=(377*np.pi)/(2*zo_in*np.sqrt(er))

    # calculate the 2 equations for stripwidth/thickness
    wsd1=(8*np.exp(a)/(np.exp(2*a)-2))
    wsd2=(2/np.pi)*(b-1-np.log(2*b-1)+((er-1)/(2*er))*(np.log(b-1)+0.39-(0.61/er)))

    # determine valid equation and strip width
    if(wsd1<2):
        ws=sub_t*wsd1
        wsdf=wsd1
    elif(wsd2>=2):
        ws=sub_t*wsd2
        wsdf=wsd2
    
    # calculate effective permitivity
    ereff=((er+1)/2)+(((er-1)/2)*(1/np.sqrt(1+12*(sub_t/ws))))

    # check if zo is correct
    if(wsdf<1):
        zo_calc=(60/np.sqrt(ereff))*np.log(((8*sub_t)/ws)+(ws/(4*sub_t)))
    elif(wsdf>=1):
        zo_calc=((120*np.pi)/(np.sqrt(ereff)*((ws/sub_t)+1.393+0.667*np.log((ws/sub_t)+1.444))))
    
    # calculate parameters of waves on line
    vp_line=3E8/np.sqrt(ereff)
    lambda_line=vp_line/frequency
    out = [ws,ereff,vp_line,lambda_line,zo_calc]
    return out

#calcualte the inductance required for resonance at f_0
l=((1/(2*np.pi*f_0))**2)/capacitance

#calculate inductor input impedance using calcualte inductance
z_l=(1j*l*2*np.pi*f_0)

#calculate microstrip properties
ustrip=microstrip_calc(zo_in,er,sub_t,f_0)

#calculate beta on the ustrip
beta = (2*np.pi)/ustrip[3]

#calculate resonator length
reso_length = np.arctan(z_l/(1j*ustrip[4]))/beta

print(reso_length+ustrip[3]/2)