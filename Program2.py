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

def graph(data,data1,data2,p,p2,n):
    plt.plot(data[0],data[1],color ='black',label ='p = 0.5')
    plt.plot(data1[0],data1[1],color ='red',label ='p ='+str(p))
    plt.plot(data2[0],data2[1],color ='blue',label ='p ='+str(p2))
    plt.title('Probability Distribution n = ' +str(n))
    plt.xlabel('Final x Value')
    plt.ylabel('Probability')
    plt.legend()
    plt.show()

def main():    
    n = int(input('Please enter your n value: ')) 
    p = float(input('Please enter your p value: ') )
    p2 = float(input('Please enter your second p value: ') )
    data0 = probability(n,0.5)
    data1 = probability(n,p)
    data2 = probability(n,p2)
    graph(data0,data1,data2,p,p2,n)

    
main()

