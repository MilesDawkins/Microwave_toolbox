import numpy as np
import cmath
import os
import matplotlib.pyplot as plot
from . import s_parameter_reader as sp


def s_param_cascade(s1: sp.snp,s2: sp.snp):
    a1,b1,c1,d1,a2,b2,c2,d2,a_c,b_c,c_c,d_c = [],[],[],[],[],[],[],[],[],[],[],[]

    #initialize return matrix
    s_c = [[[]*1]*1]*1
    for i in range(2):                    
        s_c.append([[]])
        for j in range(1):
            s_c[i].append([])
                               
    #convert both sparametrs to ABCD parameters
    for f in range(len(s1.frequencies)):
        a1.append(((1+s1.complex[0][0][f])*(1-s1.complex[1][1][f])+(s1.complex[0][1][f]*s1.complex[1][0][f]))/(2*s1.complex[1][0][f]))

        b1.append(s1.z_reference*((1+s1.complex[0][0][f])*(1+s1.complex[1][1][f])-(s1.complex[0][1][f]*s1.complex[1][0][f]))/(2*s1.complex[1][0][f]))
        c1.append((1/s1.z_reference)*((1-s1.complex[0][0][f])*(1-s1.complex[1][1][f])-(s1.complex[0][1][f]*s1.complex[1][0][f]))/(2*s1.complex[1][0][f]))
        d1.append(((1-s1.complex[0][0][f])*(1+s1.complex[1][1][f])+(s1.complex[0][1][f]*s1.complex[1][0][f]))/(2*s1.complex[1][0][f]))

        a2.append(((1+s2.complex[0][0][f])*(1-s2.complex[1][1][f])+(s2.complex[0][1][f]*s2.complex[1][0][f]))/(2*s2.complex[1][0][f]))
        b2.append(s2.z_reference*((1+s2.complex[0][0][f])*(1+s2.complex[1][1][f])-(s2.complex[0][1][f]*s2.complex[1][0][f]))/(2*s2.complex[1][0][f]))
        c2.append((1/s2.z_reference)*((1-s2.complex[0][0][f])*(1-s2.complex[1][1][f])-(s2.complex[0][1][f]*s2.complex[1][0][f]))/(2*s2.complex[1][0][f]))
        d2.append(((1-s2.complex[0][0][f])*(1+s2.complex[1][1][f])+(s2.complex[0][1][f]*s2.complex[1][0][f]))/(2*s2.complex[1][0][f]))
    
    #cascade network parameters using matrix multiplication
    for f in range(len(s1.frequencies)):
        a_c.append(a1[f]*a2[f]+b1[f]*c2[f])
        b_c.append(a1[f]*b2[f]+b1[f]*d2[f])
        c_c.append(c1[f]*a2[f]+d1[f]*c2[f])
        d_c.append(c1[f]*b2[f]+d1[f]*d2[f])

    #convert cascaded network ABCD aprameters back to s parameters
    for f in range(len(s1.frequencies)):
        s_c[0][0].append(((a_c[f]+(b_c[f]/s1.z_reference)-(c_c[f]*s1.z_reference)-d_c[f])/(a_c[f]+(b_c[f]/s1.z_reference)+(c_c[f]*s1.z_reference)+d_c[f])))
        s_c[0][1].append( ((2*(a_c[f]*d_c[f]-b_c[f]*c_c[f]))/(a_c[f]+b_c[f]/s1.z_reference+c_c[f]*s1.z_reference+d_c[f])))
        s_c[1][0].append((2/(a_c[f]+b_c[f]/s1.z_reference+c_c[f]*s1.z_reference+d_c[f])))
        s_c[1][1].append(((-a_c[f]+b_c[f]/s1.z_reference-c_c[f]*s1.z_reference+d_c[f])/(a_c[f]+b_c[f]/s1.z_reference+c_c[f]*s1.z_reference+d_c[f])))

    return s_c
