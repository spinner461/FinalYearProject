from Simulation import stock_price as stock_price, euler_method, milstein_method
import numpy as np
import requests
import pandas as pd
import datetime as datetime
import time
from random import randint 
from matplotlib import pyplot as plt
colours = ['blue','green','red','yellow','cyan','pink','orange','magenta']


def get_key(query):   
    search_symbol = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+query+'&apikey=B14MESKOADFX3X24')
    search_symbol = search_symbol.json() 
    search_symbol= search_symbol['bestMatches']
    df1 = pd.DataFrame(columns = ['','symbol','name','type','region','marketOpen','MarketClose','TimeZone','Currency','MatchScore'])
    for p in search_symbol:
        data_row= ['',str(p['1. symbol']),str(p['2. name']),str(p['3. type']),str(p['4. region']),str(p['5. marketOpen']),str(p['6. marketClose']),str(p['7. timezone']),str(p['8. currency']),str(p['9. matchScore'])]
        df1.loc[-1,:]=data_row
        df1.index=df1.index+1
    df1= df1.sort_values('MatchScore',ascending=False)
    df1.to_string(index = False)
    index = len(df1)-1
    #print(df1)
    #print(df1.loc[index]['name'],df1.loc[index]['symbol'])
    #print('The currency is:',df1.loc[index]['Currency'] )
    return(df1.loc[index])

def get_stock_data(key_data,timestep):
    
    if timestep == '60min':
        web_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+key_data['symbol']+'&interval=60min&outputsize=full&apikey=B14MESKOADFX3X24')
    elif timestep == '30min':
        web_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+key_data['symbol']+'&interval=30min&outputsize=full&apikey=B14MESKOADFX3X24')
    elif timestep == '15min':
        web_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+key_data['symbol']+'&interval=15min&outputsize=full&apikey=B14MESKOADFX3X24')
    elif timestep == 'Daily':
        web_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_Daily&symbol='+key_data['symbol']+'&outputsize=full&apikey=B14MESKOADFX3X24')
    else: 
        print('Sorry this is not a valid option')
        return ''
    data= web_data.json()
    data_key = 'Time Series (' + str((timestep))+')'
    data= data[data_key]
    df = pd.DataFrame(columns = ['date','open','high','low','close','volume'])
    for d,p in data.items():
        if timestep == 'Daily':
            date= datetime.datetime.strptime(d,'%Y-%m-%d')
        else:
            date= datetime.datetime.strptime(d,'%Y-%m-%d %H:%M:%S')
        data_row= [date,float(p['1. open']),float(p['2. high']),float(p['3. low']),float(p['4. close']),float(p['5. volume'])]
        df.loc[-1,:]=data_row
        df.index=df.index+1
    df= df.sort_values('date')
    return df

def plot_historical(data,key,timestep):
    timestamp_values = []
    data_dict = {}
    if timestep == 'Daily':
        first_timestamp = time.mktime(datetime.datetime.strptime(str(data.loc[0]['date']),'%Y-%m-%d %H:%M:%S').timetuple())
        for date in data['date']:
            timestamp = time.mktime(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').timetuple())
            timestamp_values.append(timestamp-first_timestamp)
    else:
       first_timestamp = time.mktime(datetime.datetime.strptime(str(data.loc[0]['date']),'%Y-%m-%d %H:%M:%S').timetuple())     
       for date in data['date']:
            timestamp = time.mktime(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').timetuple())
            timestamp_values.append(timestamp-first_timestamp)
    time_stamp_days = [x/ 86400 for x in timestamp_values]
    dt = time_stamp_days[2]-time_stamp_days[1]
    data_dict['time step'] = dt
    data_dict['time'] = time_stamp_days
    return data_dict
     
    
def compute_values(data,dt): #This is for using the entire data set and calculating sigma and mu'
    values = {}
    expected_value = np.mean(data['close'])
    deviation = 0
    for i in data['close']:
        deviation += (i - expected_value)**2
    values['mu'] = ((np.log(expected_value) - np.log(data['close'][0]))/(len(data['close'])*dt))        
    values['sigma'] = np.sqrt(deviation/len(data['close']))        
    
    return values

def moving_average_values(data,N,dt):
    values = {}
    sigma = []
    mu = []
    recent_mu = [] 
    recent_sigma = []
    deviation2 = [] 
    recent_group = list(data[len(data)-N:])
    total_expected_value = np.mean(list(data))
    mu.append((np.log(list(data)[-1]) - np.log(list(data)[0]))/(len(data)*dt))
    for i in data:
        deviation2.append(abs((i - total_expected_value)**2))
    variance2 = np.mean(deviation2)
    sigma.append(np.sqrt(np.log((variance2/((total_expected_value)**2))+1)/(len(data)*dt)))
    expected_value = np.mean(recent_group)
    recent_mu.append((np.log(recent_group[-1]) - np.log(recent_group[0]))/(len(recent_group)*dt))
    deviation = []
    for element in recent_group:
            deviation.append(abs((element - expected_value)**2))
    variance = np.mean(deviation)
    recent_sigma.append(np.sqrt(np.log((variance/((expected_value)**2))+1)/(len(recent_group)*dt)))
    values['mu'] = np.mean(mu)
    values['sigma'] = np.mean(sigma)
    values['mu2'] = recent_mu[0]
    values['sigma2'] = recent_sigma[0]
    return values
    
def monte_carlo(n,t,dt,price_initial,sigma,mu):
    monte_carlo_data ={}
    time = list(np.arange(0,t,dt))
    
    analytical_data = []
    euler_data = [] 
    milstein_data = []
    resultant_values = []  
    
    analytical_expected_path = []
    euler_expected_path = []
    milstein_expected_path = [] 
    
    for i in np.arange(0,n,1):
        analytical = stock_price(t,dt,price_initial,sigma,mu)
        euler = euler_method(t,dt,price_initial,sigma,mu)
        milstein = milstein_method(t,dt,price_initial,sigma,mu)
        
        analytical_data.append(list(analytical['values']))
        euler_data.append(euler['values'])
        milstein_data.append(milstein['values'])
        resultant_values.append(analytical['values'][len(analytical['values'])-1])
    
    for time_step in np.arange(0,len(time),1):
        analytical_values = []    
        euler_values = []    
        milstein_values = []    
        for data in analytical_data:
            analytical_values.append(data[time_step])
        analytical_expected_path.append(np.mean(analytical_values))
        for data in euler_data:
            euler_values.append(data[time_step])
        euler_expected_path.append(np.mean(euler_values))
        for data in milstein_data:
            milstein_values.append(data[time_step])
        milstein_expected_path.append(np.mean(milstein_values))
            
    margin_of_error = 1.959964 * (np.std(resultant_values)/len(resultant_values))
    monte_carlo_data['Error'] = margin_of_error
    monte_carlo_data['Analytical'] = analytical_expected_path
    monte_carlo_data['Euler'] = euler_expected_path
    monte_carlo_data['Milstein'] = milstein_expected_path
    monte_carlo_data['time'] = time
    monte_carlo_data['Analytical paths'] = analytical_data
       
    return monte_carlo_data
    

        
def main(query,f):
    html = {}
    timestep = "Daily"
    key_data = get_key(query)
    data = get_stock_data(key_data,timestep)
    time_data = plot_historical(data,key_data,timestep)
    parameters1 = moving_average_values(data['close'][0:len(data['close'])-(f)],len(data['close']),1)
    parameters2 = moving_average_values(data['close'][0:len(data['close'])-(f)],7,1)
    parameters3 = moving_average_values(data['close'][0:len(data['close'])-(f)],14,1)
    parameters4 = moving_average_values(data['close'][0:len(data['close'])-(f)],21,1)


    time_interval = f
    prediction1 = monte_carlo(1500,time_interval,1,data['close'][len(data['close'])-(f)],parameters1['sigma'],parameters1['mu'])
    prediction2 = monte_carlo(1500,time_interval,1,data['close'][len(data['close'])-(f)],parameters2['sigma2'],parameters2['mu2'])
    prediction3 = monte_carlo(1500,time_interval,1,data['close'][len(data['close'])-(f)],parameters3['sigma2'],parameters3['mu2'])
    prediction4 = monte_carlo(1500,time_interval,1,data['close'][len(data['close'])-(f)],parameters4['sigma2'],parameters4['mu2'])
    prediction2['time'] = [(time_data['time'][-1]-f)+ x for x in prediction2['time']]
    prediction3['time'] = [(time_data['time'][-1]-f)+ x for x in prediction3['time']]
    
    
    final_index = time_data['time'].index(prediction2['time'][-1])
    plt.figure(1)
    plt.title('Historical data of '+key_data['name']) 
    plt.plot(time_data['time'],data['close'],label = 'Historical', color = 'black')
    plt.plot(time_data['time'][len(time_data['time'])-f:],prediction1['Analytical'],label= 'Total average',color = 'red')
    plt.plot(time_data['time'][len(time_data['time'])-f:],prediction2['Analytical'],label= '1 - week',color = 'blue')
    plt.plot(time_data['time'][len(time_data['time'])-f:],prediction3['Analytical'],label= '2 - weeks',color = 'cyan')
    plt.plot(time_data['time'][len(time_data['time'])-f:],prediction4['Analytical'],label= '3 - weeks ',color = 'magenta')
    plt.xlabel('Time in Days')
    plt.ylabel('Closing Stock Value')
    plt.legend()
    plt.show()
    #print("95% confidence interval range: [{},{}]".format(
								#round(prediction['Analytical'][-1] - prediction['Error'],2), round(prediction['Analytical'][-1] + prediction['Error'],2)))
    #print('The expected value with last calulated mu/sigma is: ', round(prediction1['Analytical'][-1],2))
    #print("95% confidence interval range: [{},{}]".format(
								#round(prediction1['Analytical'][-1] - prediction1['Error'],2), round(prediction1['Analytical'][-1] + prediction1['Error'],2)))
    html['name'] = key_data['name']
    html['prediction1'] = prediction1
    html['prediction2'] = prediction2
    html['prediction3'] = prediction3
    html['prediction4'] = prediction4
    html['Time Data'] = time_data
    html['Historical'] = data['close']
    #html['sigma1'] =  round(parameters['sigma'],5)
    #html['mu1'] = round(parameters['mu'],5)
    #html['sigma2'] = round(parameters['sigma2'],5)
    #html['mu2'] = round(parameters['mu2'],5)
    html['sigma3'] =  round(parameters2['sigma'],5)
    html['mu3'] = round(parameters2['mu'],5)
    #html['CI1'] = str("95% confidence interval range: [{},{}]".format(
	#							round(prediction['Analytical'][-1] - prediction['Error'],2), round(prediction['Analytical'][-1] + prediction['Error'],2)))
    #html['CI2'] = str("95% confidence interval range: [{},{}]".format(
	#							round(prediction2['Analytical'][-1] - prediction2['Error'],2), round(prediction2['Analytical'][-1] + prediction2['Error'],2)))
    html['historical_forecast'] = [prediction2['Analytical'][-1],data.loc[final_index]['close'],data.loc[final_index-f]['close']]
    html['days'] = f
    
    return html 

def app():
    key = str(input("Please enter the name of the company you would like to analyse: "))
    days = int(input("Please enter the number of days from where you would like to forecast from (N): "))
    data = main(key,days)
    
    print("Results for Total Average")
    print("The expected value was:",round(data['prediction1']['Analytical'][-1],2))
    print("The actual value was:",round(data['historical_forecast'][1],2))
    print("The magnitude of error between them is:", round(abs(data['prediction1']['Analytical'][-1]-data['historical_forecast'][1])))
    print("The percentage error between them is: ",round(((abs(data['prediction1']['Analytical'][-1]-data['historical_forecast'][1]))/data['historical_forecast'][1]),2)) 
    print("The expected growth was: ",round(data['prediction1']['Analytical'][-1]-data['prediction1']['Analytical'][0],2))
    print("The actual growth was: ",round(data['historical_forecast'][1]-data['historical_forecast'][2],2))
    error_in_growth = abs((data['prediction1']['Analytical'][-1]-data['prediction1']['Analytical'][0])-(data['historical_forecast'][1]-data['historical_forecast'][2]))
    error_in_growth_percent = (error_in_growth/(data['historical_forecast'][1]-data['historical_forecast'][2]))*100
    print("The error in growth was: ", round(error_in_growth,2))
    print("The percentage error in growth was: ", round(error_in_growth_percent,2))
    print("     ")

    print("Results for 1 week forecast")
    print("The expected value was:",round(data['prediction2']['Analytical'][-1],2))
    print("The actual value was:",round(data['historical_forecast'][1],2))
    print("The magnitude of error between them is:", round(abs(data['prediction2']['Analytical'][-1]-data['historical_forecast'][1])),2)
    print("The percentage error between them is: ",round(((abs(data['prediction2']['Analytical'][-1]-data['historical_forecast'][1]))/data['historical_forecast'][1])*100,2)) 
    print("The expected growth was: ",round(data['prediction2']['Analytical'][-1]-data['prediction2']['Analytical'][0],2))
    print("The actual growth was: ",round(data['historical_forecast'][1]-data['historical_forecast'][2],2))
    error_in_growth = abs((data['prediction2']['Analytical'][-1]-data['prediction2']['Analytical'][0])-(data['historical_forecast'][1]-data['historical_forecast'][2]))
    error_in_growth_percent = (error_in_growth/(data['historical_forecast'][1]-data['historical_forecast'][2]))*100
    print("The error in growth was: ", round(error_in_growth,2))
    print("The percentage error in growth was: ", round(error_in_growth_percent,2))
    print("     ")
   
    print("Results for 2 week forecast")
    print("The expected value was:",round(data['prediction3']['Analytical'][-1],2))
    print("The actual value was:",round(data['historical_forecast'][1],2))
    print("The magnitude of error between them is:", round(abs(data['prediction3']['Analytical'][-1]-data['historical_forecast'][1]),2))
    print("The percentage error between them is: ",round(((abs(data['prediction3']['Analytical'][-1]-data['historical_forecast'][1]))/data['historical_forecast'][1])*100,2)) 
    print("The expected growth was: ",round(data['prediction3']['Analytical'][-1]-data['prediction3']['Analytical'][0],2))
    print("The actual growth was: ",round(data['historical_forecast'][1]-data['historical_forecast'][2],2))
    error_in_growth = abs((data['prediction3']['Analytical'][-1]-data['prediction3']['Analytical'][0])-(data['historical_forecast'][1]-data['historical_forecast'][2]))
    error_in_growth_percent = (error_in_growth/(data['historical_forecast'][1]-data['historical_forecast'][2]))*100
    print("The error in growth was: ", round(error_in_growth,2))
    print("The percentage error in growth was: ", round(error_in_growth_percent,2))
    print("     ")
    
    
    print("Results for 3 week forecast")
    print("The expected value was:",round(data['prediction4']['Analytical'][-1],2))
    print("The actual value was:",round(data['historical_forecast'][1],2))
    print("The magnitude of error between them is:", round(abs(data['prediction4']['Analytical'][-1]-data['historical_forecast'][1]),2))
    print("The percentage error between them is: ",round(((abs(data['prediction4']['Analytical'][-1]-data['historical_forecast'][1]))/data['historical_forecast'][1])*100),2) 
    print("The expected growth was: ",round(data['prediction4']['Analytical'][-1]-data['prediction4']['Analytical'][0],2))
    print("The actual growth was: ",round(data['historical_forecast'][1]-data['historical_forecast'][2],2))
    error_in_growth = abs((data['prediction4']['Analytical'][-1]-data['prediction4']['Analytical'][0])-(data['historical_forecast'][1]-data['historical_forecast'][2]))
    error_in_growth_percent = (error_in_growth/(data['historical_forecast'][1]-data['historical_forecast'][2]))*100
    print("The error in growth was: ", round(error_in_growth,2))
    print("The percentage error in growth was: ", round(error_in_growth_percent,2))
    print("     ")
    
    
app()