import plotly.graph_objects as go
import microwave_toolbox as mt


# Sample data (normalized impedance)
file = r"C:\Users\miles\Downloads\BFP840FESD_VCE_2.0V_IC_22mA.s2p"
file = file.replace("\\", "/")
trans_s2p = mt.network.s_param(file_path=file)

# Create the scatter smith trace
trace = go.Scattersmith(real=trans_s2p.real[0][0], imag=trans_s2p.imag[0][0])

# Define the layout
layout = go.Layout(title='Smith Chart', width=600, height=600)

# Create the figure and plot it
fig = go.Figure(data=[trace], layout=layout)
fig.show()