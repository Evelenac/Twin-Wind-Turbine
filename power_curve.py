# -*- coding: utf-8 -*-
"""
Basic power curve for a single turbine from the Engie Green SCADA database

Created on Wed Jan 19 13:56:13 2022

@author: des0pcm
"""

import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Set up SQL connection

conn = pymysql.connect(host = "open-energy.durham.ac.uk", 
                       user = "browser",
                       password = "curious",
                       database = "EngieGreen")

# The SQL query...

# sql = "SELECT Wind_turbine_name, Date_time, Ws_avg, P_avg from LHB WHERE Wind_turbine_name='R80711'"
# print(sql)

# # Do it, and put the results into a DataFrame (20220119: est time 1 min)

# data = pd.read_sql(sql, conn)

# data.to_pickle('wind_turbine1.pickle')

data = pd.read_pickle('wind_turbine1.pickle')

data_new = data.groupby(data["Date_time"].dt.date).mean()

data_new = data_new.reset_index()
print(data_new)

# Plot the power curve scatter plot

plt.figure(figsize=(13, 10))
plt.plot(data_new["Date_time"],data_new["Ws_avg"],'.')
plt.ylabel('Wind Speed (m/s)')
plt.xlabel('Date')
plt.savefig('speed_vs_date.png')

plt.figure(figsize=(13, 10))
plt.plot(data_new["Date_time"],data_new["P_avg"],'.')
plt.ylabel('Power (kW)')
plt.xlabel('Date')
plt.savefig('power_vs_date.png')


def power_of_wind(v,rho,r):

    power = (1/2)*rho*v**3*np.pi*r**2/1000
    
    return power

popt, _ = curve_fit(power_of_wind, data_new["Ws_avg"], data_new["P_avg"])

rho,r = popt

x_line = np.linspace(min(data_new["Ws_avg"]), max(data_new["Ws_avg"]), 1000)

y_line = power_of_wind(x_line,rho,r)

plt.figure(figsize=(13, 10))
plt.plot(data_new["Ws_avg"],data_new["P_avg"],'.')
plt.plot(x_line,y_line)
plt.ylabel('Power (kW)')
plt.xlabel('Wind Speed (m/s)')
plt.savefig('power_vs_speed.png')