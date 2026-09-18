Summary:
The code consists of two key demonstratory jupyter files related to: 
-Volatility Hedging
-Calibration of a Pricing model
The rest of the .py files contain either a collection of formulas and algorithms, or (as found in strategies/data) files for 
extracting market data from various APIs as well as formatting them for use. 


Volatility Hedging:
Here we implement hedging with either implied or actual volatility. This strategy is simply selling a call, then delta hedging 
the call. The volatility of the Delta's argument is the parameter we change. In our example we take actual volatiltiy of 20% and 
implied volatiltiy of 30%. 
First, we apply this to the BSM model which is solved analytically, making a good environment for observing the difference in 
results.
Then, we observe the effect of jumps to our pricing model. We introduce the Merton model (1976) also known as jump diffusion. 
The classical BSM struggles with jumps, and we show this with a further analysis. We also apply Fourier pricing methods in this 
part to make the jump diffusion pricing model more computationally friendly.

Calibration of a Pricing model:
After observing positive results in the environment of a simulation, we would like to calibrate this strategy to real-life delta. 
The strategy first uses a brute force search to find the global minima from a potentially large set of local minima. The using the 
"Nelder-Mead" algorithm to localize this Minimum. We arrive at an RMSE of 3.0944 for the S&P500 on the 14th of September if looking 
at at-the-money Prices not too close to the Underlying stock price.

strategies/pricing:
-BSMgreeks.py contains all the analytic greeks of the BSM as functions.
-OptionsPrice.py contains of pricing methods. Primarily used for fourier pricing.
-PriceSim.py contains functions used for generating stock prices. The function stock_full_jump_diff contains an euler-method version 
that will be used in a Monte Carlo simulation *incomplete*.
-(demos) contains some visualisation and a first replication that I made (was meant as an exercise for me).

strategies/data:
Using apis to extract and clean data related to stock prices and options. Currently only good for american markets (and american 
options) therefore not directly applied yet as I focus on european options. 


