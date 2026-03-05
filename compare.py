import pickle
import viiflowtools.vf_tools as vft
import numpy as np
from scipy import interpolate
from adjustText import adjust_text
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from utils import generate1DPlot
plt.ion()
plt.style.use('dark_background')


#open file previously generated with airfoil_search.py
res = pickle.load(open("results.pkl", "rb"))

#do some cuts on the selected airfols
airfoils0 = []
fails = []
for key, value in res.items():
	try:
		#print(f"Foil: {key}")
		cd = np.array(value["CD"])

		if len(cd)==0:
			continue
		#else:
		airfoils0.append(key)


	except Exception as e:
		print(e)
		fails.append([key, e])
		pass

print(f"Simulation fails: {len(fails)}")


airfoils1 = []
for i, key in enumerate(airfoils0):
	cd = np.array(res[key]["CD"])
	aoa = np.array(res[key]["AOA"])

	#average drag between -1 and 1 degree AOA for more reliability
	indices = np.where((aoa >= -1) & (aoa <= 1.000001))
	avg_cd = np.mean(np.take(cd, indices))
	airfoils1.append([key, avg_cd])


#sort smallest cd to largest
airfoils1.sort(key=lambda row: (row[1]), reverse=False)
worst_cd = airfoils1[-1][1]
best_cd = airfoils1[0][1]
diff = 100*(worst_cd/best_cd)
print(f"Ratio worst/best Cd: {diff}")

nfoils = len(airfoils1)
jet = plt.get_cmap('jet') 
cNorm = colors.Normalize(vmin=0, vmax=nfoils)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet) 


#plot drag (c_d) over angle of attack (AOA) for all profiles
fig,ax = generate1DPlot(xlabel="AOA [$^\circ$]", ylabel="C$_D$ [ ]", title='', figsize=(12,8))

i = 0
for key, avg_cd in airfoils1:
	colorVal = scalarMap.to_rgba(i)
	i += 1
	cd = np.array(res[key]["CD"])
	aoa = np.array(res[key]["AOA"])
	ax.plot(aoa, cd, color=colorVal, label=f"{key.split('/')[1]}")
	ax.plot(0, avg_cd, marker='o', color=colorVal, markerfacecolor='white')

handles,labels = ax.get_legend_handles_labels()
leg = ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5), title='', fontsize=9.4, ncol=4)
plt.grid(True, lw=0.5, color='grey')
plt.xlim([-2, 2])
plt.show()
plt.savefig('cd_vs_aoa.png', bbox_inches='tight', dpi=300)




#plot second moment of area vs drag
fig2,ax2 = generate1DPlot(xlabel="Drag Coefficient C$_D$ [ ]", ylabel="~Iy [a.u.] Second Moment of Area Perpendicular to Direction of Travel", figsize=(28,14))

airfoils2 = []
texts = []
#calculate second moment of area for each airfoil
for key, avg_cd in airfoils1:
	fname = f"{key}.dat"
	coord = vft.read_selig(fname)
	x = coord[0]
	y = coord[1]

	#we only need to look at 1/2 of the profile
	indices = np.where(y >= 0)
	x = np.take(x, indices)[0]
	y = np.take(y, indices)[0]
 
	#filter to only airfoils that can have a 14mm thickness at a 125mm chord:
	#if max(y) > 7.2/125:
	# 	continue
 
 
	if x[-1] == 1:
		x = np.delete(x, -1)
		y = np.delete(y, -1)

	if x[-1] != 0:
		x = np.append(x, 0)
		y = np.append(y, 0)

	yvals = interpolate.interp1d(x,y, kind='cubic')
	xvals = np.arange(0,1,0.002)
	Iy = 2*np.sum([yvals(x)**2*0.002 for x in xvals])
 
	y_interp = yvals(xvals)
	Ix = 2 * np.trapz(xvals**2 * y_interp, xvals)

	airfoils2.append([key, Iy, Ix, avg_cd, xvals, yvals])
	texts.append(plt.text(avg_cd, Iy, f"{key.split('/')[1]}\nIy:{1000*Iy:.2f} Ix:{1000*Ix:.2f}\ncd:{avg_cd:.4f}"))
	#ax2.plot(avg_cd, Iy, 'ro', color=Ix)

cd = [e[3] for e in airfoils2]
iy = [e[1] for e in airfoils2]
ix = [e[2] for e in airfoils2]

sc = ax2.scatter(cd, iy, c=ix, cmap='jet', s=50)
cbar = plt.colorbar(sc, ax=ax2)
cbar.set_label("~Ix [a.u.] (Second Moment of Area in Direction of Travel)")

plt.grid(True, lw=0.5, color='grey')
adjust_text(texts, only_move={'points':'y', 'texts':'y'}, arrowprops=dict(arrowstyle="->", color='white', lw=0.5))
fig2.show()
plt.savefig('cd_vs_I.png', bbox_inches='tight', dpi=300)



#plot profiles curves and color them according to their drag
airfoils2.sort(key=lambda row: (row[3]), reverse=True)
print('best/worst cd: ', best_cd, worst_cd)
cNorm = colors.Normalize(vmin=best_cd, vmax=worst_cd)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet) 
fig3,ax3 = generate1DPlot(xlabel="X [ ]", ylabel="Y [ ]", title='Drag for Different Geometries (worst (red) to best (blue))', figsize=(24,12))

i = 0
for key, Iy, Ix, avg_cd, xvals, yvals in airfoils2:
	i += 1
	#skip every second profile otherwise plot gets too crowded
	if(i%2 == 0):
		continue	
	
	colorVal = scalarMap.to_rgba(avg_cd)
	ax3.plot(xvals, yvals(xvals), color=colorVal)
	ax3.plot(xvals, -1*yvals(xvals), color=colorVal)


plt.grid(True, lw=0.5, color='grey')
fig3.show()
plt.savefig('cd_for_profiles.png', bbox_inches='tight', dpi=300)



#plot profiles curves and color them according to their second moment of area perpendicular to the direction of travel
airfoils2.sort(key=lambda row: (row[1]), reverse=False)
iys = [e[1] for e in airfoils2]
cNorm = colors.Normalize(vmin=min(iys), vmax=max(iys))
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet) 
fig3,ax3 = generate1DPlot(xlabel="X [ ]", ylabel="Y [ ]", title='Iy Different Airfoils (lowest (blue) to highest (red))', figsize=(24,12))

i = 0
for key, Iy, Ix, avg_cd, xvals, yvals in airfoils2:
	i += 1
	#skip every second profile otherwise plot gets too crowded
	if(i%2 == 0):
		continue	
	
	colorVal = scalarMap.to_rgba(Iy)
	ax3.plot(xvals, yvals(xvals), color=colorVal)
	ax3.plot(xvals, -1*yvals(xvals), color=colorVal)


plt.grid(True, lw=0.5, color='grey')
fig3.show()
plt.savefig('iy_for_profiles.png', bbox_inches='tight', dpi=300)


