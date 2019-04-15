import math
from matplotlib import pyplot as plt

def bi_co(n,k): # BinomialCoeffecient .
    m = math.factorial(n)
    b = math.factorial(n-k)
    r = math.factorial(k)
    
    return m/(r*b)      

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

def main():    
    n1 = int(input('Please enter your first value of n: ')) 
    n2 = int(input('Please enter your second value of n: ') )
    n3 = int(input('Please enter your third value of n: ') )
    n4 = int(input('Please enter your fourth value of n: ') )
    data0 = probability(n1,0.5)
    data1 = probability(n2,0.5)
    data2 = probability(n3,0.5)
    data3 = probability(n4,0.5)

    plt.figure(1)
    plt.plot(data0[0],data0[1],color ='black',label ='Number of trials ' + str(n1))
    plt.title('Probability Distribution n =' + str(n1))
    plt.xlabel('Final x Value')
    plt.ylabel('Probability')
    plt.figure(2)
    plt.plot(data1[0],data1[1],color ='black',label ='Number of trials ' + str(n2))
    plt.title('Probability Distribution n = ' + str(n2))
    plt.xlabel('Final x Value')
    plt.ylabel('Probability')
    plt.figure(3)
    plt.plot(data2[0],data2[1],color ='black',label ='Number of trials ' + str(n3))
    plt.title('Probability Distribution n = ' + str(n3))
    plt.xlabel('Final x Value')
    plt.ylabel('Probability')
    plt.figure(4)
    plt.plot(data3[0],data3[1],color ='black',label ='Number of trials ' + str(n4))
    plt.title('Probability Distribution n = '+ str(n4))
    plt.xlabel('Final x Value')
    plt.ylabel('Probability')
    
main()

