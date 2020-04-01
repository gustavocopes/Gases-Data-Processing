# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:11:36 2020

@author: GCopes
"""

import pandas as pd
import numpy as np
import picarroush
import os
#import statistics
from scipy.stats import linregress
import matplotlib.pyplot as plt


calibration =  'Manual'
estacion= 'Ushuaia'
instrument = 'Picarro'
dir_root = 'C:\\Users\\GCopes\\Desktop\\{0}\\'.format(estacion)
direct = dir_root + '{0}\\Minutal_SYNC\\'.format(instrument)
year = 2016

flask1_CO = 0.09045
flask2_CO = 0.27847000
flask1_CO2 = 329.530000
flask2_CO2 = 427.180000
flask1_CH4 = 1.77803000
flask2_CH4 = 2.39766000

def fit(dato1,dato2):
    
    model = linregress(dato1,dato2)
    slope, intercept = model.slope, model.intercept
    slope = slope.round(5)
    intercept = intercept.round(5)
    
    return slope, intercept
    


def autocal(pic_data, year):
    #pic_data.loc[(pic_data.solenoide_valves == 3 ) | (pic_data.solenoide_valves == 35), ['CO', 'CO2_dry','CH4_dry','H2O']]
    #flask 1 & 2 were closed in november.
    if year == 2019:
        cal1 = pic_data.loc[(pic_data.solenoid_valves == 3 ) | (pic_data.solenoid_valves == 35), ['CO', 'CO2_dry','CH4_dry','H2O','solenoid_valves']] 
        cal3 = pic_data.loc[(pic_data.solenoid_valves == 9 ) | (pic_data.solenoid_valves == 41), ['CO', 'CO2_dry','CH4_dry','H2O','solenoid_valves']]
        cal2 = pic_data.loc[(pic_data.solenoid_valves == 5 ) | (pic_data.solenoid_valves == 37), ['CO', 'CO2_dry','CH4_dry','H2O','solenoid_valves']]

        cal1.loc['2019-11-15 18:00:00': '2019-11-28 14:31:00', ['CO', 'CO2_dry','CH4_dry','H2O', 'solenoid_valves']] = np.nan
        #cal1.loc['2019-11-15 20:48:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        #cal1.loc['2019-11-23 14:23:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        #cal1.loc['2019-11-28 13:35:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
    
        cal1.loc['2019-12-07 16:20:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal1.loc['2019-12-22 22:25:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
    
        cal2.loc['2019-11-15 18:03:00':'2019-11-28 14:50:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal2.loc['2019-12-07 16:40:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal2.loc['2019-12-22 22:45:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
    
        cal3.loc['2019-11-15 12:59:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2019-11-15 19:03:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2019-11-15 21:28:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2019-11-23 15:03:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan 
        cal3.loc['2019-11-28 14:15:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2019-11-28 15:10:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2019-12-07 17:00:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2019-12-22 23:05:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        
        cal12019 = cal1.H2O  
        cal22019 = cal2.H2O
        
        return cal1, cal2, cal3, cal12019, cal22019
    
            
    if year == 2020:
        cal1 = pic_data.loc[(pic_data.solenoid_valves == 3 ) | (pic_data.solenoid_valves == 35), ['CO', 'CO2_dry','CH4_dry','H2O','solenoid_valves']] 
        cal3 = pic_data.loc[(pic_data.solenoid_valves == 9 ) | (pic_data.solenoid_valves == 41), ['CO', 'CO2_dry','CH4_dry','H2O','solenoid_valves']]
        cal2 = pic_data.loc[(pic_data.solenoid_valves == 5 ) | (pic_data.solenoid_valves == 37), ['CO', 'CO2_dry','CH4_dry','H2O','solenoid_valves']]
              
        cal1.loc['2020-01-05 12:16:00':'2020-01-05 12:17:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal1.loc['2020-01-20 18:21:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal1.loc['2020-02-05 00:26:00':'2020-02-05 00:27:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal1.loc['2020-02-05 00:45:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal1.loc['2020-02-07 20:27:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
    
        cal2.loc['2020-01-05 12:36:00':'2020-01-05 12:37:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal2.loc['2020-01-20 18:41:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal2.loc['2020-02-05 00:46:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
    
        cal3.loc['2020-01-05 12:56:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2020-01-20 19:01:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2020-02-05 01:06:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        cal3.loc['2020-02-07 20:48:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
        
        cal12020 = cal1.H2O  
        cal22020 = cal2.H2O
        
        return cal1, cal2, cal3, cal12020, cal22020
    

for i in os.listdir(dir_root + 'Picarro\\Minutal_SYNC\\' ):
     
    year += 1  

    INPUTDIR = direct + '{0}'.format(year)  # os.getcwd()
    OUTPUTDIR = os.getcwd()

    input_dir= dir_root + 'Met\\RAW\\2018'#'{0}'.format(year)
    input_file = 'ush{0}.met'.format(year)
    header_file = 'headline.txt'
    
    pic_data, met = picarroush.load_new_files(input_dir,INPUTDIR, year)
    
    if year == 2017: None
    
    if year == 2018 and calibration == 'Manual':
      a = pic_data.loc['2018-04-06 18:02:00':'2018-04-06 18:20:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      a2 = pic_data.loc['2018-04-06 18:36:00':'2018-04-06 18:54:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_a = a.mean()
      r_a2 = a2.mean()
      slopea, intercepta = fit(r_a, r_a2)

      b = pic_data.loc['2018-04-11 18:44:00':'2018-04-11 19:02:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      b2 = pic_data.loc['2018-04-11 18:22:00':'2018-04-11 18:39:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_b = b.mean()
      r_b2 = b2.mean()
      slopeb, interceptb = fit(r_b, r_b2)

      c = pic_data.loc['2018-04-18 19:17:00':'2018-04-18 19:35:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      c2 = pic_data.loc['2018-04-18 19:40:00':'2018-04-18 19:58:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_c = c.mean()
      r_c2 = c2.mean()
      slopec, interceptc = fit(r_c, r_c2)

      d = pic_data.loc['2018-04-25 18:50:00':'2018-04-25 19:04:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      d2 = pic_data.loc['2018-04-25 18:31:00':'2018-04-25 18:45:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_d = d.mean()
      r_d2 = d2.mean()
      sloped, interceptd = fit(r_d, r_d2)

      e = pic_data.loc['2018-05-02 17:59:00':'2018-05-02 18:11:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      e2 = pic_data.loc['2018-05-02 18:17:00':'2018-05-02 18:30:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_e = e.mean()
      r_e2 = e2.mean()
      slopee, intercepte = fit(r_e, r_e2)

      f = pic_data.loc['2018-05-09 18:12:00':'2018-05-09 18:26:00', ['CO', 'CO2_dry','CH4_dry','H2O']]
      f2 = pic_data.loc['2018-05-09 17:53:00':'2018-05-09 18:07:00', ['CO', 'CO2_dry','CH4_dry','H2O']]
      r_f = f.mean()
      r_f2 = f2.mean()
      slopef, interceptf = fit(r_f, r_f2)

      g = pic_data.loc['2018-05-16 18:00:00':'2018-05-16 18:14:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      g2 = pic_data.loc['2018-05-16 18:24:00':'2018-05-16 18:38:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_g = g.mean()
      r_g2 = g2.mean()
      slopeg, interceptg = fit(r_g, r_g2)

      h = pic_data.loc['2018-05-25 16:14:00':'2018-05-25 16:30:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      h2 = pic_data.loc['2018-05-25 15:53:00':'2018-05-25 16:06:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_h = h.mean()
      r_h2 = h2.mean()
      slopeh, intercepth = fit(r_h, r_h2)

      i = pic_data.loc['2018-05-30 19:06:00':'2018-05-30 19:14:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      i2 = pic_data.loc['2018-05-31 19:21:00':'2018-05-30 19:30:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_i = i.mean()
      r_i2 = i2.mean()
      slopei, intercepti = fit(r_i, r_i2)

      j = pic_data.loc['2018-06-20 17:14:00':'2018-06-20 17:22:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      j2 = pic_data.loc['2018-06-20 16:05:00':'2018-06-20 16:14:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_j = j.mean()
      r_j2 = j2.mean()
      slopej, interceptj = fit(r_j, r_j2)

      k = pic_data.loc['2018-07-11 18:50:00':'2018-07-11 18:58:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      k2 = pic_data.loc['2018-07-11 19:03:00':'2018-07-11 19:12:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_k = k.mean()
      r_k2 = k2.mean()
      slopek, interceptk = fit(r_k, r_k2)

      l = pic_data.loc['2018-08-08 18:30:00':'2018-08-08 18:41:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      l2 = pic_data.loc['2018-08-08 18:16:00':'2018-08-08 18:24:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_l = l.mean()
      r_l2 = l2.mean()
      slopel, interceptl = fit(r_l, r_l2)

      m = pic_data.loc['2018-09-05 19:25:00':'2018-09-05 19:33:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      m2 = pic_data.loc['2018-09-05 19:39:00':'2018-09-05 19:47:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_m = m.mean()
      r_m2 = m2.mean()
      slopem, interceptm = fit(r_m, r_m2)

      n = pic_data.loc['2018-10-03 19:41:00':'2018-10-03 19:49:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      n2 = pic_data.loc['2018-10-03 19:27:00':'2018-10-03 19:35:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_n = n.mean()
      r_n2 = n2.mean()
      slopen, interceptn = fit(r_n, r_n2)

      o = pic_data.loc['2018-11-08 14:50:00':'2018-11-08 14:58:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      o2 = pic_data.loc['2018-11-08 15:08:00':'2018-11-08 15:16:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_o = o.mean()
      r_o2 = o2.mean()
      slopeo, intercepto = fit(r_o, r_o2)

      p = pic_data.loc['2018-12-06 19:41:00':'2018-12-06 19:49:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      p2 = pic_data.loc['2018-12-06 19:24:00':'2018-12-06 19:33:00', ['CO', 'CO2_dry','CH4_dry','H2O']] 
      r_p = p.mean()
      r_p2 = p2.mean()
      slopep, interceptp = fit(r_p, r_p2)
    
      cal1 =  a.append([b,c,d,e,f,g,h,i,j,k,l,m,n,o,p],ignore_index=False)
      cal2 =  a2.append([b2,c2,d2,e2,f2,g2,h2,i2,j2,k2,l2,m2,n2,o2,p2],ignore_index=False)
      cal12018 = cal1.H2O  
      cal22018 = cal2.H2O
      
      slope2018 = slopea.append([slopeb,slopec,sloped,slopee,slopef,slopeg,slopeh,slopei,slopej,slopek,slopel,slopem,slopen,slopeo,slopep])
      intercept2018 = intercepta.append([interceptb, interceptc,interceptd,intercepte,interceptf,interceptg,intercepth,intercepti,interceptj,interceptk,interceptl,interceptm,interceptn,intercepto,interceptp])
      
      s = open(dir_root + 'slopeinterc2018.dat'.format(instrument,estacion, year), 'wt')
      f.write(slope2018.to_string())
      f.close()
    if year == 2019 and calibration == 'Manual':
    
      a = pic_data.loc['2019-01-09 15:12:00' :'2019-01-09 15:20', ['CO', 'CO2_dry', 'CH4_dry', 'H2O']]
      a1 = pic_data.loc['2019-01-09 15:28:00' :'2019-01-09 15:36', ['CO', 'CO2_dry', 'CH4_dry', 'H2O']]
      r_a = a.mean()
      r_a1 = a1.mean()
      slopea, intercepta = fit(r_a, r_a2)

      b = pic_data.loc['2019-02-08 18:06:00' :'2019-02-08 18:14', ['CO', 'CO2_dry', 'CH4_dry', 'H2O']]
      b1 = pic_data.loc['2019-02-08 17:50:00' :'2019-02-08 17:58', ['CO', 'CO2_dry', 'CH4_dry', 'H2O']]
      r_b = b.mean()
      r_b1 = b1.mean()
      slopeb, interceptb = fit(r_b, r_b2)

      c = pic_data.loc['2019-03-06 13:50:00' :'2019-03-06 13:58', ['CO', 'CO2_dry', 'CH4_dry', 'H2O']]
      c1 = pic_data.loc['2019-03-06 14:04:00' :'2019-03-06 14:12', ['CO', 'CO2_dry', 'CH4_dry', 'H2O']]
      r_c = c.mean()
      r_c1 = c1.mean()
      slopec, interceptc = fit(r_c, r_c2)

      d = pic_data.loc['2019-04-10 19:11:00':'2019-04-10 19:19:00', ['CO','CO2_dry','CH4_dry','H2O']]
      d1 = pic_data.loc['2019-04-10 18:56:00':'2019-04-10 19:04:00', ['CO','CO2_dry','CH4_dry','H2O']]
      r_d = d.mean()
      r_d1 = d1.mean()
      sloped, interceptd = fit(r_d, r_d2)
    
      f = pic_data.loc['2019-05-08 15:34:00':'2019-05-08 15:42:00', ['CO','CO2_dry','CH4_dry','H2O']] 
      f1 = pic_data.loc['2019-05-08 15:48:00':'2019-05-08 15:56:00', ['CO','CO2_dry','CH4_dry','H2O']]
      r_f = f.mean()
      r_f1 = f1.mean()
      slopef, interceptf = fit(r_f, r_f2)

      g = pic_data.loc['2019-06-06 19:40:00':'2019-06-06 19:48:00', ['CO','CO2_dry','CH4_dry','H2O']]
      g2 = pic_data.loc['2019-06-06 19:23:00':'2019-06-06 19:31:00', ['CO','CO2_dry','CH4_dry','H2O']]
      r_g = g.mean()
      r_g2 = g2.mean()    
      slopeg, interceptg = fit(r_g, r_g2)

          
      cal1 =  a.append([b,c,d,f,g],ignore_index=False)
      cal2 =  a1.append([b1,c1,d1,f1,g2],ignore_index=False)
      
      cal12019 = cal1.H2O  
      cal22019 = cal2.H2O
      
      slope2019 = slopea.append([slopeb,slopec,sloped,slopef,slopeg])
      intercept2019 = intercepta.append([interceptb, interceptc,interceptd,interceptf,interceptg])
   
      
    if calibration == 'Auto' and year == 2019:
      cal1, cal2, cal3, cal12019, cal22019 = autocal(pic_data, year)
      
    if calibration == 'Auto' and year == 2020:
      cal1, cal2, cal3, cal12020, cal22020 = autocal(pic_data, year)

    cal = pd.DataFrame()

    if year == 2018:
      date = '2018-12-31'
    
    elif year == 2019:
      date = '2019-12-31'
    
    elif year == 2020 and calibration == 'Auto':
      date = '2020-12-31'
      
    if year == 2018 | 2019 | 2020:
            cal['avgCO(1)'] = cal1.CO.resample('A').mean()
            cal['flask1_CO'] =  flask1_CO 

            cal['avgCO(2)'] = cal2.CO.resample('A').mean()
            cal['flask2_CO'] = flask2_CO

            cal['avgCO2(1)'] = cal1.CO2_dry.resample('A').mean()
            cal['flask1_CO2'] = flask1_CO2

            cal['avgCO2(2)'] = cal2.CO2_dry.resample('A').mean()
            cal['flask2_CO2'] = flask2_CO2
        
            cal['avgCH4(1)'] = cal1.CH4_dry.resample('A').mean()
            cal['flask1_CH4'] = flask1_CH4
        
            cal['avgCH4(2)'] = cal2.CH4_dry.resample('A').mean()
            cal['flask2_CH4'] = flask2_CH4
            
            # slope and interpept for CO
            flask1pic= cal.loc[date,'avgCO(1)'] * 1000
            flask1= float(cal['flask1_CO']) * 1000

            flask2pic=  cal.loc[date,'avgCO(2)']*1000
            flask2 = float(cal['flask2_CO'])*1000

#for CO2
            flask1picCO2= cal.loc[date,'avgCO2(1)']
            flask1CO2= float(cal['flask1_CO2'])

            flask2picCO2=  cal.loc[date,'avgCO2(2)']
            flask2CO2 = float(cal['flask2_CO2'])

#for CH4
            flask1picCH4= cal.loc[date,'avgCH4(1)'] * 1000
            flask1CH4= float(cal['flask1_CH4']) * 1000

            flask2picCH4=  cal.loc[date,'avgCH4(2)'] * 1000
            flask2CH4 = float(cal['flask2_CH4']) * 1000
  
            data1 = (flask1, flask2)
            data2 = (flask1pic, flask2pic)
            
            slopeCO, interceptCO = fit(data1, data2)

            # model = linregress(data1, data2) # CO
            # slopeCO, interceptCO = model.slope, model.intercept
            # slopeCO = slopeCO.round(5)
            # interceptCO = interceptCO.round(5)

            xCO2 = (flask1CO2, flask2CO2)
            yCO2 = (flask1picCO2, flask2picCO2)
            
            slopeCO2, interceptCO2 = fit(xCO2,yCO2)

            xCH4 = (flask1CH4, flask2CH4)
            yCH4 = (flask1picCH4, flask2picCH4)
            
            slopeCH4, interceptCH4 = fit(xCH4, yCH4)
             
    else:  None
    


####Calibration periods -removed first and last minute for more of them in order to avoid sample contamination


    if calibration == 'Auto' and year == 2019| 2020:
        cal['avgCO(3)'] = cal3.CO.resample('A').mean()
        cal['avgCO2(3)'] = cal3.CO2_dry.resample('A').mean()
        cal['avgCH4(3)'] = cal3.CH4_dry.resample('A').mean()

        cal['flask3_CO'] =  0.14379
        flask3 = cal['flask3_CO'] * 1000
        cal['flask3_CO2'] = 419.125
        flask3CO2 = cal['flask3_CO2']
    
        cal['flask3_CH4'] = 1.94863
        flask3CH4 = cal['flask3_CH4'] * 1000

        flask3pic = cal.loc[date, 'avgCO(3)'] * 1000
        data1 = (flask1, flask3,flask2)
        data2 = (flask1pic,flask3pic, flask2pic)
        flask3picCO2 = cal.loc[date, 'avgCO2(3)']
        xCO2 = (flask1CO2, flask3CO2, flask2CO2)
        yCO2 = (flask1picCO2, flask3picCO2, flask2picCO2)
        flask3picCH4=  cal.loc[date,'avgCH4(3)'] * 1000
        xCH4 = (flask1CH4, flask3CH4,flask2CH4)
        yCH4 = (flask1picCH4, flask3picCH4, flask2picCH4)
    
    
    

# fig,(CH4, CO2, CO) = plt.subplots(1, 3, figsize = (15,6))

# CO.plot(data1, data2, '.-')
# CO.text(100,287, 'CO  {0} {1}'.format(calibration, year))
# CO.set_xlabel('CO SMN assigned [ppb]')
# CO.set_ylabel('CO measured [ppb]')
# CO.text(100, 250, 'slope: {0}'.format(slopeCO), fontsize=12)
# CO.text(100, 240, 'intercept: {0}'.format(interceptCO), fontsize=12)
# #CH4.title('Ushuaia 2020')

# CO2.plot(xCO2,yCO2, '.-')
# CO2.text(335,430, '$CO2$  {0} {1}'.format(calibration, year))
# #plt.title('CO2 Ushuaia {0}'.format(year))
# CO2.set_xlabel('CO2 SMN assigned [ppm]')
# CO2.set_ylabel('CO2 measured [ppm]')
# CO2.text(335, 410, 'slope: {0}'.format(slopeCO2), fontsize=12)
# CO2.text(335, 405, 'intercept: {0}'.format(interceptCO2), fontsize=12)
               
# CH4.plot(xCH4, yCH4,'.-')
# CH4.text(1800,2435, 'CH4  {0} {1}'.format(calibration, year))
# #plt.title('CH4 Ushuaia {0}'.format(year))
# CH4.set_xlabel('CH4 SMN assigned [ppb]')  
# CH4.set_ylabel('CH4 measured [ppb]')
# CH4.text(1800, 2300, 'slope: {0}'.format(slopeCH4), fontsize=12)
# CH4.text(1800, 2270, 'intercept: {0}'.format(interceptCH4), fontsize=12)

# plt.show()
# fig.savefig('{0}_cal_Picarro{1}.png'.format(calibration, year))
if calibration == 'Manual':
    ncal = cal12018.append(cal12019)
    ncal2 = cal22018.append(cal22019)
    fig2 = plt.figure(figsize=(15,10))
    ax1 = fig2.add_subplot(111)
    avg = ncal.mean()
    avg2 = ncal2.mean()
    avg = round(avg, 5)
    avg2 = round(avg2, 5)
    ax1.scatter(ncal.index, ncal[0:], s=10, c='b', marker="s", label='flask(1) {0} Mean: {1}'.format(calibration, avg))
    ax1.scatter(ncal2.index,ncal2[0:], s=10, c='r', marker="o", label=' flask(2) {0} Mean: {1}'.format(calibration, avg2))
    ax1.set_xlabel('date')
    ax1.set_ylabel('$H2O$')
    
    plt.legend(loc='upper left');
    plt.show()
    fig2.savefig('H2O {0}.png'.format(calibration))
    
if calibration == 'Auto':
    ncal = cal12019.append(cal12020)
    ncal2 = cal22019.append(cal22020)
    fig2 = plt.figure(figsize=(15,10))
    ax1 = fig2.add_subplot(111)
    avg = ncal.mean()
    avg2 = ncal2.mean()
    avg = round(avg, 5)
    avg2 = round(avg2, 5)
    ax1.scatter(ncal.index, ncal[0:], s=10, c='b', marker="s", label='flask(1) {0} Mean: {1}'.format(calibration, avg))
    ax1.scatter(ncal2.index,ncal2[0:], s=10, c='r', marker="o", label=' flask(2) {0} Mean: {1}'.format(calibration, avg2))
    ax1.set_xlabel('date')
    ax1.set_ylabel('$H2O$')
    
    plt.legend(loc='upper left');
    plt.show()
    fig2.savefig('H2O {0}.png'.format(calibration))
    


def calmensual(cal, cal1, cal2):

    var = pd.DataFrame()
   
    var['avgCO(1)'] = cal1.CO.resample('M').mean()
    var['avgCO(2)'] = cal2.CO.resample('M').mean()
    var['avgCO2(1)'] = cal1.CO2_dry.resample('M').mean()
    var['avgCO2(2)'] = cal2.CO2_dry.resample('M').mean()
    var['avgCH4(1)'] = cal1.CH4_dry.resample('M').mean()
    var['avgCH4(2)'] = cal2.CH4_dry.resample('M').mean()
    
    flask1pic= var.loc['avgCO(1)'] * 1000
    flask1_CO = cal['flask1_CO'] * 1000
    #print linregress(var['avgCO(1)'],flask1_CO)

    flask2pic=  var.loc['avgCO(2)']*1000
    cal['flask2_CO']*1000

#for CO2
    flask1picCO2= var.loc['avgCO2(1)']
    cal['flask1_CO2']

    flask2picCO2=  var.loc['avgCO2(2)']
    cal['flask2_CO2']

#for CH4
    flask1picCH4= var.loc['avgCH4(1)'] * 1000
    cal['flask1_CH4'] * 1000

    flask2picCH4= var.loc['avgCH4(2)'] * 1000
    cal['flask2_CH4'] * 1000
    return var

    