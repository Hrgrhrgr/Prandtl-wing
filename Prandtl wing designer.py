import math
#import re #RegEx can be used to check if a string contains the specified search pattern.
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import time
from matplotlib import animation
from mpl_toolkits.mplot3d import axes3d

# Struktura:
def myfunc():
    x = "fantastic"
    print("Python is " + x)
# fce pro načítání .csv dat jednotlivých airfoilů
# fce pro uložení dat
# fce pro vizualizaci dat (grafy, tabulky?)
# fce nalezení rovnice přímky
# fce pro určení úhlů hran
def getLeadingEdgeAngle(span, sweep, root, tip):
    angle = math.atan( (span*math.tan(sweep*math.pi/180) + 0.5*root - 0.5*tip)/span)*180/math.pi
    #print("Leading edge angle is ")
    #print(angle)
    return angle
    
def getTrailingEdgeAngle(span, sweep, root, tip):
    angle = math.atan( (span*math.tan(sweep*math.pi/180) - 0.5*root + 0.5*tip)/span)*180/math.pi
    #print("Trailing edge angle is ") 
    #print(angle)
    return angle

def getSectionOrigin(lead,trail,span,ofset):
    sectionOrigin.append(span*math.tan(lead*math.pi/180)+ofset)

def getWingGeometry(lead,trail,span,root,ofset):    
    for i in range(int(span+0)):
        LeadingEdgeY.append(i*math.tan(lead*math.pi/180)+ofset)
    
    for i in range(int(span+0)):
        TrailingEdgeY.append(i*math.tan(trail*math.pi/180)+root+ofset)
        

def getAoAValue (foil,aoa,rey):
    re1Found = 0
    re2Found = 0
    #print(aoa)
    if rey <= 1e5:
        re1 = 0
        re2 = 1
    if rey > 1e5 and rey <= 2e5:
        re1 = 1
        re2 = 2
    if rey > 2e5:
        if rey > 5e5:
            rey = 5e5
        re1 = 2
        re2 = 3
    if foil[re1, 99, 0] < aoa:
        Cl_re1 = foil[re1, 99, 1]
        Cd_re1 = foil[re1, 99, 2]
        Cm_re1 = foil[re1, 99, 3]
        re1Found = 1 
    if foil[re1, 0, 0] > aoa:
        Cl_re1 = foil[re1, 0, 1]
        Cd_re1 = foil[re1, 0, 2]
        Cm_re1 = foil[re1, 0, 3]
        re1Found = 1 
    if foil[re2, 99, 0] < aoa:
        Cl_re2 = foil[re2, 99, 1]
        Cd_re2 = foil[re2, 99, 2]
        Cm_re2 = foil[re2, 99, 3]
        re2Found = 1     
    if foil[re2, 0, 0] > aoa:
        Cl_re2 = foil[re2, 0, 1]
        Cd_re2 = foil[re2, 0, 2]
        Cm_re2 = foil[re2, 0, 3]
        re2Found = 1
    for l in range(1000):
        if re1Found == 1 and re2Found == 1:
            break
        if np.isnan(foil[re1, l, 0]) and re1Found == 0:
            Cl_re1 = foil[re1, l-1, 1]
            Cd_re1 = foil[re1, l-1, 2]
            Cm_re1 = foil[re1, l-1, 3]
            re1Found = 1 
            #print("Angle too high!")    
        if foil[re1, l, 0] <= aoa and foil[re1, l+1, 0] >= aoa:
            split = (aoa - foil[re1, l, 0])/(foil[re1, l+1, 0] - foil[re1, l, 0])
            Cl_re1 = foil[re1, l, 1] + split*(foil[re1, l+1, 1] - foil[re1, l, 1])
            Cd_re1 = foil[re1, l, 2] + split*(foil[re1, l+1, 2] - foil[re1, l, 2])
            Cm_re1 = foil[re1, l, 3] + split*(foil[re1, l+1, 3] - foil[re1, l, 3])
            re1Found = 1       
            #rint("Angle too low!")  
        if np.isnan(foil[re2, l, 0]) and re2Found == 0:
            Cl_re2 = foil[re2, l-1, 1]
            Cd_re2 = foil[re2, l-1, 2]
            Cm_re2 = foil[re2, l-1, 3]
            re2Found = 1 
            #print("Angle too high!")
        if foil[re2, l, 0] <= aoa and foil[re2, l+1, 0] >= aoa:
            split = (aoa - foil[re2, l, 0])/(foil[re2, l+1, 0] - foil[re2, l, 0])
            Cl_re2 = foil[re2, l, 1] + split*(foil[re2, l+1, 1] - foil[re2, l, 1])
            Cd_re2 = foil[re2, l, 2] + split*(foil[re2, l+1, 2] - foil[re2, l, 2])
            Cm_re2 = foil[re2, l, 3] + split*(foil[re2, l+1, 3] - foil[re2, l, 3])
            re2Found = 1

    if re1 == 0:
        re1=50000
    if re1 == 1:
        re1=100000    
    if re1 == 2:
        re1=200000
    if re1 == 3:
        re1=500000
    if re2 == 0:
        re2=50000
    if re2 == 1:
        re2=100000
    if re2 == 2:
        re2=200000
    if re2 == 3:
        re2=500000
        
    if rey > 50000:    
        split = (rey - re1) / (re1 - re2)
        Cl = Cl_re1 + split * (Cl_re1 - Cl_re2) 
        Cd = Cd_re1 + split * (Cd_re1 - Cd_re2)
        Cm = Cm_re1 + split * (Cm_re1 - Cm_re2)
    if rey <= 50000:
        if re1 == 50000:
            Cl = Cl_re1
            Cd = Cd_re1
            Cm = Cm_re1
        if re2 == 50000:
            Cl = Cl_re2
            Cd = Cd_re2
            Cm = Cm_re2
    return [Cl, Cd, Cm]

def killZeros(matice):
    for i in range(4):
        for j in range(99,-1,-1):
            if matice[i,j,0] != 0:
                break
            if matice[i,j,0] == 0:
                matice[i,j,3] = np.nan
                matice[i,j,2] = np.nan
                matice[i,j,1] = np.nan
                matice[i,j,0] = np.nan
    return matice 
        
def plotFoilCl(foil,foilname):
    plt.figure()
    plt.title(foilname)
    plt.xlabel("alpha")
    plt.ylabel("Cl")
    plt.plot(foil[0, 0:, 0],foil[0, 0:, 1], label = "50k_n5")
    plt.plot(foil[1, 0:, 0],foil[1, 0:, 1], label = "100k")
    plt.plot(foil[2, 0:, 0],foil[2, 0:, 1], label = "200k")
    plt.plot(foil[3, 0:, 0],foil[3, 0:, 1], label = "500k")
    plt.grid(linestyle='-', linewidth=0.5)
    plt.legend()
    plt.show
    
def plotFoilCd(foil,foilname):
    plt.figure()
    plt.title(foilname)
    plt.xlabel("alpha")
    plt.ylabel("Cd")
    plt.plot(foil[0, 0:, 0],foil[0, 0:, 2], label = "50k")
    plt.plot(foil[1, 0:, 0],foil[1, 0:, 2], label = "100k")
    plt.plot(foil[2, 0:, 0],foil[2, 0:, 2], label = "200k")
    plt.plot(foil[3, 0:, 0],foil[3, 0:, 2], label = "500k")
    plt.grid(linestyle='-', linewidth=0.5)
    plt.legend()
    plt.show  
    
def plotFoilClCd(foil,foilname):
    plt.figure()
    plt.title(foilname)
    plt.xlabel("alpha")
    plt.ylabel("Cl/Cd")
    plt.plot(foil[0, 0:, 0],foil[0, 0:, 1]/foil[0, 0:, 2], label = "50k")
    plt.plot(foil[1, 0:, 0],foil[1, 0:, 1]/foil[1, 0:, 2], label = "100k")
    plt.plot(foil[2, 0:, 0],foil[2, 0:, 1]/foil[2, 0:, 2], label = "200k")
    plt.plot(foil[3, 0:, 0],foil[3, 0:, 1]/foil[3, 0:, 2], label = "500k")
    plt.grid(linestyle='-', linewidth=0.5)
    plt.legend()
    plt.show     

def plotFoilCm(foil,foilname):
    plt.figure()
    plt.title(foilname)
    plt.xlabel("alpha")
    plt.ylabel("Cm")
    plt.plot(foil[0, 0:, 0],foil[0, 0:, 3], label = "50k")
    plt.plot(foil[1, 0:, 0],foil[1, 0:, 3], label = "100k")
    plt.plot(foil[2, 0:, 0],foil[2, 0:, 3], label = "200k")
    plt.plot(foil[3, 0:, 0],foil[3, 0:, 3], label = "500k")
    plt.grid(linestyle='-', linewidth=0.5)
    plt.legend()
    plt.show        
    
def plotLiftDistribution(speed,aoa):
    plt.figure()
    plt.title("Lift distribution")
    plt.xlabel("Span [cm]")
    plt.ylabel("Lift [grams]")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
                pass
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
                pass
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0], label=(speedPoint,"m/s at",aoaPoint,"deg"))
                                                               
                                plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
    plt.legend()
    plt.show
    
def plotTorqueDistribution(speed,aoa):
    plt.figure()
    plt.title(".25root reduced torque distribution")
    plt.xlabel("Span [cm]")
    plt.ylabel("Torque [Nm]")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 6], label=(speedPoint,"m/s at",aoaPoint,"deg"))                                                               
                                #plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
    plt.legend()
    plt.show

def plotTorqueElementDistribution(speed,aoa):
    plt.figure()
    plt.title(".25chord torque element distribution")
    plt.xlabel("Span [cm]")
    plt.ylabel("Torque [Nm]")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 3], label=(speedPoint,"m/s at",aoaPoint,"deg"))                                                               
                                #plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
    plt.legend()
    plt.show 
    
def plotMomentArmDistribution(speed,aoa):
    plt.figure()
    plt.title("Moment arm relative to element .25 chord")
    plt.xlabel("Span [cm]")
    plt.ylabel("Moment arm [mm]")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 4], label=(speedPoint,"m/s at",aoaPoint,"deg"))                                                               
                                #plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
    plt.legend()
    plt.show 
    
def plotReducedMomentArmDistribution(speed,aoa):
    plt.figure()
    plt.title("Reduced moment arm to .25 root chord")
    plt.xlabel("Span [cm]")
    plt.ylabel("Moment arm [mm]")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 5], label=(speedPoint,"m/s at",aoaPoint,"deg"))                                                               
                                #plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
    plt.legend()
    plt.show     

def plotClDistribution(speed,aoa):
    #♥plt.figure()
    #plt.title("Cl, Cd distribution")
    #plt.xlabel("Span")
    #plt.ylabel("Cl")
    #plt.grid(linestyle='-', linewidth=0.5)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    ax1.set_ylabel('Cl')
    ax2.set_ylabel('Cd')
    ax2.set_ylabel('Re')
    plt.title("Cl, Cd, Re distribution")
    ax1.set_xlabel("Span")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                

                                ax1.plot(spanCm,evalData[plotSpeed, plotAngle, 0:, 0], 'r-', label=("Cl at",speedPoint,"m/s at",aoaPoint,"deg"))
                                ax2.plot(spanCm,evalData[plotSpeed, plotAngle, 0:, 1], 'g-', label=("Cd at",speedPoint,"m/s and",aoaPoint,"deg"))
                                ax3.plot(spanCm,evalData[plotSpeed, plotAngle, 0:, 3], 'b-', label=("Re at",speedPoint,"m/s and",aoaPoint,"deg"))
                                #plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
    #plt.legend()
    plt.show
    

def plotClCdDistribution(speed,aoa):
    plt.figure()
    plt.title("Cl/Cd distribution")
    plt.xlabel("Span")
    plt.ylabel("Cl/Cd")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                plt.plot(spanCm,evalData[plotSpeed, plotAngle, 0:, 4], label=((speedPoint,"m/s at",aoaPoint,"deg")))
                                                               
                                #plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
    plt.legend()
    plt.show
    
def plotCmClDistribution(speed,aoa):
    plt.figure()
    plt.title("Cm/Cl distribution")
    plt.xlabel("Span")
    plt.ylabel("Cm/Cl")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                plt.plot(spanCm,evalData[plotSpeed, plotAngle, 0:, 2]/evalData[plotSpeed, plotAngle, 0:, 0], label=((speedPoint,"m/s at",aoaPoint,"deg")))
                                                               
                                #plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
    plt.legend()
    plt.show
    

def plotLiftDragDistribution(speed,aoa):
    plt.figure()
    plt.title("Lift/drag distribution")
    plt.xlabel("Span")
    plt.ylabel("Lift/drag")
    plt.grid(linestyle='-', linewidth=0.5)
    for speedPoint in speed:
        for aoaPoint in aoa:
            #plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 0])
            if speedPoint < tasMin or speedPoint > tasMax:
                print("Speed out of range")
            if aoaPoint < aoaMin or aoaPoint > aoaMax:
                print("Angle of attack out of range")
            if speedPoint >= tasMin and speedPoint <=tasMax and aoaPoint >= aoaMin and aoaPoint <= aoaMax:
                for speedIter in range(numberOfTASpoints):
                    if speedPoint <= (tasMin + speedIter * (tasMax - tasMin)/(numberOfTASpoints-1)):
                        for aoaIter in range(numberOfAOApoints):
                            if aoaPoint <= (aoaMin + aoaIter * (aoaMax - aoaMin)/(numberOfAOApoints-1)):
                                plotAngle = aoaIter
                                plotSpeed = speedIter
                                plt.plot(spanCm,forceData[plotSpeed, plotAngle, 0:, 2], label=(speedPoint,"m/s at",aoaPoint,"deg"))
                                                               
                                #plt.plot(spanCm,getBellDistribution(0.1*wingSpan+1,forceData[plotSpeed, plotAngle, 0, 0]))
                                #legenda actual speed
                                #legenda actual aoa
                                break
                        break
            pass
    plt.legend()
    plt.show
    pass

def plotLDmap(a1,a2):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X, Y = np.meshgrid(np.linspace(aoaMin,aoaMax,num=numberOfAOApoints),np.linspace(tasMin,tasMax,num=numberOfTASpoints))
    ax.plot_surface(Y,X,sumData[0:,0:,3])
    ax.set_xlabel('TAS [m/s]')
    ax.set_ylabel('AoA [deg]')
    ax.set_zlabel('L/D ratio')
    ax.view_init(a1, a2)
    plt.show()

def plotTorqueMap(a1,a2):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X, Y = np.meshgrid(np.linspace(aoaMin,aoaMax,num=numberOfAOApoints),np.linspace(tasMin,tasMax,num=numberOfTASpoints))
    ax.plot_surface(Y,X,sumData[0:,0:,4])
    ax.set_xlabel('TAS [m/s]')
    ax.set_ylabel('AoA [deg]')
    ax.set_zlabel('Torque [Nm]')
    ax.view_init(a1, a2)
    plt.show()

def getBellDistribution(numberOfPoints,rootLift):
    BellDistribution = []
    for i in range(int(numberOfPoints)):
        BellDistribution.append(rootLift*((1-(i/numberOfPoints)**2)**1.5))
    return BellDistribution

def findHighestLD(data,speed):
    global topLD
    global optimalAoA
    global optimalTAS
    topLD = 0
    if speed == 0:
        for i in range(numberOfTASpoints):
            for j in range(numberOfAOApoints):
                if data[i,j,3] > topLD:
                    topLD = round(data[i,j,3],2)
                    optimalAoA = round(aoaMin + j * (aoaMax - aoaMin)/(numberOfAOApoints-1),2)
                    optimalTAS = round(tasMin + i * (tasMax - tasMin)/(numberOfTASpoints-1),2)
                    Re_min = round(evalData[i,j,int(0.1*wingSpan),3])
                    Re_max = round(evalData[i,j,0,3])
                    M_pitch = round(data[i,j,4],3)
                    
    if speed != 0:
        if speed < tasMin or speed > tasMax:
                print("Speed out of range")
        if speed >= tasMin and speed <=tasMax :       
            for i in range(numberOfTASpoints):
                if speed <= (tasMin + i * (tasMax - tasMin)/(numberOfTASpoints-1)):
                    for j in range(numberOfAOApoints):
                        if data[i,j,3] > topLD:
                            topLD = round(data[i,j,3],2)
                            optimalAoA = round(aoaMin + j * (aoaMax - aoaMin)/(numberOfAOApoints-1),2)
                            optimalTAS = round(tasMin + i * (tasMax - tasMin)/(numberOfTASpoints-1),2)
                            Re_min = round(evalData[i,j,int(0.1*wingSpan),3])
                            Re_max = round(evalData[i,j,0,3])
                            M_pitch = round(data[i,j,4],3)
                    break  
    print("Best LD of", topLD, "at", optimalTAS,"m/s and", optimalAoA,"deg .. M_pitch=",M_pitch, "Nm")
    print("    with Re_min=", Re_min, ".. Re_max=", Re_max)
# Bell shape funkce!!!!!!!!!!!!!!!
# (1-x^2)^(1.5)
 
# tělo kódu
# deklarace konstant
# class Person:
#   def __init__(mysillyobject, name, age):
#     mysillyobject.name = name
#     mysillyobject.age = age

#   def myfunc(abc):
#     print("Hello my name is " + abc.name)

# p1 = Person("John", 36)
# p1.myfunc()

################################################################
start = time.time()

# načtení xfoil dat

# e71
e71_200000 = np.genfromtxt("foil_data/xf-e71-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e71_50000_n5 = np.genfromtxt("foil_data/xf-e71-il-50000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
np.resize(e71_200000,(100,4))

# e61
e61_50000 = np.genfromtxt("foil_data/xf-e61-il-50000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e61_100000 = np.genfromtxt("foil_data/xf-e61-il-100000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
#e61_100000_n5 = np.genfromtxt("foil_data/xf-e61-il-100000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e61_200000 = np.genfromtxt("foil_data/xf-e61-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e61_500000 = np.genfromtxt("foil_data/xf-e61-il-500000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e61_50000.resize(100,4)
e61_100000.resize(100,4)
#e61_100000_n5.resize(100,4)
e61_200000.resize(100,4)
e61_500000.resize(100,4)
e61 = np.stack([e61_50000, e61_100000, e61_200000, e61_500000])
e61 = killZeros(e61)

# e62
e62_50000_n5 = np.genfromtxt("foil_data/xf-e62-il-50000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e62_100000 = np.genfromtxt("foil_data/xf-e62-il-100000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
e62_100000_n5 = np.genfromtxt("foil_data/xf-e62-il-100000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e62_200000 = np.genfromtxt("foil_data/xf-e62-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e62_500000 = np.genfromtxt("foil_data/xf-e62-il-500000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e62_50000_n5.resize(100,4)
e62_100000.resize(100,4)
e62_100000_n5.resize(100,4)
e62_200000.resize(100,4)
e62_500000.resize(100,4)
e62 = np.stack([e62_50000_n5, e62_100000, e62_200000, e62_500000])
e62 = killZeros(e62)

# e63
e63_50000_n5 = np.genfromtxt("foil_data/xf-e63-il-50000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e63_50000 = np.genfromtxt("foil_data/xf-e63-il-50000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e63_100000 = np.genfromtxt("foil_data/xf-e63-il-100000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
e63_100000_n5 = np.genfromtxt("foil_data/xf-e63-il-100000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e63_200000 = np.genfromtxt("foil_data/xf-e63-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e63_500000 = np.genfromtxt("foil_data/xf-e63-il-500000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e63_50000_n5.resize(100,4)
e63_50000.resize(100,4)
e63_100000.resize(100,4)
e63_100000_n5.resize(100,4)
e63_200000.resize(100,4)
e63_500000.resize(100,4)
e63 = np.stack([e63_50000, e63_100000, e63_200000, e63_500000])
e63 = killZeros(e63)

# e64
e64_50000_n5 = np.genfromtxt("foil_data/xf-e64-il-50000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e64_100000 = np.genfromtxt("foil_data/xf-e64-il-100000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
e64_100000_n5 = np.genfromtxt("foil_data/xf-e64-il-100000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e64_200000 = np.genfromtxt("foil_data/xf-e64-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e64_500000 = np.genfromtxt("foil_data/xf-e64-il-500000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e64_50000_n5.resize(100,4)
e64_100000.resize(100,4)
e64_100000_n5.resize(100,4)
e64_200000.resize(100,4)
e64_500000.resize(100,4)
e64 = np.stack([e64_50000_n5, e64_100000, e64_200000, e64_500000])
e64 = killZeros(e64)

# e71
e71_50000_n5 = np.genfromtxt("foil_data/xf-e71-il-50000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e71_100000 = np.genfromtxt("foil_data/xf-e71-il-100000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
e71_100000_n5 = np.genfromtxt("foil_data/xf-e71-il-100000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e71_200000 = np.genfromtxt("foil_data/xf-e71-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e71_500000 = np.genfromtxt("foil_data/xf-e71-il-500000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e71_50000_n5.resize(100,4)
e71_100000.resize(100,4)
e71_100000_n5.resize(100,4)
e71_200000.resize(100,4)
e71_500000.resize(100,4)
e71 = np.stack([e71_50000_n5, e71_100000, e71_200000, e71_500000])
e71 = killZeros(e71)

# e228
e228_50000_n5 = np.genfromtxt("foil_data/xf-e228-il-50000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e228_100000 = np.genfromtxt("foil_data/xf-e228-il-100000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
e228_100000_n5 = np.genfromtxt("foil_data/xf-e228-il-100000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
e228_200000 = np.genfromtxt("foil_data/xf-e228-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
e228_500000 = np.genfromtxt("foil_data/xf-e228-il-500000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
e228_50000_n5.resize(100,4)
e228_100000.resize(100,4)
e228_100000_n5.resize(100,4)
e228_200000.resize(100,4)
e228_500000.resize(100,4)
e228 = np.stack([e228_50000_n5, e228_100000, e228_200000, e228_500000])
e228 = killZeros(e228)

# s2048
s2048_50000_n5 = np.genfromtxt("foil_data/xf-s2048-il-50000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
s2048_100000 = np.genfromtxt("foil_data/xf-s2048-il-100000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
s2048_100000_n5 = np.genfromtxt("foil_data/xf-s2048-il-100000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
s2048_200000 = np.genfromtxt("foil_data/xf-s2048-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
s2048_500000 = np.genfromtxt("foil_data/xf-s2048-il-500000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
s2048_50000_n5.resize(100,4)
s2048_100000.resize(100,4)
s2048_100000_n5.resize(100,4)
s2048_200000.resize(100,4)
s2048_500000.resize(100,4)
s2048 = np.stack([s2048_50000_n5, s2048_100000, s2048_200000, s2048_500000])
s2048 = killZeros(s2048)

# s4022
s4022_50000_n5 = np.genfromtxt("foil_data/xf-s4022-il-50000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
s4022_50000 = np.genfromtxt("foil_data/xf-s4022-il-50000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
s4022_100000 = np.genfromtxt("foil_data/xf-s4022-il-100000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4) )
s4022_100000_n5 = np.genfromtxt("foil_data/xf-s4022-il-100000-n5.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
s4022_200000 = np.genfromtxt("foil_data/xf-s4022-il-200000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
s4022_500000 = np.genfromtxt("foil_data/xf-s4022-il-500000.csv", dtype='float', delimiter=',', skip_header=11, usecols=(0,1,2,4))
s4022_50000.resize(100,4)
s4022_50000_n5.resize(100,4)
s4022_100000.resize(100,4)
s4022_100000_n5.resize(100,4)
s4022_200000.resize(100,4)
s4022_500000.resize(100,4)
s4022 = np.stack([s4022_50000_n5, s4022_100000, s4022_200000, s4022_500000])
s4022 = killZeros(s4022)

#------------------------------------------------------------------------------
#       VÝCHOZÍ HODNOTY
#------------------------------------------------------------------------------
# deklarace výchozích hodnot
wingSpan = 750

nominalTAS = 8
nominalAoA = 3.0

mass = 0.4
airdensity = 1.225
viscosity0C = 13.324e-6
viscosity10C = 14.207e-6
viscosity20C = 15.111e-6
viscosity = viscosity20C


profile0 = s4022
profile1 = s4022
profile2 = s4022
profile3 = e228

aoaMin = -3.5
aoaMax = 12 
tasMin = 5
tasMax = 18
numberOfTASpoints = 11
numberOfAOApoints = 21

sweepS1 = -6
sweepS2 = -6
sweepS3 = 0

twistTotal = 4
twistRoot = 2.4
sweepSections = 3

cgShift = 150

chordRoot = 265
chordRatio12 = 0.78
chordRatio23 = 0.47
chordTip = 0.3*chordRoot


rootSectionPercentage = 0.24
endSectionPercentage = 0.28

spanS1 = round(rootSectionPercentage*wingSpan)
spanS2 = round((1-rootSectionPercentage-endSectionPercentage)*wingSpan)
spanS3 = round(endSectionPercentage*wingSpan)
# spanS1 = round(0.8*wingSpan/(1+spanSectionRatio))
# spanS2 = round(spanS1*spanSectionRatio)
# spanS3 = round((1-(spanS1+spanS2)/wingSpan)*wingSpan)
#spanS3 = 0.2*wingSpan

e63Thickness = 7

chord12 = round(chordRoot*chordRatio12)
chord23 = round(chordRoot*chordRatio23)

evalData = np.empty([numberOfTASpoints,numberOfAOApoints,int(wingSpan*0.1+1),5])
evalData.fill(np.nan)

forceData = np.empty([numberOfTASpoints,numberOfAOApoints,int(wingSpan*0.1+1),7])
forceData.fill(np.nan)

sumData = np.empty([numberOfTASpoints,numberOfAOApoints,5])
sumData.fill(0)

twist = np.empty([int(0.1*wingSpan+1)])
twist.fill(0)

global Reynolds
Reynolds = 0
wingArea = 0

global lift
global drag

global LeadingEdgeY
LeadingEdgeY = []

global TrailingEdgeY
TrailingEdgeY = []

global chord
chord = []
span = []
spanCm = []
global BellDistribution
BellDistribution = []

global sectionOrigin
sectionOrigin = []

localOptimalAoA = 0
localM_pitch = 0
localTopLD = 0


leadingEdgeAngle1 = getLeadingEdgeAngle(spanS1,sweepS1,chordRoot,chord12)
leadingEdgeAngle2 = getLeadingEdgeAngle(spanS2,sweepS2,chord12,chord23)
leadingEdgeAngle3 = getLeadingEdgeAngle(spanS3,sweepS3,chord23,chordTip)

trailingEdgeAngle1 = getTrailingEdgeAngle(spanS1,sweepS1,chordRoot,chord12)
trailingEdgeAngle2 = getTrailingEdgeAngle(spanS2,sweepS2,chord12,chord23)
trailingEdgeAngle3 = getTrailingEdgeAngle(spanS3,sweepS3,chord23,chordTip)

getSectionOrigin(leadingEdgeAngle1,trailingEdgeAngle1,spanS1,0)
getSectionOrigin(leadingEdgeAngle2,trailingEdgeAngle2,spanS2,sectionOrigin[0])
getSectionOrigin(leadingEdgeAngle3,trailingEdgeAngle3,spanS3,sectionOrigin[1])

getWingGeometry(leadingEdgeAngle1,trailingEdgeAngle1,spanS1,chordRoot,0)
getWingGeometry(leadingEdgeAngle2,trailingEdgeAngle2,spanS2,chord12,sectionOrigin[0])
getWingGeometry(leadingEdgeAngle3,trailingEdgeAngle3,spanS3,chord23,sectionOrigin[1])
#print("Tady /\ ")

# Zakončení křídla
LeadingEdgeY.append(spanS3*math.tan(leadingEdgeAngle3*math.pi/180)+sectionOrigin[1])
TrailingEdgeY.append(spanS3*math.tan(trailingEdgeAngle3*math.pi/180)+chord23+sectionOrigin[1])

for i in range(int(wingSpan+1)):
    chord.append(abs(LeadingEdgeY[i]-TrailingEdgeY[i]))
    span.append(i)
    wingArea = wingArea + chord[i]*1
for i in range(int(0.1*wingSpan+1)): 
    spanCm.append(i)
wingArea = round(wingArea)
aspectRatio = round(wingSpan*wingSpan / wingArea,2)

print("--------------------")
#print("Span sections lengths")
print("Section 1:",spanS1,"mm")
print("Section 2:",spanS2,"mm")
print("Section 3:",spanS3,"mm")
print("Wing half:",spanS1 + spanS2 + spanS3,"mm")
print("Wing span:",2*(spanS1 + spanS2 + spanS3),"mm")
print("Wing area:",wingArea,"mm2")
print("Aspect ratio:", aspectRatio)
print("---------------------")


#--------------------------------------------------------------
# Induced drag equation!!!!
# Cdi = (1+k)*Cl^2 *(pi*AR)
#    MAIN
#--------------------------------------------------------------
# Přepočtení plochy křídla, průřezu, aspect ratio
for i in range (10):
    pass
# Twist calculation
TAS = nominalTAS
aoa = nominalAoA
twist[0] = 0
# Root lift inicialization
Reynolds = int(round(TAS * 0.001* chord[0] / viscosity))
rootData = getAoAValue(profile0, aoa, Reynolds)
dynamicPressure = 0.5*airdensity*TAS*TAS
rootLift = 1e-2*1e-3*chord[0]* rootData[0]* dynamicPressure

# Get Bell distribution
BellDistribution = getBellDistribution(int(0.1*wingSpan+1), rootLift)

# for k in range(1,int(0.1*wingSpan)):
#     Cl = 0
#     Reynolds = int(round(TAS * 0.001* chord[k*10] / viscosity))
#     pass

# wingSpan smyčka PRVNÍ - element křídla v milimetrech
for k in range(1,int(0.1*spanS1)):
    newLift = 0
    Reynolds = int(round(TAS * 0.001* chord[k*10] / viscosity))
    split = abs(10*k - 0) / abs(spanS1 - 0)
    while abs(BellDistribution[k]-newLift) > 0.01 * BellDistribution[k]:                     
        inProfile = getAoAValue(profile0, aoa + twist[k], Reynolds)
        outProfile = getAoAValue(profile1, aoa + twist[k], Reynolds)   
        Cl = inProfile[0] + split * (outProfile[0] - inProfile[0])        
        newLift = 1e-2*1e-3*chord[k*10]* Cl * dynamicPressure
        if (BellDistribution[k] - newLift) > 0.01 *BellDistribution[k]:
            twist[k] = twist[k] + 0.01*aoa
        if (BellDistribution[k] - newLift) < -0.01 *BellDistribution[k]:
            twist[k] = twist[k] - 0.01*aoa    
    #print(k)       
# wingSpan smyčka DRUHÁ - element křídla v milimetrech
for k in range(int(0.1*spanS1),int(0.1*(spanS1+spanS2))):
    newLift = 0
    Reynolds = int(round(TAS * 0.001* chord[k*10] / viscosity))
    split = (10*k - spanS1) / spanS2
    while abs(BellDistribution[k]-newLift) > 0.02 * BellDistribution[k]: 
        #print(aoa, twist[k],k)                    
        inProfile = getAoAValue(profile1, aoa + twist[k], Reynolds)
        outProfile = getAoAValue(profile2, aoa + twist[k], Reynolds)   
        Cl = inProfile[0] + split * (outProfile[0] - inProfile[0])        
        newLift = 1e-2*1e-3*chord[k*10]* Cl * dynamicPressure
        
        if (BellDistribution[k] - newLift) > 0.02 *BellDistribution[k]:
            twist[k] = twist[k] + 0.005*aoa
        if (BellDistribution[k] - newLift) < -0.02 *BellDistribution[k]:
            twist[k] = twist[k] - 0.005*aoa    
    #print(k) 
    
# wingSpan smyčka TŘETÍ - element křídla v milimetrech
for k in range(int(0.1*(spanS1+spanS2)),int(0.1*wingSpan)+1):
    newLift = 0
    Reynolds = int(round(TAS * 0.001* chord[k*10] / viscosity))
    split = (10*k - (spanS1+spanS2)) / spanS3 
    while abs(BellDistribution[k]-newLift) > 0.04 * BellDistribution[k]:                     
        inProfile = getAoAValue(profile2, aoa + twist[k], Reynolds)
        outProfile = getAoAValue(profile3, aoa + twist[k], Reynolds)   
        Cl = inProfile[0] + split * (outProfile[0] - inProfile[0])        
        newLift = 1e-2*1e-3*chord[k*10]* Cl * dynamicPressure
        
        if (BellDistribution[k] - newLift) > 0.04 *BellDistribution[k]:
            twist[k] = twist[k] + 0.001*aoa
        if (BellDistribution[k] - newLift) < -0.04 *BellDistribution[k]:
            twist[k] = twist[k] - 0.001*aoa    
    #print(k) 

end = time.time()
print("Wing twist found")
print("Twist max=",round(np.amax(twist),1),", twist min=",round(np.amin(twist),1),", elapsed time",round((end - start),1),"s")
print("---------------------------------------------------------------")
#--------------------------------------------------------------
# TAS smyčka - true airspeed



for i in range(numberOfTASpoints):
    TAS = round(tasMin + i * (tasMax - tasMin)/(numberOfTASpoints-1),2)
    # Dynamic pressure q8 = 1/2.ro.v^2
    dynamicPressure = 0.5*airdensity*TAS*TAS
    if i == 0:
        print("0 %,  TAS= ", TAS, "m/s")
    if i == round(0.1*(numberOfTASpoints-1)):
        print("10 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")        
    if i == round(0.2*(numberOfTASpoints-1)):
        print("20 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")
    if i == round(0.3*(numberOfTASpoints-1)):
        print("30 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")    
    if i == round(0.4*(numberOfTASpoints-1)):
        print("40 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm") 
    if i == round(0.5*(numberOfTASpoints-1)):
        print("50 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")    
    if i == round(0.6*(numberOfTASpoints-1)):
        print("60 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")
    if i == round(0.7*(numberOfTASpoints-1)):
        print("70 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")    
    if i == round(0.8*(numberOfTASpoints-1)):
        print("80 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")
    if i == round(0.9*(numberOfTASpoints-1)):
        print("90 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")
    if i == round(1*(numberOfTASpoints-1)):
        print("100 %, TAS=", TAS, "m/s, Re_min=", Reynolds, ", Re_max=", int(evalData [i-1,0,0,3]),", LD=",localTopLD,", AoA=",localOptimalAoA,"deg, M_pitch=",localM_pitch, "Nm")
    localTopLD = 0
    #--------------------------------------------------------------
    # AOA smyčka - angle of attack
    for j in range(numberOfAOApoints):
        # Rozpětí AOA     
        aoa = aoaMin + j * (aoaMax - aoaMin)/(numberOfAOApoints-1)
        #--------------------------------------------------------------
        # wingSpan smyčka PRVNÍ - element křídla v milimetrech
        for k in range(int(0.1*spanS1)):
            # k = wingElement
            #--------------------------------------------------------------
            Reynolds = int(round(TAS * 0.001* chord[k*10] / viscosity))
            split = abs(10*k - 0) / abs(spanS1 - 0) 
                
            inProfile = getAoAValue(profile0, aoa+ twist[k], Reynolds)
            outProfile = getAoAValue(profile1, aoa+ twist[k], Reynolds)
            
            Cl = inProfile[0] + split * (outProfile[0] - inProfile[0])
            Cd = inProfile[1] + split * (outProfile[1] - inProfile[1])
            Cm = inProfile[2] + split * (outProfile[2] - inProfile[2])
            evalData [i,j,k,0] = Cl
            evalData [i,j,k,1] = Cd
            evalData [i,j,k,2] = Cm
            evalData [i,j,k,3] = Reynolds
            evalData [i,j,k,4] = round(Cl/Cd,2)
        #--------------------------------------------------------------
        # wingSpan smyčka DRUHÁ - element křídla v milimetrech
        for k in range(int(0.1*spanS1),int(0.1*(spanS1+spanS2))):
            # k = wingElement
            #--------------------------------------------------------------
            Reynolds = int(round(TAS * 0.001* chord[k*10] / viscosity))
            split = (10*k - spanS1) / spanS2
            #print(aoa,twist[k],TAS,k)
            inProfile = getAoAValue(profile1, aoa+ twist[k], Reynolds)
            outProfile = getAoAValue(profile2, aoa+ twist[k], Reynolds)
            
            Cl = inProfile[0] + split * (outProfile[0] - inProfile[0])
            Cd = inProfile[1] + split * (outProfile[1] - inProfile[1])
            Cm = inProfile[2] + split * (outProfile[2] - inProfile[2])
            evalData [i,j,k,0] = Cl
            evalData [i,j,k,1] = Cd
            evalData [i,j,k,2] = Cm
            evalData [i,j,k,3] = Reynolds
            evalData [i,j,k,4] = round(Cl/Cd,2)
        #--------------------------------------------------------------
        # wingSpan smyčka TŘETÍ - element křídla v milimetrech
        for k in range(int(0.1*(spanS1+spanS2)),int(0.1*wingSpan)+1):
            # k = wingElement
            #--------------------------------------------------------------
            Reynolds = int(round(TAS * 0.001* chord[k*10] / viscosity))
            split = (10*k - (spanS1+spanS2)) / spanS3
            
            inProfile = getAoAValue(profile2, aoa+ twist[k], Reynolds)
            outProfile = getAoAValue(profile3, aoa+ twist[k], Reynolds)
            
            Cl = inProfile[0] + split * (outProfile[0] - inProfile[0])
            Cd = inProfile[1] + split * (outProfile[1] - inProfile[1])
            Cm = inProfile[2] + split * (outProfile[2] - inProfile[2])
            evalData [i,j,k,0] = Cl
            evalData [i,j,k,1] = Cd
            evalData [i,j,k,2] = Cm
            evalData [i,j,k,3] = Reynolds
            evalData [i,j,k,4] = round(Cl/Cd,2)
        #--------------------------------------------------------------
        for k in range(int(0.1*wingSpan)+1):
            # Dynamic pressure q8 = 1/2.ro.v^2
            # Force in grams for some reason
            forceData [i,j,k,0] = (1000/9.81)*evalData[i,j,k,0]*1e-2*chord[k*10]*1e-3*dynamicPressure
            # Drag as a fuction of lift and cd/cl ratio: Drag = Lift * Cd/Cd
            forceData [i,j,k,1] = forceData [i,j,k,0]*evalData[i,j,k,1]/evalData[i,j,k,0]
            # Lift/Drag distribution
            forceData [i,j,k,2] = forceData [i,j,k,0]/forceData [i,j,k,1]
            # Element torque as M = dynamicPressure * Cm * crosssectional area ...Frontal Area = 1e-2* chord[k*10]*1e-3*e63Thickness*0.01
            forceData [i,j,k,3] = -1*evalData[i,j,k,2]*1e-2* chord[k*10]*1e-3*e63Thickness*0.01*dynamicPressure
            # Moment arm in milimeters
            forceData [i,j,k,4] = 1000*(1000/9.81)*(forceData [i,j,k,3] / forceData [i,j,k,0])
            # Moment arm reduced to 0.25 root chord position
            forceData [i,j,k,5] = LeadingEdgeY[k*10] + 0.25 * chord[k*10] + forceData [i,j,k,4] - 0.25*chord[0]
            # Reduced torque to 0.25 root chord position
            forceData [i,j,k,6] = 0.001*forceData [i,j,k,5] * evalData[i,j,k,0]*1e-2*chord[k*10]*1e-3*dynamicPressure
            
            # Total lift force
            sumData [i,j,0] = sumData [i,j,0] + forceData [i,j,k,0]
            # Total drag
            sumData [i,j,1] = sumData [i,j,1] + forceData [i,j,k,1]
            # Required power
            sumData [i,j,2] = sumData [i,j,1] *(9.81/1000)*TAS
            # Total L/D ratio
            sumData [i,j,3] = sumData [i,j,0] /sumData [i,j,1]
            # Total 0.25 root chord torque
            sumData [i,j,4] = sumData [i,j,4] + forceData [i,j,k,6]
        if sumData[i,j,3] > localTopLD:
            localTopLD = round(sumData[i,j,3],1)
            localOptimalAoA = round(aoaMin + j * (aoaMax - aoaMin)/(numberOfAOApoints-1),1)
            localM_pitch = round(sumData[i,j,4],3)
# Lift averaged Reynolds number


#--------------------------------------------------------------

#print("evalData")
#print(evalData[32,83,0:,0:])
#print("forceData")
#print(forceData[32,83,0:,0:])
#print("sumData")
#print(sumData[32,0:,0:])

# Plot wingform
plt.figure(1)
plt.plot(span,LeadingEdgeY)
plt.plot(span,TrailingEdgeY)
plt.show

# Plot chord distribution
plt.figure(2)
plt.plot(span,chord)
plt.show

plt.figure()
plt.plot(twist)
plt.show

# plotFoilCl(e63, "e63")
# plotFoilClCd(e63, "e63")
# plotFoilCd(e63, "e63")
# plotFoilCl(e228, "e228")
# plotFoilClCd(e228, "e228")
# plotFoilCd(e228, "e228")

#plotFoilCd(e228, "e228")
#plotFoilCm(e228, "e228")

plotLiftDistribution([10], [-2,0,2,4,6])
plotClDistribution([10], [2.5])
plotClCdDistribution([10], [0,2,3,4,5,6])
#plotCmClDistribution([10], [-3,0,2,4,6])
#plotMomentArmDistribution([10], [-3,0,2,4,6])
#plotReducedMomentArmDistribution([10], [-3,0,2,4,6])
plotTorqueElementDistribution([10], [-3,0,2,4,6])
plotTorqueDistribution([10], [-3,0,2,4,6])
#plotLiftDragDistribution([10], [0,2,4])

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
X, Y = np.meshgrid(np.linspace(aoaMin,aoaMax,num=numberOfAOApoints),np.linspace(tasMin,tasMax,num=numberOfTASpoints))
surf = ax.plot_surface(Y,X,sumData[0:,0:,4])
ax.set_xlabel('TAS [m/s]')
ax.set_ylabel('AoA [deg]')
ax.set_zlabel('Torque [Nm]')
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
X, Y = np.meshgrid(np.linspace(aoaMin,aoaMax,num=numberOfAOApoints),np.linspace(tasMin,tasMax,num=numberOfTASpoints))
surf = ax.plot_surface(Y,X,sumData[0:,0:,3])
ax.set_xlabel('TAS [m/s]')
ax.set_ylabel('AoA [deg]')
ax.set_zlabel('L/D ratio')
#ax.view_init(30, 0)
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
X, Y = np.meshgrid(np.linspace(aoaMin,aoaMax,num=numberOfAOApoints),np.linspace(tasMin,tasMax,num=numberOfTASpoints))
surf = ax.plot_surface(Y,X,sumData[0:,0:,0])
ax.set_xlabel('TAS [m/s]')
ax.set_ylabel('AoA [deg]')
ax.set_zlabel('Lift [grams]')
plt.show()

#print("------------------------------------------") 
#findHighestLD(sumData, 0)
#findHighestLD(sumData, 15)
#findHighestLD(sumData, 10)
#findHighestLD(sumData, 7)
#findHighestLD(sumData, 4)
# Udělat fci pro nalezení stabilního letu M = 0

#   smyčka citlivosti na +- 20 % změnu sweepu (pozice i úhlu)


x = lambda a, b, c : a + b + c
#print(x(5, 6, 2))
# kinematická viskozita

# wing span
# nominal airspeed
# mass
# sweep1, sweep2, sweep3
# sweep1_coord, sweep2_coord, sweep3_coord
# sweep section angles lead, trail
print("---------------------------------------------------------------") 
end = time.time()
print("Total run time",round((end - start),1),"s")