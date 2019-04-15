import numpy as np 
from random import randint
from matplotlib import pyplot as plt

def stock_price(t,dt,price_initial,sigma,mu):   
    stock_dict = {}
    t_values = [0]
    prices = []
    mean = (mu-(sigma**2)/2)*dt 
    for i in np.arange(0,t,dt):
        if i == 0:
            price = price_initial
        else:
            B = np.sqrt(dt)*np.random.normal(0.0,1)
            variance = sigma*B
            price = price_initial*np.exp(mean)*np.exp(variance)
            t_values.append(i)
        prices.append(price)
        price_initial = price
    stock_dict['time'] = t_values
    stock_dict['values'] = prices
    
    return stock_dict

def arithmetic_brownian_motion(t,dt,price_initial):
    mean = 0.1
    results = {}
    x_values = []
    t_values = [] 
    for i in np.arange(0,t,dt):   
        sigma = dt
        B = np.random.normal(0.0,dt)
        value = price_initial + mean*i + sigma*B
        t_values.append(i)
        x_values.append(value)
        
    results['time'] = t_values
    results['values'] = x_values
    
    return results 

def compare_mu_vals(gbm_array,dt,print_res=False):
	computed_mu_vals = []
	for step in range(1,len(np.arange(0,t,dt))):
		vals = []
		for i in np.arange(0,len(gbm_array),1):
            
			vals.append(gbm_array[i][step])
            
		expected_val = np.average(vals)
		computed_mu_vals.append( (np.log(expected_val) - np.log(price_initial)) / (step*dt) )
	computed_mu = np.mean(computed_mu_vals)
	rel_error = round(100*(abs(mue-computed_mu)/mue),4)
	compared_mu_vals = {
						'computed_mu_vals':computed_mu_vals, # can also get list of mu relative errors
						'mu':computed_mu,
						'rel_error':rel_error,
						}

	return compared_mu_vals
	
		
def compare_sigma_vals(gbm_array,dt,print_res=False):
	computed_sigma_vals = []
	for step in np.arange(1,len(np.arange(0,t,dt))):
		vals = []
		for i in range(len(gbm_array)):
			vals.append(gbm_array[i][step])
		expected_val = np.average(vals)
		variance = np.var(vals)
		computed_sigma_vals.append(np.sqrt(np.log((variance/((expected_val)**2))+1)/(step*dt)))
	computed_sigma = np.mean(computed_sigma_vals)
	rel_error = round(100*(abs(sigma-computed_sigma)/sigma),4)
	compared_sigma_vals = {
							'computed_sigma_vals':computed_sigma_vals,
							'sigma':computed_sigma,
							'rel_error':rel_error,
							}
	
	return compared_sigma_vals

    
def euler_method(t,dt,price_initial,sigma,mu):
    data_dict2 = {}
    values = []
    time = list(np.arange(0,t,dt))
    
    for i in np.arange(0,t,dt):
        j = time.index(i)
        B = np.sqrt(dt)*np.random.normal(0.0,1)
        if j == 0:
            price = price_initial
        else:
            price = values[j-1] + dt*(values[j-1]*mu) + (values[j-1]*sigma)*B
        values.append(price)
    data_dict2['values'] = values
    data_dict2['time'] = time
    
    return data_dict2

def milstein_method(t,dt,price_initial,sigma,mu):
    
    data_dict3 = {}
    values = []
    time = list(np.arange(0,t,dt))
    
    for i in np.arange(0,t,dt):
        j = time.index(i)
        B = np.sqrt(dt)*np.random.normal(0.0,1)
        if j == 0:
            price = price_initial
        else:
            price = values[j-1] + dt*(values[j-1]*mu) + (values[j-1]*sigma)*B + (1/2)*(values[j-1]*sigma)*(sigma)*(B**2 -dt)
        values.append(price)
    data_dict3['values'] = values
    data_dict3['time'] = time
    return data_dict3

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
    

    
    

