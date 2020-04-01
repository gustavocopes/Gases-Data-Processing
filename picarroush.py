__author__ = 'German Perez Fogwill'

import pandas as pd
import datetime
import numpy as np
import os
from optparse import OptionParser
import math  # import math library
import scipy  # import scientific python functions


year = 2019
estacion= 'Ushuaia'
instrument = 'Picarro'
VERSIONSTR = "\n%prog v. 0.1 2015 byNegro\n"
dir_root = 'C:\\Users\\GCopes\\Desktop\\{0}\\'.format(estacion)
INPUTDIR = dir_root + '{0}\\Minutal_SYNC\\{1}'.format(instrument,year)  # os.getcwd()
OUTPUTDIR = os.getcwd()

input_dir= dir_root + 'Met\\RAW\\2018'#'{0}'.format(year)
input_file = 'ush{0}.met'.format(year)
header_file = 'headline.txt'



def _arraytest(*args):
    """
    Function to convert input parameters in as lists or tuples to
    arrays, while leaving single values intact.

    Test function for single values or valid array parameter input
    (J. Delsman).

    Parameters:
        args (array, list, tuple, int, float): Input values for functions.

    Returns:
        rargs (array, int, float): Valid single value or array function input.

    Examples
    --------

     #   >>> _arraytest(12.76)
        12.76
      #  >>> _arraytest([(1,2,3,4,5),(6,7,8,9)])
        array([(1, 2, 3, 4, 5), (6, 7, 8, 9)], dtype=object)
      #  >>> x=[1.2,3.6,0.8,1.7]
      #  >>> _arraytest(x)
        array([ 1.2,  3.6,  0.8,  1.7])
      #  >>> _arraytest('This is a string')
        'This is a string'

    """

    rargs = []
    for a in args:
        if isinstance(a, (list, tuple)):
            rargs.append(scipy.array(a))
        else:
            rargs.append(a)
    if len(rargs) == 1:
        return rargs[0]  # no unpacking if single value, return value i/o list
    else:
        return rargs


def windvec(aux_wind):
    """
    Function to calculate the wind vector from time series of wind
    speed and direction.

    Parameters:
        - u: array of wind speeds [m s-1].
        - D: array of wind directions [degrees from North].

    Returns:
        - uv: Vector wind speed [m s-1].
        - Dv: Vector wind direction [degrees from North].

    Examples
    --------

      #  >>> u = scipy.array([[ 3.],[7.5],[2.1]])
       # >>> D = scipy.array([[340],[356],[2]])
        #>>> windvec(u,D)
       # (4.162354202836905, array([ 353.2118882]))
       # >>> uv, Dv = windvec(u,D)
        #>>> uv
        #4.162354202836905
        #>>> Dv
        #array([ 353.2118882])

    """

    aux_wind = aux_wind.str.split('_')

    u = aux_wind.apply(lambda x: x[0])
    D = aux_wind.apply(lambda x: x[1])

    u = u.values
    D = D.values

    u = [float(i) for i in u]
    D = [float(i) for i in D]

    if u.__len__() == 0:
        return np.nan, np.nan

    # Test input array/value
    u, D = _arraytest(u, D)

    ve = 0.0  # define east component of wind speed
    vn = 0.0  # define north component of wind speed
    D = D * math.pi / 180.0  # convert wind direction degrees to radians
    for i in range(0, len(u)):
        ve = ve + u[i] * math.sin(D[i])  # calculate sum east speed components
        vn = vn + u[i] * math.cos(D[i])  # calculate sum north speed components
    ve = - ve / len(u)  # determine average east speed component
    vn = - vn / len(u)  # determine average north speed component
    uv = math.sqrt(ve * ve + vn * vn)  # calculate wind speed vector magnitude
    # Calculate wind speed vector direction
    vdir = scipy.arctan2(ve, vn)
    vdir = vdir * 180.0 / math.pi  # Convert radians to degrees
    if vdir < 180:
        Dv = vdir + 180.0
    else:
        if vdir > 180.0:
            Dv = vdir - 180
        else:
            Dv = vdir
    return uv, Dv  # uv in m/s, Dv in dgerees from North


def load_new_files(input_dir,INPUTDIR, year):
    ozn_files_list = []
    met_files_list = []
    header_file_list = []
    df = pd.DataFrame()
    df_met = pd.DataFrame()

    # Listo los headers para ver si hay mas de uno.
    for file in os.listdir(INPUTDIR):
        
        if file.endswith(".txt") | file.endswith('.TXT'):
            header_file_list.append(file)
        elif file.endswith(".ozn") | file.endswith('.OZN'):
            # ozn_files_list.append(file)
            df = df.append(load_TEI49C_file(input_dir, file, year))
        elif file.endswith(".cv") | file.endswith('.CV'):
            df = df.append(load_horiba_file(INPUTDIR, file, year))
        elif file.endswith(".csv") | file.endswith('.CSV'):
            df = df.append(picarro_alternative(INPUTDIR,file,year))
    
    for file in os.listdir(input_dir):
        
        if file.endswith(".txt") | file.endswith('.TXT'):
            header_file_list.append(file)
        elif file.endswith(".ozn") | file.endswith('.OZN'):
            # ozn_files_list.append(file)
            df = df.append(load_TEI49C_file(input_dir, file, year))
        elif file.endswith(".hor") | file.endswith('.HOR'):
            df = df.append(load_horiba_file(input_dir, file, year))
        elif file.endswith(".cs") | file.endswith('.CV'):
            df = df.append(picarro_alternative(INPUTDIR,file,year))

        elif file.endswith(".met") | file.endswith('.MET'):

            # met_files_list.append(file)  ### quito la opcion de seleccionar encabezado 
#            if header_file_list.__len__() != 0:
#                i = 0
#                for p in header_file_list:
#                    print('[' + str(i) + ']:\t' + p)
#                    i += 1
#                var = input("Seleccione el archivo del HEADER para procesar el archivo " + file + ": ")
                aux_df = load_cr10_file(input_dir, file, header_file, year)
                df_met = df_met.append(aux_df)

           # else:  #POR AHORA NO QUIERO ESTO
            #    aux_df = load_lqo_2014_met(file, header_file_list[0], year)
                # aux_df = load_cr10_file(file, header_file_list[0], year)
             #   df_met = df_met.append(aux_df)
             

    return df, df_met


def load_lqo_2014_met(input_file, header_file, year):
    met = pd.read_csv(INPUTDIR + '\\2014LQO.met', parse_dates=[[0, 1]], dayfirst=True)
    met_df = pd.DataFrame(index=met.FECHA_HORA)

    met_df['WD'] = met.WD.data
    met_df['WS'] = met.WS.data
    met_df['RH'] = met.RH.data
    met_df['AP'] = met.AP.data
    met_df['AT'] = met.AT.data

    met_df['WD'] = met_df['WD'] * 10
    met_df['WS'] = met_df['WS'] * 0.514444
    met_df.loc[met_df.WD == 0, ['WD']] = 360

    return met_df


def load_mbi_file(input_dir, year):
    df_data = pd.DataFrame.from_csv(input_dir + '\\' + 'mbiomet' + year + '.DAT', sep=',', infer_datetime_format=True)
    df_met = pd.DataFrame.from_csv(input_dir + '\\' + 'mbiomet' + year + '.DAT', sep=',', infer_datetime_format=True)

    df_data.columns = ['WD', 'WS', 'AT', 'RH', 'DT', 'AP', 'NA', 'NA', 'NA', 'NA', 'O3']
    df_met.columns = ['WD', 'WS', 'AT', 'RH', 'DT', 'AP', 'NA', 'NA', 'NA', 'NA', 'O3']

    return df_data, df_met


def load_TEI49C_file(input_dir, file, year):
    df = []
    full_dir = input_dir + '\\' + file

    fi = pd.read_csv(full_dir, delim_whitespace=True, header=1, comment=';', parse_dates=[[0, 1]],
                     error_bad_lines=False, warn_bad_lines=False)
    fi.columns = ['Time_Date', 'Alarms', 'O3', 'IntenA', 'IntenB', 'Bench_Temp', 'LampTemp', 'O3LampTemp', 'FlowA',
                  'FlowB', 'Pres']

    data_time = pd.DatetimeIndex(fi['Time_Date'])
    data_time = data_time + pd.DateOffset(year=int(year))

    data = np.array(fi.iloc[:, 2::], dtype=np.float64)
    df = pd.DataFrame(data=data, index=data_time)

    df.columns = ['O3', 'IntenA', 'IntenB', 'Bench_Temp', 'LampTemp', 'O3LampTemp', 'FlowA', 'FlowB', 'Pres']

    return df

def load_Picarro_file(input_dir, file, year):
    ##df = []
    full_dir = input_dir + '\\' + file

    ##dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    fi = pd.read_csv(full_dir, sep=',', comment=';', parse_dates=[[0, 1]], index_col=0,error_bad_lines=False, warn_bad_lines=False)
    #fi.columns = ['FRAC_DAYS_SINCE_JAN1', 'FRAC_HRS_SINCE_JAN1', 'JULIAN_DAYS', 'EPOCH_TIME', 'ALARM_STATUS', 'INST_STATUS', 'CavityPressure','CavityTemp', 'DasTemp', 'EtalonTemp', 'WarmBoxTemp', 'MPVPosition', 'OutletValve', 'CO_sync', 'O3', 'CH4_sync', 'H2O_sync']

    #data_time = pd.DatetimeIndex(fi['DATE_TIME'])
    #data_time = data_time + pd.DateOffset(year=int(year))

    #data = np.array(fi.iloc[:, 2::], dtype=np.float64)
    #df = pd.DataFrame(data=data, index=data_time)

    #df.columns = ['FRAC_DAYS_SINCE_JAN1', 'FRAC_HRS_SINCE_JAN1', 'JULIAN_DAYS', 'EPOCH_TIME', 'ALARM_STATUS', 'INST_STATUS', 'CO_sync', 'CO2_sync', 'CH4_sync', 'H2O_sync']

    return fi

def load_horiba_file(INPUTDIR, file, year):

    df = []
    full_dir = INPUTDIR + '\\' + file
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    fi = pd.read_csv(full_dir, delimiter=",", index_col = 0,  error_bad_lines=False, warn_bad_lines=False, date_parser=dateparse, engine="python")

    df = pd.DataFrame(data=fi, index=fi.index)

    
    return df

def picarro_alternative(INPUTDIR, file, year):

    df = pd.DataFrame()
    full_dir = INPUTDIR + '\\' + file
    #dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    fi = pd.read_csv(full_dir, sep=r'\s+ |,', comment=';', parse_dates=[[0, 1]], index_col=0,
                     error_bad_lines=False, warn_bad_lines=False, engine='python')

  
   
    #df['H2O_rep'] = (-0.772 + np.sqrt((0.772)**2+(4*fi['H2O_sync']*0.019493)))/(2*0.019493)# fórmula para generar H2O reported

    
#Parte del año no tiene valores dry, si no los tiene los calcula a partir del H2o rep
    if year != 2021:
        try:
            df['CO'] = fi['CO_sync']
            df['CO2_dry'] = fi['CO2_sync'] / (1 + 0.000053 * fi['H2O_sync']**2 - 0.015157 * fi['H2O_sync'])# C. Zellweger eq. 5a
#           
            df['CH4_dry'] = fi['CH4_sync'] / (1 - 0.000026 * fi['H2O_sync']**2 - 0.012043 * fi['H2O_sync'])# C. Zellweger eq 5b
            df['H2O'] = fi['H2O_sync']
            df['solenoid_valves'] = fi.solenoid_valves
        except KeyError:
            print(file)
        except AttributeError:
             df['solenoid_valves'] = -999    
             
             
        # try:
        #      df['solenoid_valves'] = fi.solenoid_valves
                
        # except AttributeError:
        #      df['solenoid_valves'] = -999
            
            
    #else:
        
                        
        # try :
        #     df['CO'] = fi['CO']
        #     df['CO2_dry'] = fi['CO2'] / (1 + 0.000053 * fi['h2o_reported']**2 - 0.015157 * fi['h2o_reported'])# C. Zellweger eq. 5a
        #     df['CH4_dry'] = fi['CH4'] / (1 - 0.000026 * fi['h2o_reported']**2 - 0.012043 * fi['h2o_reported'])# C. Zellweger eq 5b
        #     df['H2O'] = fi['h2o_reported']
            
        # #except ValueError : 
           
            
        # except KeyError:
            
         # df['CO'] = fi['CO_sync']
         # df['CO2_dry'] = fi['CO2_sync'] / (1 + 0.000053 * fi['H2O_sync']**2 - 0.015157 * fi['H2O_sync'])# C. Zellweger eq. 5a
         # df['CH4_dry'] = fi['CH4_sync'] / (1 - 0.000026 * fi['H2O_sync']**2 - 0.012043 * fi['H2O_sync'])# C. Zellweger eq 5b
         # df['H2O'] = fi['H2O_sync']
         

 
       
#        a = datetime.datetime(2017,9,9,11,0,0)
#        b = datetime.datetime(2017,12,5,23,59,0)        
        
#                
#        df.loc['2017-09-09 13:00:00':'2017-09-09 23:59:00','24H', ['CO', 'CO2_sync','CO2_dry','CH4_sync','CH4_dry','H2O_sync']] = np.nan

        

    return df

def load_old_files(input_dir, year):
    files_list = []
    header_file_list = []
    df = pd.DataFrame()

    # Listo los headers para ver si hay mas de uno.
    for file in os.listdir(input_dir):
        if file.endswith(".txt") | file.endswith('.TXT'):
            header_file_list.append(file)

    # Listo los archivos que voy a cargar en memoria
    for file in os.listdir(input_dir):
        if file.endswith(".dat") | file.endswith('.DAT'):

            if (header_file_list.__len__() != 1):
                i = 0
                for p in header_file_list:
                    print('[' + str(i) + ']:\t' + p)
                    i += 1
                var = input("Seleccione el archivo del HEADER para procesar el archivo:\t " + file)
                year = int(input("Seleccione el año del archivo procesar el archivo:\t "))
                aux_df = load_cr10_file(file, header_file_list[int(var)], year)
                df = df.append(aux_df[['WD', 'WS', 'RH', 'AP', 'AT', 'O3']])

            else:
                aux_df = load_cr10_file(file, header_file_list, year)
                df = df.append(aux_df)

    return df, df


def load_cr10_file(INPUTDIR, input_file, header_file, year):
    with open(INPUTDIR + '\\' + header_file) as f:
    #with open(header_file) as f:
        header = f.readlines()

    header = header[0].split(',')

    file = pd.read_csv(INPUTDIR + '\\' + input_file, error_bad_lines=False, warn_bad_lines=False)
    #file = pd.read_csv(input_file, error_bad_lines=False, warn_bad_lines=False)

    file = file.iloc[:, 0:header.__len__()]
    file = file[file.iloc[:, 0] != 102]
    file.columns = header

    time_str = [str(i) for i in file['TIME (UTC)']] #muy mala praxis
    aux = []
    for i in time_str:
        aux.append('0' * (4 - i.__len__()) + i)

    # time_str = aux

    b = ",".join(str(int(i)) for i in file.iloc[:, 3]) #TODO El 3 dice la posicion de 'TIME (UTC)'
    b = b.split(',')
    b = [i.rjust(4, '0') for i in b]
    file.iloc[:, 3] = b #TODO El 3 dice la posicion de 'TIME (UTC)'

    a = (file['Julian Day'].map(int)).map(str) + ' ' + file['TIME (UTC)']

    time = []

    for row in a:

        try:
            time.append(datetime.datetime.strptime(str(year) + ' ' + row, "%Y %j %H%M"))
        except ValueError:
            aux_time = row.replace(' 24', ' 23')
            aux_time = datetime.datetime.strptime(str(year) + ' ' + aux_time, "%Y %j %H%M")
            aux_time += datetime.timedelta(hours=1)
            time.append(aux_time)

    data = np.array(file.iloc[:, 4::], dtype=np.float64)
    df_met = pd.DataFrame(data=data, index=time)
    df_met.columns = header[4::]

    return df_met


def resample_met(df_met, period_to_resample):
    aux_wind = df_met['WS'].map(str) + '_' + df_met['WD'].map(str)

    df_met = df_met.resample(period_to_resample).mean()
    aux_wind = aux_wind.resample(period_to_resample).apply(windvec)
    df_met['WS'] = aux_wind.apply(lambda x: x[0])
    df_met['WD'] = aux_wind.apply(lambda x: x[1])

    return df_met


def process_data(df, df_met, max_std_co, max_std_co2, max_std_ch4, min_ws, max_ws, min_wd, max_wd, year, instrument):

    df_met = resample_met(df_met, 'H')

    
    if instrument == 'Horiba':
            df.loc[(df.Status == '100010-0') | (df.Status == '010010-0') | (df.Status == '010000-0'),['CO']] = np.nan # calibraciones Horiba 
            df.loc[((df.CO > 500) | (df.CO < 0)), ['CO']] = np.nan  # 500 para co 100 para o3

            co = pd.DataFrame()
            
            co['DATE'] = '9999-99-99'
            co['TIME'] = '99:99'
            co.reindex(pd.date_range(pd.datetime(int(year), 1, 1, 0, 0), pd.datetime(int(year), 12, 31, 23, 59), freq='H'))
           
            co['CO'] = df.CO.resample('H').mean()
            co['SD'] = df.CO.resample('H').std()
            co['ND'] = df.CO.resample('H').count()
            co['F'] = 0

            co.CO = co.CO.round(3)
            
            co.loc[(df_met.WS > max_ws) | (df_met.WS < min_ws), ['F']] = [1]  # 3 viento bajo o muy alto
            co.loc[(df_met.WD > max_wd) | (df_met.WD < min_wd), ['F']] = [1] #2 no background
            co.loc[(df_met.WS.isnull()) | (df_met.WD.isnull()), ['F']] = [1] #no se las condiciones del viento
            co.loc[(co.ND < 40), ['F']] = 1  #  es 1 para el caso de CO de Ushuaia
            #co.loc[(co.SD > max_std_co),['F']] = [2] # desvio estandar alto
            co.loc[co.ND < 3, ['SD']] = [-999.999]

            co.loc[(np.isnan(co.CO)), ['CO','SD','ND','F']] = [ -999.999, -999.999, -9, 2] 
            co.loc[(co.CO == -999.999), ['SD','ND', 'F']] = [-999.999, -9, 2]
            co.loc[((co.CO == 0) & (co.SD == 0)), ['CO', 'ND', 'SD', 'F']] = [-999.999, -9, -999.999, 2]
            co.loc[(np.isnan(co.SD)), ['SD']] = [-999.999]

  
    else :
        
        pic_data = pd.DataFrame()
            # met_data = pd.DataFrame()
    



    #df.loc[((df.CO_sync > 2000) | (df.CO_sync < 0)), ['CO_sync']] = np.nan  # 500 para co 100 para o3
    # df.loc[((df.CO2_sync > 1000) | (df.CO2_sync < 0)), ['CO2_sync']] = np.nan  # 500 para co 100 para o3
    # df.loc[((df.CO2_dry_sync > 1000) | (df.CO2_dry_sync < 0)), ['CO2_dry_sync']] = np.nan  # 500 para co 100 para o3
    #
    # df.loc[((df.CH4_sync > 10) | (df.CH4_sync < 0)), ['CH4_sync']] = np.nan  # 500 para co 100 para o3
    # df.loc[((df.CH4_dry_sync > 10) | (df.CH4_dry_sync < 0)), ['CH4_dry_sync']] = np.nan  # 500 para co 100 para o3
    if instrument == 'Picarro':
        
    #Datos de la calibración 2019 -- Estimated by Christoph 2019
        p_CO = 1.0027
        o_CO = -3
        p_CO2= 0.9944
        o_CO2 = -0.28
        p_CH4= 1.0008	
        o_CH4 = 0.85
    
    #Datos de la calibracion 2018 manual
        p_CO_2018 = 1.007645455	
        o_CO_2018 = -0.004945455
        p_CO2_2018 = 0.993483333	
        o_CO2_2018 = 0.038383333
        p_CH4_2018= 0.999172727	
        o_CH4_2018= 0.000736364
    
    

    
    # Datos de Ozono
        # pic_data['DATE'] = '9999-99-99'
        # pic_data['TIME'] = '99:99'
        #pic_data['WD'] = df_met.WD
        pic_data.reindex(pd.date_range(pd.datetime(int(year), 11, 13, 0, 0), pd.datetime(int(year), 12, 31, 23, 59), freq='T'))
        pic_data['solenoid_valves'] = df.solenoid_valves
        pic_data.loc[np.isnan(pic_data.solenoid_valves), ['solenoid_valves']] = -999
        pic_data.solenoid_valves.astype(int)
        pic_data['CO'] = df.CO
        pic_data['CO'] = pic_data['CO'] * 1000 # convertion from ppm to ppb
        #pic_data['CO2_dry_G1301'] = df.CO2_sync.resample('H').mean()
        pic_data['CO2_dry'] = df.CO2_dry
        pic_data['CH4_dry'] = df.CH4_dry *1000
#        pic_data['SD_CO'] = df.CO.resample('H').std()    #pic_data['CH4_dry_G1301'] = df.CH4_sync.resample('H').mean()
#        pic_data['SD_CO2'] = df.CO2_dry.resample('H').std()
#    #pic_data['ND_CO'] = df.CO_sync.resample('H', how='count')
#    #pic_data['ND_CO2'] = df.CO2_sync.resample('H').count()
#    #pic_data['ND_CH4'] = df.CH4_sync.resample('H').count()
#        pic_data['SD_CH4'] = df.CH4_dry.resample('H').std()
    # pic_data['SD_CH4P'] = df.CH4_dry_sync.resample('H', how=np.std)
    #pic_data['H2O_sync'] = df.H2O_sync.resample('H').mean()
    #pic_data['H2O_rep'] = (-0.772 + np.sqrt((0.772)**2+(4*pic_data['H2O_sync']*0.019493)))/(2*0.019493)# fórmula para generar H2O reported
        pic_data['H2O'] = df.H2O

    #pic_data['CH4_dry_Picarro'] = df.CH4_dry_sync.resample('H').mean()
    #pic_data['CO2_dry_G1301'] = pic_data['CO2_dry_G1301'] / (-0.0002674 * pic_data['H2O']**2 - 0.01200 * pic_data['H2O'] + 1)#formual del paper de picarro
    #pic_data['CH4_dry_Picarro'] = (pic_data['CH4_dry_Picarro'] - 0.001) / 0.9994
    #pic_data['CH4_dry_G1301'] = pic_data['CH4_dry_G1301'] / (-0.0002393 * pic_data['H2O'] ** 2 - 0.00982 * pic_data['H2O'] + 1)
    # pic_data['CH4_dry_G1301'] = (pic_data['CH4_dry_G1301'] - 0.001) / 0.9994 #factor calibracion para CH4
    # #pic_data['CO2_dry_Picarro'] = df.CO2_dry_sync.resample('H').mean()
    # pic_data['CO2_dry_G1301'] = (pic_data['CO2_dry_G1301'] - 0.0193) / 0.9935# factor de calibracion para CO2
    # pic_data['CO2_dry'] = (pic_data['CO2_dry'] - 0.0193) / 0.9935
    # pic_data['CH4_dry'] = (pic_data['CH4_dry'] - 0.001) / 0.9994
       ## remuevo valores de calibracion para 2019
    if estacion == 'Ushuaia':
        if year == 2019:
            pic_data.loc['2019-03-06 13:49:00':'2019-03-06 14:15:00', ['CO','CO2_dry','CH4_dry','H2O']] = np.nan
            pic_data.loc['2019-04-10 18:55:00':'2019-04-10 19:22:00', ['CO','CO2_dry','CH4_dry','H2O']] = np.nan
            pic_data.loc['2019-05-08 15:33:00':'2019-05-08 15:59:00', ['CO','CO2_dry','CH4_dry','H2O']] = np.nan
            pic_data.loc['2019-06-06 19:22:00':'2019-06-06 19:51:00', ['CO','CO2_dry','CH4_dry','H2O']] = np.nan
            
            
        elif year == 2018:   ##calibracion para 2018 y sistema de calibracion de Horiba
                pic_data.loc['2018-04-06 18:00:00':'2018-04-06 19:00:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-04-11 18:20:00':'2018-04-11 19:05:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-04-18 19:15:00':'2018-04-18 20:02:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-04-25 18:30:00':'2018-04-25 19:10:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-05-02 17:55:00':'2018-05-02 18:35:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-05-09 17:50:00':'2018-05-09 11:30:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-05-16 18:00:00':'2018-05-16 18:42:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-05-25 15:50:00':'2018-05-25 16:35:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-05-30 19:05:00':'2018-05-30 19:35:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-06-20 16:05:00':'2018-06-20 17:25:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-07-11 18:49:00':'2018-07-11 19:15:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-08-08 18:15:00':'2018-08-08 18:45:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-09-05 19:24:00':'2018-09-05 19:50:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-10-03 19:26:00':'2018-10-03 19:55:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-11-08 14:49:00':'2018-11-08 15:20:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
                pic_data.loc['2018-12-06 19:24:00':'2018-12-06 19:55:00', ['CO', 'CO2_dry','CH4_dry','H2O']] = np.nan
            
            
    
        
        if year==[2018, 2017]:
                pic_data['CO'] = (pic_data['CO'] - o_CO_2018) / p_CO_2018 #factor calibracio
                pic_data['CO2_dry'] = (pic_data['CO2_dry'] - o_CO2_2018) / p_CO2_2018 #factor calibracion 
                pic_data['CH4_dry'] = (pic_data['CH4_dry'] - o_CH4_2018) / p_CH4_2018 #factor calibracion 

        else :
                pic_data['CO'] = (pic_data['CO'] - o_CO) / p_CO #factor calibracio
                pic_data['CO2_dry'] = (pic_data['CO2_dry'] - o_CO2) / p_CO2 #factor calibracion 
                pic_data['CH4_dry'] = (pic_data['CH4_dry'] - o_CH4) / p_CH4 #factor calibracion 

        
        #pic_data.loc[df.solenoid_valves > 0, ['CO','CO2_dry','CH4_dry','H2O']] = np.nan  values during calibration
        pic_data.CO = pic_data.CO.round(6)
        pic_data.CO2_dry = pic_data.CO2_dry.round(6)
    #pic_data.CO2_dry_G1301 = pic_data.CO2_dry_G1301.round(6)
    #pic_data.CH4_dry_G1301 = pic_data.CH4_dry_G1301.round(6)
        pic_data.CH4_dry = pic_data.CH4_dry.round(6)
        pic_data.solenoid_valves = pic_data.solenoid_valves.round(1)
    #pic_data.SD_CO = pic_data.SD_CO.round(2)
    #pic_data.SD_CO2 = pic_data.SD_CO2.round(2)
    #pic_data.SD_CH4 = pic_data.SD_CH4.round(2)
        #pic_data.WS = pic_data.WS.round(3)


    # Completo las series de tiempo
#        df_met = df_met.reindex(pd.date_range(pd.datetime(int(year), 1, 1, 0, 0), pd.datetime(int(year), 12, 31, 23, 59), freq='H'))
#
#        pic_data['F_CO'] = 0
#        pic_data['F_CO2'] = 0
#        pic_data['F_CH4'] = 0
#
#
#      # Pongo las banderas
#        pic_data.loc[(pic_data.SD_CO > max_std_co),['F_CO']] = [5] # desvio estandar alto
#        pic_data.loc[(pic_data.SD_CO2 > max_std_co2),['F_CO2']] = [5]
#        pic_data.loc[(pic_data.SD_CH4 > max_std_ch4),['F_CH4']] = [5]
#
#        pic_data.loc[(df_met.WS > max_ws) | (df_met.WS < min_ws), ['F_CO','F_CO2','F_CH4']] = [3, 3, 3]  # 3 viento bajo o muy alto
#        pic_data.loc[(df_met.WD > max_wd) | (df_met.WD < min_wd), ['F_CO','F_CO2','F_CH4']] = [2, 2, 2] #2 no background
##    pic_data.loc[np.isnan(pic_data.CO), ['F_CO']] = [5] # 5 valor de calibracion
#    pic_data.loc[np.isnan(pic_data.CO2_dry), ['F_CO2']] = [5] # 5 valor de calibracion
#    pic_data.loc[np.isnan(pic_data.CH4_dry), ['F_CH4']] = [5] # 5 valor de calibracion

    # pic_data.loc[pic_data.CO2 == -9999999.9, ['CO2','CO2_dry_Picarro']] = [-9999999.9, -9999999.9]
    #pic_data.loc[pic_data.CH4 == -9999999.9, ['CH4_dry', 'CH4_cal']] = [-9999999.9,-9999999.9]

   # if met_data.WS < min_ws:
      #  o3_data['F'] = 1

    #pic_data.loc[pic_data.ND_CO < 40, ['F_CO']] = 2  # Desabilitado para Picarro, es 2 para el caso de CO de Ushuaia
    #pic_data.loc[pic_data.ND_CO2 < 40, ['CO2_dry']] = -999999.9  # Desabilitado para Picarro, es 2 para el caso de CO de Ushuaia
    #pic_data.loc[pic_data.ND_CH4 < 40, ['CH4_dry']] = -999999.9  # Desabilitado para Picarro, es 2 para el caso de CO de Ushuaia
    # pic_data.loc[pic_data.SD_CO2 < 40, ['F_CO']] = 2  # Desabilitado para Picarro, es 2 para el caso de CO de Ushuaia
    # pic_data.loc[pic_data.SD_CH4 < 40, ['F_CO']] = 2  # Desabilitado para Picarro, es 2 para el caso de CO de Ushuaia




    # Pongo datos no validos

    #pic_data.loc[pic_data.DATE.isnull(), ['DATE', 'TIME', 'CO2_dry','CO2_dry_G1301']] = ['9999-99-99', '99:99', -9999999.9, -9999999.9]
    # met_data.loc[((met_data.WD == 0) | (np.isnan(met_data.WD))), ['WD', 'WS']] = [-99.9, -99.9]
        #pic_data.loc[(df_met.WS.isnull()) | (df_met.WD.isnull()), ['F_CO','F_CO2','F_CH4']] = [4, 4, 4] #no se las condiciones del viento
    #pic_data.loc[np.isnan(pic_data.CO), ['CO', 'ND_CO', 'SD_CO', 'F_CO']] = [-9999999.9, -9999, -99.99, -9999]
    #pic_data.loc[np.isnan(pic_data.CO2_dry), ['CO2_dry', 'CO2_dry_Picarro','ND_CO2','SD_CO2']] = [-9999999.9, -9999999.9, -9999, -99.99]
    #pic_data.loc[np.isnan(pic_data.CH4_dry), ['CH4_dry', 'ND_CH4', 'SD_CH4']] = [-9999999.9, -9999, -99.99]

    #pic_data.loc[pic_data.CO2_dry == 0, ['CO2_dry', 'ND_CO2', 'SD_CO2']] = [-9999999.9, -9999, -99.99, -9999]
    #pic_data.loc[pic_data.CH4_dry == 0, ['CH4_dry', 'ND_CH4', 'SD_CH4']] = [-9999999.9, -9999, -99.99, -9999]
    #pic_data.loc[pic_data.ND_CO2 > 60, ['ND_CO2']] = [60]
    #pic_data.loc[pic_data.ND_CH4 > 60, ['ND_CH4']] = [60]
    #o3_data.loc[np.isnan(o3_data.SD), ['SD']] = [-99.99]


    #o3_data.loc[o3_data.ND < 3, ['O3', 'ND', 'SD', 'F']] = [-9999999.9, -9999, -99.99, -9999]

    #pic_data.loc[((pic_data.CO == 0) & (pic_data.SD_CO == 0)), ['CO', 'ND_CO', 'SD_CO', 'F_CO']] = [-9999999.9, -9999, -99.99, -9999]
    #pic_data.loc[((pic_data.CO2 == 0) & (pic_data.SD_CO2 == 0)), ['CO2', 'ND_CO2', 'SD_CO2', 'F_CO2']] = [-9999999.9, -9999, -99.99, -9999]
    #pic_data.loc[((pic_data.CH4 == 0) & (pic_data.SD_CH4 == 0)), ['CH4', 'ND_CH4', 'SD_CH4', 'F_CH4']] = [-9999999.9, -9999, -99.99, -9999]




   # met_data.loc[np.isnan(met_data.RH) | np.isnan(met_data.WD), ['WD', 'WS', 'RH', 'AP', 'AT']] = [-99.9, -99.9, -99.9,
      #                                                                                             -999.9, -99.9]

    # met_data.loc[((met_data.AT < -20) | (met_data.AT > 40) | (np.isnan(met_data.AT))), ['AT']] = [-99.9] # -20 para ush
    # #met_data.loc[(met_data.AP> -900), ['AP']] = [-999.9]
    # #met_data.loc[(met_data.RH > 0), ['RH']] = [-99.9]#invalidando columna de presion
    # met_data.loc[(np.isnan(met_data.AP)), ['AP']] = [-999.9]
    # met_data.loc[(np.isnan(met_data.RH)), ['RH']] = [-99.9]


    # Promedios horarios y mensuales
    

    # Cambio formato de hora
        pic_data.index = pic_data.index.map(lambda t: t.strftime('%Y-%m-%d %H:%M'))
    # met_data.index = met_data.index.map(lambda t: t.strftime('%Y-%m-%d %H:%M'))
    # o3_data_D.index = o3_data_D.index.map(lambda t: t.strftime('%Y-%m-%d %H:%M'))

    # o3_data_M.index = o3_data_M.index.map(lambda t: t.strftime('%Y-%m-%d %H:%M'))
        if estacion == 'Ushuaia':

                if year == 2017:
                    pic_data.loc[pic_data.index[11:2987:24], ['F_CO','F_CO2', 'F_CH4']] = 6 # calibraciones del horiba 
     
                    pic_data.loc[pic_data.index[2988:4788:24],['F_CO','F_CO2', 'F_CH4']] = 6
    
                    pic_data.loc[pic_data.index[4789:8175:24],['F_CO','F_CO2', 'F_CH4']] = 6
    
    
                    pic_data.loc[pic_data.index[8176:8784:24], ['F_CO','F_CO2', 'F_CH4']] = 6


                    pic_data.loc[pic_data.index[16:1573:24], ['F_CO','F_CO2', 'F_CH4']] = 6
                    pic_data.loc[pic_data.index[1574:3782:24], ['F_CO','F_CO2', 'F_CH4']] = 6
                    pic_data.loc[pic_data.index[3783:5415:24], ['F_CO','F_CO2', 'F_CH4']] = 6
                    pic_data.loc[pic_data.index[5416:8761:24], ['F_CO','F_CO2', 'F_CH4']] = 6
     
                if year == 2018:
                    pic_data.loc[pic_data.index[16:1536:24], ['F_CO','F_CO2', 'F_CH4']] = 6
                    pic_data.loc[pic_data.index[1550:3760:24], ['F_CO','F_CO2', 'F_CH4']] = 6
                    pic_data.loc[pic_data.index[3759:5372:24], ['F_CO','F_CO2', 'F_CH4']] = 6
                    pic_data.loc[pic_data.index[5392:8755:24], ['F_CO','F_CO2', 'F_CH4']] = 6

#    co_data_D = process_daily(co, year)
#    co_data_M = process_monthly(co, year)
    pic_h = process_hourly(pic_data)                


    return pic_data, pic_h #co_data_D, co_data_M

def process_hourly(pic_data):
    pic_h =pd.DataFrame()
    
    pic_h['CO'] = pic_data.CO.resample('H').mean()
    
    pic_h['CO2_dry'] = pic_data.CO2_dry.resample('H').mean()
    pic_h['CH4_dry'] = pic_data.CH4_dry.resample('H').mean()
    pic_h['H2O'] = pic_data.H2O.resample('H').mean()
    
    return pic_h
    
def process_daily(o3_data, year):
    o3_data_D = pd.DataFrame()

    # Datos de Ozono
    o3_data_D['DATE'] = '9999-99-99'
    o3_data_D['TIME'] = '99:99'
    o3_data_D['CO'] = o3_data.CO[o3_data.F != 2 ].resample('D', how='mean')
    o3_data_D['ND'] = o3_data.ND[o3_data.F != 2 ].resample('D', how='count')
    o3_data_D['SD'] = o3_data.SD[o3_data.F != 2 ].resample('D', how=np.std)
    o3_data_D['F'] = -999.999

    o3_data_D.CO = o3_data_D.CO.round(3)
    o3_data_D.SD = o3_data_D.SD.round(2)

    o3_data_D = o3_data_D.reindex(
        pd.date_range(pd.datetime(int(year), 1, 1, 0, 0), pd.datetime(int(year), 12, 31, 23, 59), freq='D'))

    #f0 = o3_data.CO[o3_data.F == 0].resample('D', how='count')
    f1 = o3_data.CO[o3_data.F == 1].resample('D', how='count')
    #f2 = o3_data.CO[o3_data.F == 2].resample('D').count()

    o3_data_D.loc[f1 > 9, 'F'] = [1]
    o3_data_D.loc[f1 <= 9, ['F']] = 0


    o3_data_D.loc[o3_data_D.ND < 15, ['F']] = [2]
    o3_data_D.loc[np.isnan(o3_data_D.CO), ['DATE', 'TIME', 'CO', 'ND', 'SD', 'F']] = ['9999-99-99', '99:99', -999.999, -9, -999.999, 2]


    return o3_data_D


def process_monthly(o3_data, year):
    o3_data_M = pd.DataFrame()

    # Datos de Ozono
    o3_data_M['DATE'] = '9999-99-99'
    o3_data_M['TIME'] = '99:99'
    o3_data_M['CO'] = o3_data.CO[o3_data.F != 2].resample('MS', how='mean')
    o3_data_M['ND'] = o3_data.ND[o3_data.F != 2].resample('MS', how='count')
    o3_data_M['SD'] = o3_data.SD[o3_data.F != 2].resample('MS', how=np.std)
    o3_data_M['F'] = -999.999
  

    o3_data_M.CO = o3_data_M.CO.round(3)
    o3_data_M.SD = o3_data_M.SD.round(2)

    o3_data_M = o3_data_M.reindex(
        pd.date_range(pd.datetime(int(year), 1, 1, 0, 0), pd.datetime(int(year), 12, 31, 23, 59), freq='MS'))

    o3_data_M.loc[np.isnan(o3_data_M.CO), ['DATE', 'TIME', 'CO', 'ND', 'SD', 'F']] = ['9999-99-99', '99:99', -999.999, -9, -999.999, 2]

    f1 = o3_data.CO[o3_data.F == 1].resample('MS', how='count')

    o3_data_M.loc[f1 > 240, 'F'] = [1]
    o3_data_M.loc[f1 <= 240, ['F']] = 0

    o3_data_M.loc[o3_data_M.ND < 16, ['F']] = [ 2]

    #o3_data_M.loc[np.isnan(o3_data_M.SD), ['SD']] = [-99.99]

    return o3_data_M


def save_data(pic_data, hourly):
    f = open(dir_root + '{}_{}_{}.dat'.format(instrument,estacion, year), 'wt')
    f.write(pic_data.to_string())
    f.close()

    f = open(dir_root + 'hourly_{}_{}_{}.dat'.format(instrument,estacion, year), 'wt')
    f.write(hourly.to_string())
    f.close()

#    f = open(dir_root + 'CO_D{0}Ushuaia.dat'.format(year), 'wt')
#    f.write(o3_data_D.to_string())
#    f.close()
#    
#    f = open(dir_root + 'CO_M{0}Ushuaia.dat'.format(year), 'wt')
#    f.write(o3_data_M.to_string())
#    f.close()

    return


def main():
    usagestr = "\n\t%prog [options]" \
               "\nProcesador de los datos de Ozono superficial.\n" \
               "(Ver las opciones usando: --help)"

    parser = OptionParser(usage=usagestr, version=VERSIONSTR)
    parser.add_option("-i", "--input", dest="inputdir", default=INPUTDIR,
                      help="Directorio de entrada ,default:%s" % INPUTDIR)
    parser.add_option("-o", "--output", dest="outputdir", default=OUTPUTDIR,
                      help="Directorio de salida ,default:%s" % OUTPUTDIR)
    parser.add_option("-y", "--year", dest="year", default= year, help="Año de datos a procesar, default:")
    parser.add_option("-s", "--station", dest="station", default="lqi",
                      help="Estacion a procesar (mbi, lqi, sju, pil), default:mbi") 
    parser.add_option("-f", "--format", dest="format", default="nuevo",
                      help="Formato de los archivos 'viejo' o 'nuevo', default: nuevo")
    (opts, args) = parser.parse_args()
    parser.print_usage()

    print("Directorio de entrada:", opts.inputdir)
    print("Directorio de salida :", opts.outputdir)
    print("Año a procesar       :", opts.year)
    print("Estacion             :", opts.station)
    print("Formato              :", opts.format)

    if opts.station == 'mbi':
        max_std = 1.75
        min_ws = 2
        max_ws = 20
        max_wd = 90
    if opts.station == 'pil':
        max_std = 2
        min_ws = 2
        max_ws = 20
        max_wd = 0
    if opts.station == 'sju':
        max_std = 2
        min_ws = 2
        max_ws = 20
        max_wd = 0
    if opts.station == 'lqi':
        # a = input("Ingrese pendiente de calibracion")
        # b = input("Ingrese ordenada al origen de calibracion")
        max_std_co = 60 #1.75  cambio provisorio para el proceso de co
        max_std_co2 = 30
        max_std_ch4 =0.1
        min_ws = 3 # 1 para picarro en ush
        max_ws = 40
        max_wd = 270
        min_wd = 90

    # Cargo todos los archivos en memoria
    if opts.station == 'mbi':
        df_data, df_met = load_mbi_file(opts.inputdir, opts.year)
    elif opts.format != 'nuevo':
        df_data, df_met = load_old_files(opts.inputdir, opts.year)
    else:
        df, df_met = load_new_files(input_dir,INPUTDIR, year)

    # Proceso los datos
    pic_h, pic_data = process_data(df, df_met, max_std_co, max_std_co2, max_std_ch4, min_ws, max_ws,min_wd, max_wd, year, instrument)
    

    # Guardo los datos
    save_data(pic_data, pic_h)

    print('PF')


if __name__ == "__main__":  # if not a module, execute main()
    main()