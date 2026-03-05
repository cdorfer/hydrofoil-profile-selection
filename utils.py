"""
@author: cdorfer
"""
from matplotlib import pyplot as plt
plt.ion()

def generate1DPlot(xlabel='', ylabel='', title='', figsize=(8,6)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlabel(xlabel,fontsize=16)
    ax.set_ylabel(ylabel,fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.set_title(title, fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    return [fig, ax]


def dyn_viscoscity_h2o(temp_c=20, salt_water=False):
	if salt_water == True:
		return "Not implemented"

	temp_k = temp_c + 273.15
	return 1 / (0.1*temp_k**2 - 34.335*temp_k + 2472)


def kin_viscosity_h20(temp_c=20, salt_water=False):
	density_water = 1000 #kg/m^3
	return (dyn_viscoscity_h2o(temp_c=temp_c, salt_water=salt_water))/density_water


def re_number(chord_length_m, flow_speed_m_s, temp_c=20, salt_water=False):
	if salt_water == True:
		return "Not implemented"

	density_water = 1000 #kg/m^3
	dyn_vis = dyn_viscoscity_h2o(temp_c=temp_c, salt_water=salt_water)
	
	re = (density_water*flow_speed_m_s*chord_length_m) / dyn_vis
	return round(re)


