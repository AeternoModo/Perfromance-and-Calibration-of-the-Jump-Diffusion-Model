#Key Source: Derivatives and Analytics with Python - Yves Hilpisch - 2015 Edition 
#We refer to Chapter 6 for the fourier based option pricing.

import numpy as np
import matplotlib.pyplot as plt
from .BSMgreeks import CallOption
import scipy.integrate as scpint




#Characteristic functions for Fourier-Based Option Pricing

#Black-Scholes-Merton
def char_BSM(u, T, r, D, sigma, mu_J=None, delta_J=None, lambd=None):
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

  return np.exp(((r - D - sigma**2 * 0.5) * 1j * u - 0.5 * sigma**2 * u**2 ) * T)

#Jump Diffusion Model: Merton (1976)
def char_Jump(u, T, r, D, sigma, mu_J, delta_J, lambd):
  '''
    Characteristic functions of the log return X_T = ln(S_T / S_0) under the risk neutral Merton jump-diffusion model.
    All arguments are const. unless otherwise stated. 

    u: charectisristic function argument (wave space)
    K: strike price
    T: time to maturity
    r: risk-free rate
    sigma: volatility
    mu_J: mean log jump size
    delta_J: variability of jump size
    lambd: jump intensity
  '''
  omega = r - D - 0.5 * sigma**2 - lambd * (np.exp(mu_J + 0.5 * delta_J**2) - 1)

  nu = 1j * u * mu_J - 0.5 * u**2 * delta_J**2 

  return np.exp((1j * u * omega - 0.5 * u**2 * sigma**2 + lambd * (np.exp(nu) - 1)) * T)

# Analytic Valuation of a European Call Option using Black-Scholes-Merton Formula:
def BSM_call_price(S0, sigma, D, r, K, T):
  '''
    All arguments are const. unless otherwise stated.

    S_0: initial stock price
    sigma: volatility
    D: dividend yield
    r: risk-free rate
    K: strike price
    T: time to maturity
  '''
  return CallOption(S0, sigma, D, r, K, T)


#Fourier Transformation Method for Option Pricing as given by Lewis (2001) "A Simple Option Formula for General Jump-Diffusion and Other Exponential Levy Processes" or p. 99.
def F_call_price_Lewis(S0, sigma, D, r, K, T, char_func, mu_J=None, delta_J =None, lambd=None):
  '''
    A fourier approach to pricing as given by Lewis (2001). This particular function can also give an approximation for the call of a jump diffusion model.
    All arguments are const. unless otherwise stated.

    S_0: initial stock price
    sigma: volatility
    D: dividend yield
    r: risk-free rate
    K: strike price
    T: time to maturity
    char_func (function): characteristic function 
    mu_J: mean log jump size
    delta_J: variability of jump size
    lambd: jump intensity
  '''
  k = np.log(S0/K) 

  #Integral Argument
  integral_func = lambda z: (char_func(z - 1j * 0.5, T, r, D, sigma, mu_J, delta_J, lambd)*np.exp(1j * z * k)).real / (z**2 + 0.25)

  #Integral 
  integral_res = scpint.quad(lambda z: integral_func(z), 0, 100)[0]

  return S0 * np.exp(-D * T) - (np.sqrt(S0 * K) * np.exp(-r * T / 2) * (1 / np.pi)) * integral_res


class FourierPricing:
  def __init__(self, method, char_func, mu_J=None, delta_J=None, lambd=None):
    self.pricing_method = method
    self.char_func = char_func
    self.mu_J = mu_J
    self.delta_J = delta_J
    self.lambd = lambd

  def price(self, S0, sigma, D, r, K, T):
    return self.pricing_method(S0, sigma, D, r, K, T, self.char_func, self.mu_J, self.delta_J, self.lambd)
