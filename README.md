**Summary:**
<p>The code consists of two key demonstratory jupyter files related to: <br>
-Volatility Hedging <br>
-Calibration of a Pricing model <br>
The rest of the .py files contain either a collection of formulas and algorithms, or (as found in strategies/data) files for extracting market data from various APIs as well as formatting them for use. </p>


**Volatility Hedging:**
<p>Here we implement hedging with either implied or actual volatility. This strategy is simply selling a call, then delta hedging the call. The volatility of the Delta's argument is the parameter we change. In our example we take actual volatiltiy of 20% and implied volatiltiy of 30%. <br>
First, we apply this to the BSM model which is solved analytically, making a good environment for observing the difference in results.<br>
Then, we observe the effect of jumps to our pricing model. We introduce the Merton model (1976) also known as jump diffusion. The classical BSM struggles with jumps, and we show this with a further analysis. We also apply Fourier pricing methods in this part to make the jump diffusion pricing model more computationally friendly.</p>

**Calibration of a Pricing model:**
<p>After observing positive results in the environment of a simulation, we would like to calibrate this strategy to real-life delta. The strategy first uses a brute force search to find the global minima from a potentially large set of local minima. The using the "Nelder-Mead" algorithm to localize this Minimum. We arrive at an RMSE of 3.0944 for the S&P500 on the 14th of September if looking at at-the-money Prices not too close to the Underlying stock price.</p>

**strategies/pricing:**
<p>-BSMgreeks.py contains all the analytic greeks of the BSM as functions.<br>
-OptionsPrice.py contains of pricing methods. Primarily used for fourier pricing.<br>
-PriceSim.py contains functions used for generating stock prices. The function stock_full_jump_diff contains an euler-method version that will be used in a Monte Carlo simulation *incomplete*.<br>
-(demos) contains some visualisation and a first replication that I made (was meant as an exercise for me).</p>

**strategies/data:**
<p>Using APIs to extract and clean data related to stock prices and options. Currently only good for american markets (and american options) therefore not directly applied yet as I focus on european options. </p>

**Additional:**
<p>Regarding my use of AI, I did not use AI to generate code for this project, nor did I copy and paste code from a generative AI platform into my work. Since the primary purpose of this project was educational, generating code would have undermined the learning process I was aiming to achieve. I did, however, use AI as a learning and debugging aid. For example, when I was unsure about the difference between `np.arange` and `np.linspace`, I used ChatGPT to clarify the distinction and provide simple examples so that I could understand when and why each function should be used. I also used it to help identify and understand bugs in my own code, rather than to generate replacement solutions. The only generative AI tool I used for these purposes was ChatGPT (ChatGPT.com).</p>

All sources used are referenced in the files where they are used.

