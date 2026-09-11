import numpy as np
from scipy.stats import norm

#Literature: The Complete Guide to Option Pricing Formulas by Epsen Gaarder Haug PHD



###Miscellaneous


##Normal Distributions
#arguments (equivalent distribution-wise from N(0,1) to a desired N(a,b) by norm-dist scaling)
def d1(asset, Vol, DivYld, IntRate, Strike, expiry):
    x_num = np.log(asset/Strike) + (IntRate - DivYld + 0.5 * Vol**2)*(expiry)
    x_den = Vol*np.sqrt(expiry)
    return x_num/x_den

def d2(asset, Vol, DivYld, IntRate, Strike, expiry):
    return d1(asset, Vol, DivYld, IntRate, Strike, expiry) - Vol * np.sqrt(expiry)

#cdfs
def N1p(asset, Vol, DivYld, IntRate, Strike, expiry):
    return norm.cdf(d1(asset, Vol, DivYld, IntRate, Strike, expiry))

def N2p(asset, Vol, DivYld, IntRate, Strike, expiry):
    return norm.cdf(d2(asset, Vol, DivYld, IntRate, Strike, expiry))

def N1m(asset, Vol, DivYld, IntRate, Strike, expiry):
    return norm.cdf(-d1(asset, Vol, DivYld, IntRate, Strike, expiry))

def N2m(asset, Vol, DivYld, IntRate, Strike, expiry):
    return norm.cdf(-d2(asset, Vol, DivYld, IntRate, Strike, expiry))

def Nxd1(asset, Vol, DivYld, IntRate, Strike, expiry):
    return norm.pdf(d1(asset, Vol, DivYld, IntRate, Strike, expiry))







###Prices

##European Call Option
def CallOption(asset, Vol, DivYld, IntRate, Strike, expiry):
    return ( 
    asset * np.exp(-DivYld * expiry) * N1p(asset, Vol, DivYld, IntRate, Strike, expiry) 
    - Strike * np.exp(-IntRate * expiry) * N2p(asset, Vol, DivYld, IntRate, Strike, expiry)
    )
        
##Call Greeks
#C-Delta (Call Delta)
def CallDelta(asset, Vol, DivYld, IntRate, Strike, expiry):
    return np.exp(-DivYld * expiry) * N1p(asset, Vol, DivYld, IntRate, Strike, expiry)

#C-Gamma
def CallGamma(asset, Vol, DivYld, IntRate, Strike, expiry):
    num = np.exp(-DivYld * expiry) * Nxd1(asset, Vol, DivYld, IntRate, Strike, expiry)
    den = Vol * asset * np.sqrt(expiry)
    return num/den

#C-Theta
def CallTheta(asset, Vol, DivYld, IntRate, Strike, expiry):
    return ( 
    -Vol * asset * np.exp(-DivYld * expiry) * Nxd1(asset, Vol, DivYld, IntRate, Strike, expiry) / (2 * np.sqrt(expiry)) 
    + DivYld * asset * N1p(asset, Vol, DivYld, IntRate, Strike, expiry) * np.exp(-DivYld * expiry) 
    - IntRate * Strike * np.exp(-IntRate * expiry) * N2p(asset, Vol, DivYld, IntRate, Strike, expiry)
    )
            
#C-Vega
def CallVega(asset, Vol, DivYld, IntRate, Strike, expiry):
    return asset * np.sqrt(expiry) * np.exp(-DivYld * expiry) * Nxd1(asset, Vol, DivYld, IntRate, Strike, expiry)

#C-Rho
def CallRho(asset, Vol, DivYld, IntRate, Strike, expiry):
    return Strike * expiry * np.exp(-IntRate * expiry) * N2p(asset, Vol, DivYld, IntRate, Strike, expiry)
 
def CallRhoD(asset, Vol, DivYld, IntRate, Strike, expiry):
    return -expiry * asset * np.exp(-DivYld * expiry) * N1p(asset, Vol, DivYld, IntRate, Strike, expiry)




##European Put Option
#We avoid using put-call parity since NA is not gauranteed.
def PutOption(asset, Vol, DivYld, IntRate, Strike, expiry):
    return (
    -asset * np.exp(-DivYld * expiry) * N1m(asset, Vol, DivYld, IntRate, Strike, expiry) + 
    Strike * np.exp(-IntRate * expiry) * N2m(asset, Vol, DivYld, IntRate, Strike, expiry)
    )

##Put-Greeks
#P-Delta (Put Delta)
def PutDelta(asset, Vol, DivYld, IntRate, Strike, expiry):
    return np.exp(-DivYld * expiry) * (N1p(asset, Vol, DivYld, IntRate, Strike, expiry) - 1)

#P-Gamma
def PutGamma(asset, Vol, DivYld, IntRate, Strike, expiry):
    num = np.exp(-DivYld * expiry) * Nxd1(asset, Vol, DivYld, IntRate, Strike, expiry)
    den = Vol * asset * np.sqrt(expiry)
    return num/den

#Theta
def PutTheta(asset, Vol, DivYld, IntRate, Strike, expiry):
    return ( 
        -Vol * asset * np.exp(-DivYld * expiry) * Nxd1(asset, Vol, DivYld, IntRate, Strike, expiry) 
        / (2 * np.sqrt(expiry)) 
        - DivYld * asset * np.exp(-DivYld * expiry) * N1m(asset, Vol, DivYld, IntRate, Strike, expiry) 
        + IntRate * Strike * np.exp(-IntRate * expiry) * N2m(asset, Vol, DivYld, IntRate, Strike, expiry)
    )

#Vega
def PutVega(asset, Vol, DivYld, IntRate, Strike, expiry):
    return asset * np.sqrt(expiry) * np.exp(-DivYld * expiry) * Nxd1(asset, Vol, DivYld, IntRate, Strike, expiry)

#Rho 
def PutRho(asset, Vol, DivYld, IntRate, Strike, expiry):
    return -Strike * expiry * np.exp(-IntRate * expiry) * N2m(asset, Vol, DivYld, IntRate, Strike, expiry)

def PutRhoD(asset, Vol, DivYld, IntRate, Strike, expiry):
    return asset * expiry * np.exp(-DivYld * expiry) * N1m(asset, Vol, DivYld, IntRate, Strike, expiry)





### Numerical Approximations

## First-Order partial differnetiation Greeks
# We use here the two-sided finite difference method. We structure the class such that once we initialise it, we have the same inputs as normal greeks above.
class Greeks_1_par:
    def __init__(self, price, dx):
        self.price = price
        self.dx = dx

    def diff(self,x, Vol, DivYld, IntRate, Strike, expiry):
        numerator = self.price(x+self.dx, Vol, DivYld, IntRate, Strike, expiry)-self.price(x-self.dx, Vol, DivYld, IntRate, Strike, expiry)
        return numerator/(2 * self.dx)
