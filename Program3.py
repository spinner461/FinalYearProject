import numpy as np 
import random
from matplotlib import pyplot as plt

def arithmetic_brownian_motion(t,dt,mu,sigma,price_initial):
    results = {}
    x_values = [price_initial]
    t_values = [0] 
    for i in np.arange(0+dt,t,dt):   
        sigma = sigma
        B = np.sqrt(i)*np.random.normal(0.0,1)
        value = price_initial + mu*i + sigma*B
        t_values.append(i)
        x_values.append(value)
    results['time'] = t_values
    results['values'] = x_values
    
    return results 

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
    plt.title("Arithmetic Brownian Motion σ = "+ str(sigma) + " µ = " + str(mu))
    final_values = []
    for i in np.arange(0,n,1):
        data = arithmetic_brownian_motion(t,dt,mu,sigma,price_initial)
        final_values.append(data['values'][-1])
        plt.plot(data['time'],data['values'],color = colours[random.randint(0,6)])
        
    plt.show()
    print("The expected value is:", round(np.mean(final_values),2))
    print("The variance is: ", round(np.var(final_values),2))
main()