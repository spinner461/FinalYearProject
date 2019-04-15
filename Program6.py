import numpy as np 
import random 
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

def main():
    colours = ['blue','green','red','yellow','black','orange','magenta']
    mu = float(input("Please get enter a mu value: "))
    sigma = float(input("Please get enter a sigma value: "))
    t = float(input("Please enter a total time value: "))
    dt = float(input("Please enter a time-step value: "))
    n = float(input("Please enter a number of paths (n): "))
    price_initial = float(input("Please enter an initial value: "))
    plt.figure(1)
    plt.ylabel("X(t)")
    plt.xlabel("Time")
    plt.title("Geometric Brownian Motion σ = "+ str(sigma) + " µ = " + str(mu))
    final_values = []
    for i in np.arange(0,n,1):
        data = stock_price(t,dt,price_initial,sigma,mu)
        final_values.append(data['values'][-1])
        plt.plot(data['time'],data['values'],color = colours[random.randint(0,6)])
        
    plt.show()
    print("The expected value is:", round(np.mean(final_values),2))
    print("The variance is: ", round(np.var(final_values),2))
main()