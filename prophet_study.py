import pandas as pd
from prophet import Prophet

data = pd.read_pickle('wind_turbine1.pickle')

data_new = data[["Date_time","Ws_avg"]]

data_new = data_new.rename(columns={"Date_time":"ds","Ws_avg":"y"})

m = Prophet()

m.fit(data_new)
future = m.make_future_dataframe(periods=365)


forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)

fig1.write_image("forecast.png")
fig2.write_image("components.png")