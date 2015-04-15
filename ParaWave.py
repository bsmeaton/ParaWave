import numpy as np
import pylab as pl
from matplotlib.legend_handler import HandlerLine2D
returnval = 0.0001

print("    ____                  _       __                \n   / __ \____ __________ | |     / /___ __   _____  \n  / /_/ / __ `/ ___/ __ `/ | /| / / __ `/ | / / _ \ \n / ____/ /_/ / /  / /_/ /| |/ |/ / /_/ /| |/ /  __/ \n/_/    \__,_/_/   \__,_/ |__/|__/\__,_/ |___/\___/  \n By Ben Smeaton. \n \n Program takes input from .txt (column1: time) (column2: wave parameter) \n and outputs average maxima and minima of wave parameter \n (e.g wave height) as well as period.")

# define formula for finding maximum and minimum height points
def crest(a, b, c):
    if a > b and a > c:
        return a
    else:
        return returnval
        
def trough(a, b, c):
    if a < b and a < c:
        return a
    else:
        return returnval

def period(a,b,c):
    if a == b:
        return 0
    else:
        return c
        
# import data and parameters
inputfile = input(" Wave parameter vs time input file (e.g log_01.txt): ")
columna = np.loadtxt(open(inputfile,"rb"),delimiter=" ", usecols=(1,))
columntime = np.loadtxt(open(inputfile,"rb"),delimiter=" ", usecols=(0,))
rampuptime = input(" Input wave rampup time: ")
rampupstep = input(" Input time step size: ")
rampupint = int(float(rampuptime) / float(rampupstep))
rampupkey = np.arange(0, rampupint)

# set up offset arrays
zero = np.array([0])
columna3 = np.delete(columna, (0), axis=0)
columna3b = np.hstack((columna3,zero))
columna4 = np.hstack((zero,columna))
columna4b = np.delete(columna4, len(columna4)-1, axis=0)

wavedata = np.array(columna)
wavecompprev = np.array(columna3b)
wavecompost = np.array(columna4b)

# vectorize crest and trough maxima and minima formula
vcrest = np.vectorize(crest)
vtrough = np.vectorize(trough)
vperiod = np.vectorize(period)

# apply crest and trough max and min formula to array, then take out rampup time
resultcrest = vcrest(wavedata, wavecompprev, wavecompost)
resultcrestb = np.delete(resultcrest, rampupkey, axis=0)

resulttrough = vtrough(wavedata, wavecompprev, wavecompost)
resulttroughb = np.delete(resulttrough, rampupkey, axis=0)

resulttime = vperiod(resultcrest, returnval, columntime)
resulttimeb = np.delete(resulttime, rampupkey, axis=0)

columntimeb = np.delete(columntime, rampupkey, axis=0)

#np.savetxt('time',resulttimeb)
#np.savetxt('columna2',columna3b)
#np.savetxt('columna3',columna4b)
#np.savetxt('trough',resulttroughb)
#np.savetxt('crest',resultcrestb)

crestheightaverage = np.average(resultcrestb, weights=(resultcrestb!=returnval))
troughheightaverage = np.average(resulttroughb, weights=(resulttroughb!=returnval))

# count number of waves in selection
countcrest = (resultcrestb!=returnval).sum()
counttrough = (resulttroughb!=returnval).sum()
countwave = ((countcrest + counttrough) / 2)

# getperiod
resulttimec = np.extract(resulttimeb != 0, resulttimeb)
waveperiod = np.average(np.diff(resulttimec))

# print results
waveperiodp = str(" Average Wave Period: " + str(waveperiod))
print(waveperiodp)
waveheightp = str(" Average Wave Parameter: " + str(crestheightaverage - troughheightaverage))
print (waveheightp)
wavecrestp = str(" Average Maxima height above Datum: " + str(crestheightaverage))
print (wavecrestp)
wavetroughp = str(" Average Minima height below Datum: " + str(troughheightaverage))
print (wavetroughp)

template = """Output from WavePara from file GaugeVOF01 by Ben Smeaton.
{waveperiod}
{waveheight}
{wavecrest}
{wavetrough}
""" 
context = {
 "waveperiod":waveperiodp, 
 "waveheight":waveheightp,
 "wavecrest": wavecrestp,
 "wavetrough":wavetroughp
 } 
with  open('WaveParaResults','w') as myfile:
    myfile.write(template.format(**context))

# plot graphs
graphwave = np.delete(columna, rampupkey, axis=0)
crestline = np.full(len(columntimeb),crestheightaverage)
troughline = np.full(len(columntimeb),troughheightaverage)

line1, = pl.plot(columntimeb,graphwave,'',label = "Wave Parameter" ,linewidth=1)
line2, = pl.plot(columntimeb,crestline,'',label = "Average Maxima" ,linewidth=1)
line3, = pl.plot(columntimeb,troughline,'',label = "Average Minima" ,linewidth=1)
pl.legend(handler_map={line1: HandlerLine2D(numpoints=6)}) # plots the legend

pl.title("Wave Para Time vs Wave Parameter")
pl.xlabel("Time (s)")
pl.ylabel("Time Varying Wave Parameter")

pl.show()
