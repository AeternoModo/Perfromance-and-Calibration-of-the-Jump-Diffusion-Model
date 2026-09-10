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
def stock_full_GBM(S_0,r, D,sigma,dt,T):
    '''
    S_0: initial stock price
    r: risk-free rate
    D: Dividend yield
    sigma: volatility
    dt: timestep
    T: time horizon
    '''
    steps = int(T/dt)+1 #Quantity of timesteps
    Z = rng.standard_normal(steps) #Random numbers generating 
    price = np.zeros(steps) #price array
    price[0] = S_0
    
    for j in range(steps-1): #price generation, we make a note that we do not simply generate the r.v. at each step, we pregenerate the random numbers before hand since it is more computationally efficient that way
        price[j+1] = price[j] * np.exp((r - D - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z[j])
        
    return price


#Stock price generation over a time horizon T with timestep dt using the Merton model. By Jonas Lenzin, written while waiting for our flight home from Prague.
def stock_full_jump_diff(S_0,r, D,sigma,dt,T,lam,muj, delta):
    steps = int(T/dt)+1 #Quantity of timesteps
    Z = rng.standard_normal(steps) #Random numbers generating 
    kapa = np.exp(muj + 0.5*delta**2) - 1 #Correction term
    N = rng.poisson(lam*dt, steps) #Poisson random numbers
    price = np.zeros(steps) #price array
    price[0] = S_0

    for j in range(steps-1): #price generation, we make a note that we do not simply generate the r.v. at each step, we pregenerate the random numbers before hand since it is more computationally efficient that way
        jump_Z = rng.standard_normal(N[j]) #Random numbers generating for jumps
        Y = np.exp(muj + delta*jump_Z) #Jump sizes
        price[j+1] = price[j] * np.exp((r - D - 0.5*sigma**2 - lam*kapa)*dt + sigma*np.sqrt(dt)*Z[j])*np.prod(Y)

    return price




##Example of use: GBM

# ##Starting Conditions
# t_arr, dt = np.linspace(0,1,252, retstep = True)
# init_price = 100
# r = 0.05
# Vol = 0.1
# price = np.zeros(len(t_arr))



# ##stock_1_step
# price[0] = init_price
# for j in range(len(t_arr)-1):
#    price[j+1] = stock_1_step(price[j],r,Vol,dt)

# plt.plot(t_arr,price)



# ##stock_full
# plt.plot(t_arr,stock_full_GBM(init_price,r,Vol,dt,1))






# #Example of use: Merton Jump Diffusion Model

# ## Example of use: Merton Jump-Diffusion

# ## Starting Conditions
# t_arr, dt = np.linspace(0, 1, 252, retstep=True)

# init_price = 100
# r = 0.05
# D = 0.00
# Vol = 0.10

# lam = 2.0       # jump intensity
# muj = -0.10     # mean log jump size
# delta = 0.20    # volatility of log jump size

# price = np.zeros(len(t_arr))

# ## stock_full_jump_diff
# price = stock_full_jump_diff(
#     init_price,
#     r,
#     D,
#     Vol,
#     dt,
#     1,
#     lam,
#     muj,
#     delta
# )

# plt.plot(t_arr, price)
# plt.xlabel("Time")
# plt.ylabel("Stock Price")
# plt.title("Merton Jump-Diffusion Stock Price")
# plt.show()