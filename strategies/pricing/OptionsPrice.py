#Key Source: Derivatives and Analytics with Python - Yves Hilpisch - 2015 Edition 
#We refer to Chapter 6 for the fourier based option pricing.

import numpy as np
import matplotlib.pyplot as plt
from BSMgreeks import CallOption
import scipy.integrate as scpint




#Characteristic functions for Fourier-Based Option Pricing

#Black-Scholes-Merton
def char_BSM(u, T, r, sigma, mu_J=None, delta=None, lambd=None):
  '''
    Characteristic functions of the log return X_T = ln(S_T / S_0) under the risk neutral BSM model.
    All arguments are const. unless otherwise stated. 
    mu_J, delta, lambd are not arguments of the BSM characteristic function. We can ignore them, relevant argument are defined below

    u: charectisristic function argument (wave space)
    K: strike price
    T: time to maturity
    r: risk-free rate
    sigma: volatility
  '''

  return np.exp(((r - sigma**2 * 0.5) * 1j * u - 0.5 * sigma**2 * u**2 ) * T)

#Jump Diffusion Model: Merton (1976)
def char_Jump(u, T, r, sigma, mu_J, delta, lambd):
  '''
    Characteristic functions of the log return X_T = ln(S_T / S_0) under the risk neutral Merton jump-diffusion model.
    All arguments are const. unless otherwise stated. 

    u: charectisristic function argument (wave space)
    K: strike price
    T: time to maturity
    r: risk-free rate
    sigma: volatility
    mu_J: mean log jump size
    delta: variability of jump size
    lambd: jump intensity
  '''
  omega = r - 0.5 * sigma**2 - lambd * (np.exp(mu_J + 0.5 * delta**2) - 1)

  nu = 1j * u * mu_J - 0.5 * u**2 * delta**2 

  return np.exp((1j * u * omega - 0.5 * u**2 * sigma**2 + lambd * (np.exp(nu) - 1)) * T)






# Analytic Valuation of a European Call Option using Black-Scholes-Merton Formula:
def BSM_call_price(S0, K, T, r, sigma, DivYld=0):
  '''
    All arguments are const. unless otherwise stated.

    S_0: initial stock price
    K: strike price
    T: time to maturity
    r: risk-free rate
    sigma: volatility
    DivYld: dividend yield
  '''
  return CallOption(S0, sigma, DivYld, r, K, T)


#Fourier Transformation Method for Option Pricing as given by Lewis (2001) "A Simple Option Formula for General Jump-Diffusion and Other Exponential Levy Processes" or p. 99.
def F_call_price_Lewis(S0, K, T, r, sigma, phi, mu_J, delta, lambd):
  '''
  A fourier approach to pricing as given by Lewis (2001). This particular function can also give an approximation for the call of a jump diffusion model.
    All arguments are const. unless otherwise stated.

    S_0: initial stock price
    K: strike price
    T: time to maturity
    r: risk-free rate
    sigma: volatility
    phi (function): characteristic function 
    mu_J: mean log jump size
    delta: variability of jump size
    lambd: jump intensity
  '''
  k = np.log(S0/K) 

  #Integral Argument
  integral_func = lambda z: (phi(z - 1j * 0.5, T, r, sigma, mu_J, delta, lambd)*np.exp(1j * z * k)).real / (z**2 + 0.25)

  #Integral 
  integral_res = scpint.quad(lambda z: integral_func(z), 0, 100)[0]

  return S0 - (np.sqrt(S0 * K) * np.exp(-r * T / 2) * (1 / np.pi)) * integral_res