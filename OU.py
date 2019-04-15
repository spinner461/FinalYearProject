import numpy as np 
from matplotlib import pyplot as plt

def OU_motion(t,dt,tau,sigma,initial_value):
    
    values = []
    timesteps = list(np.arange(0,t,dt))
    for i,ti in enumerate(timesteps):
        B = np.sqrt(dt)*np.random.normal(0.0,1)
        if i == 0:
            value = initial_value
        else:
            value = values[i-1] + dt*(values[i-1])*(-1/tau) + (sigma/np.sqrt(tau))*B
        values.append(value) 
        
    return values

def monte_carlo_OU(t,dt,tau,sigma,initial_value,n):
    OU_array = []
    average_path = []
    timesteps = list(np.arange(0,t,dt))
    std_vals = [] 
    squared_vals2 = []
    for i in np.arange(0,n,1):
        OU_array.append(OU_motion(t,dt,tau,sigma,initial_value))
    for step in np.arange(0,len(timesteps)):
        vals = []
        squared_vals = []
        for i in range(len(OU_array)):
            vals.append(OU_array[i][step])
            squared_vals.append((OU_array[i][step])**2)
        expected_val = np.average(vals)
        std = np.sqrt(np.average((np.array(vals)-expected_val)**2))
        average_path.append(expected_val)
        squared_vals2.append(np.mean(squared_vals))
        std_vals.append(std)
    sigmaplus = np.array(average_path) + np.array(std_vals)
    sigmaminus = np.array(average_path) - np.array(std_vals) 

    plt.figure(1)
    plt.title("Ornstein-Uhlenbeck ")
    plt.ylabel("X(t)")
    plt.xlabel("Time")
    plt.scatter(timesteps,average_path, color = 'gray', label = 'Average', s=0.1)
    plt.scatter(timesteps,sigmaplus, color = 'tomato', label = 'Average + σ(t)',s=0.1)
    plt.scatter(timesteps,sigmaminus, color = 'darkturquoise', label = 'Average - σ(t) ',s=0.1)
    plt.legend()

    plt.figure(2)
    plt.title("Ornstein-Uhlenbeck")
    plt.ylabel("X(T)")
    plt.xlabel("Time")
    plt.scatter(timesteps,average_path, s = 0.1, color = 'gray')
    
    plt.figure(3)
    plt.title("Average Value of X^2 vs Time")
    plt.ylabel("<X^2>")
    plt.xlabel("Time")
    plt.scatter(timesteps,squared_vals2,color = 'gray',s=0.1)
    plt.show()
    
def main():
    tau = float(input("Please enter a tau value: "))
    sigma = float(input("Please enter a sigma value: "))
    t = float(input("Please enter a total t value: "))
    dt = float(input("Please enter a time step value: "))
    n = float(input("Please enter a number of trials: "))
    monte_carlo_OU(t,dt,tau,sigma,0,n)

main()
            
            
            
            