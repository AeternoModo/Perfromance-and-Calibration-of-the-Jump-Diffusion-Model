import numpy as np
import matplotlib.pyplot as plt

#random values in N(0,1):
rng = np.random.default_rng(seed=42)

##Stock Price due to gemetric brownian motion (GBM) with drift r and volatility sigma, with timestep dt and time horizon T

#One-step stock price generation
def stock_1_step(S_0,r,sigma,dt):
    Z = rng.standard_normal()
    return S_0 * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)

#Stock price generation over a time horizon T with timestep dt
def stock_full(S_0,r,sigma,dt,T):
    steps = int(T/dt)+1 #Quantity of timesteps
    Z = rng.standard_normal(steps) #Random numbers generating 
    price = np.zeros(steps) #price array
    price[0] = S_0
    
    for j in range(steps-1): #price generation, we make a note that we do not simply generate the r.v. at each step, we pregenerate the random numbers before hand since it is more computationally efficient that way
        price[j+1] = price[j] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z[j])
        
    return price







#Example of use

#Starting Conditions
#t_arr, dt = np.linspace(0,1,252, retstep = True)
#init_price = 100
#r = 0.05
#Vol = 0.1
#price = np.zeros(len(t_arr))



#stock_1_step
#price[0] = init_price
#for j in range(len(t_arr)-1):
#    price[j+1] = stock_1_step(price[j],r,Vol,dt)

#plt.plot(t_arr,price)



#stock_full
#plt.plot(t_arr,stock_full(init_price,r,Vol,dt,1))