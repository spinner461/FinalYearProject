import numpy as np 
from matplotlib import pyplot as plt
import math

def random_walk(n,z):
    steps = np.random.choice([-1,1],n,p =[(1-z),(z)])
    final = sum(steps)
    return final

def bi_co(n,k): # BinomialCoeffecient .
    m = math.factorial(n)
    b = math.factorial(n-k)
    r = math.factorial(k)
    
    return m/(r*b)     

def monte_carlo(trials,n,p):
    final_values = []
    for i in np.arange(0,trials,1):
        final_values.append(random_walk(n,p))

    return final_values

def probability(n,p): # This is my probability density function for n,k,p and q. 
    k_vals =[]
    prob_vals = [] 
    p = p
    q = 1-p
    for k in range(-n,n,2):
        n_plus = (n+k)/2
        n_minus = (n-k)/2
        prob = ( bi_co(n,(n+k)/2) ) * (p**n_plus)*(q**n_minus)
        k_vals.append(k)
        prob_vals.append(prob)
        
    return k_vals,prob_vals

def graph(data,expected,n):
    plt.figure(1)
    plt.title("Frequency Distribution")
    plt.ylabel("Frequency")
    plt.xlabel("Distance from x = 0")
    bin_widths = int(round(np.sqrt(n)))
    plt.hist(data, bins= bin_widths,label = "Actual Distribution")
    plt.plot(expected[0],expected[1], "r--", label = "Expected Distribution")
    plt.legend()
    plt.show()
    


def main():
    trial_no = int(input("Please enter the number of trials you would like to run: "))
    number_of_steps = int(input("Please enter the number of steps the particle will take: "))
    p = float(input("Please enter the probability of the particle moving to the right: "))
    real_trial = monte_carlo(trial_no,number_of_steps,p)
    probabilities = probability(number_of_steps,p)
    expected_frequencies = []
    for i in probabilities[1]:
        expected_frequencies.append(i*trial_no)
    expected_results = [probabilities[0],expected_frequencies]
    graph(real_trial,expected_results,trial_no)
    print("The expected value is: ", round(np.mean(real_trial),1))
    print("The variance of the sample is: ", round(np.var(real_trial),1))
    
main()