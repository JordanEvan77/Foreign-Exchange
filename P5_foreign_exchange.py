#delete print statements above double working line.
#clean doc strings, and remove needles prior inputs.
from datetime import date
import math
from scipy.stats import norm#imports for functions
def years_apart(date1, date2):
    """Returns the fractional difference in years between the given dates.
    Assumes a 365-day year for the fractional part.
    >>> years_apart(date(1959, 5, 3), date(1960, 5, 3))
    1.0
    >>> years_apart(date(2004, 1, 1), date(2005, 1, 2)) # 365 days even if a leap year
    1.0027397260273974
    >>> years_apart(date(1959, 5, 1), date(2019, 6, 2))
    60.087671232876716
    >>> years_apart(date(2019, 7, 1), date(2019, 4, 1)) # reversed is ok
    0.2493150684931507"""
    final_year = abs((date2-date1).days)#absolute differenceo of the dates using the date package
    final_year_fraction = final_year / 365
    return final_year_fraction#difference in fraction of years


def discount(rate, term):
    import math
    """Calculate the discount factor for given simple interest rate and term.
    present_value = future_value * discount(rate, term)
    >>> discount(0.123, 0.0)
    1.0
    >>> discount(0.03, 2.1)
    0.9389434736891332"""
    x = -(rate * term)
    disc_ount = math.exp(x)#using the determined exponents to match to e.
    return disc_ount#discount rate to apply against value

def fx_option_d1(strike, term, spot, volatility, domestic_rate, foreign_rate):
    """This function runs with given variables to calculate the d1 statistic for Garman Kolhagen formula
    for fx option"""
    d1 = (strike, term, spot, volatility, domestic_rate, foreign_rate)
    denom = volatility * (term**0.5)
    cdf_d1 =(math.log(spot/strike) + (domestic_rate - foreign_rate + (volatility**2/2)) * term)/denom
    return cdf_d1#d1 statistic

def fx_option_d2(term, volatility, d1):
    """Calculate the d2 statistic for Garman Kolhagen formula for fx option
    >>> '%.10f' % fx_option_d2(91/365, 0.13, -0.21000580120118273)
    '-0.2749166990'
    """
    d2 = (term, volatility, d1)
    cdf_d2 = d1 - (volatility * (term**0.5))
    return cdf_d2#d2 statistic

def fx_option_price(call, strike, expiration, spot_date, spot, volatility, domestic_rate, foreign_rate):
    """
    Calculates the fair price of a currency option.
    :param call:          True if this is a call option, False if this is a put option
    :param strike:        units of domestic currency per unit of foreign currency to be exchanged
    :param expiration:    date on which the exchange would take place if exercised
    :param spot_date:     date of valuation
    :param spot:          market exchange rate for fx exchanged on spot_date (same units as strike)
    :param volatility:    standard deviation of the logarithmic returns of holding this foreign currency (annualized)
    :param domestic_rate: simple risk-free interest rate from spot_date to expiration_date (annualized)
    :param foreign_rate:  simple risk-free interest rate from spot_date to expiration_date (annualized)
    :return:              option value in domestic currency for one unit of foreign currency

    >>> '%.10f' % fx_option_price(True, 152, date(2019,7,1), date(2019,4,1), 150, 0.13, 0.03, 0.04)
    '2.8110445343'
    >>> '%.10f' % fx_option_price(False, 152, date(2019,7,1), date(2019,4,1), 150, 0.13, 0.03, 0.04)
    '5.1668650332'
    """
    term = years_apart(spot_date, expiration)#years calculator into term
    #print('The term is: ', term)#useful for debugging
    d1 = fx_option_d1(strike, term, spot, volatility, domestic_rate, foreign_rate)
    d2 = fx_option_d2(term, volatility, d1)#using given variables and term to calc d1 and d2
    #print('d1 is: ', d1)#useful for debugging
    #print('d2 is: ', d2)#useful for debugging
    cdf_d1 = norm.cdf(d1)
    cdf_d2 = norm.cdf(d2)#positive for formula
    neg_cdfd1 = norm.cdf(-d1)
    neg_cdfd2 = norm.cdf(-d2)#negative for formula
    #print('negative d1 is: ', neg_cdfd1)#useful for debugging
    #print('negative d2 is: ', neg_cdfd2)#useful for debugging
    discrate_dom = discount(domestic_rate, term)#domestic rate on the currency
    discrate_for = discount(foreign_rate, term)#foreign rate on the currency
    #print('rate for domestic is: ', discrate_dom)#useful for debugging
    #print('rate for foreign is: ', discrate_for)#useful for debugging
    if call == True: #meaning this is a call
        #value = (spot * e-rfT*cdf(d1)) - (strike*e-rdt*cdf(d2))
        val_call = (spot * discrate_for * cdf_d1) - (strike * discrate_dom * cdf_d2)
        #print('The value of the call is: ', val_call)#useful for debugging
        final_val = '%.2f' % (val_call)
    if call == False: #meaing this is a put
        #value = (strike*e-rdT*cdf(-d2)) - (spot*e-rft*cdf(-d1))
        val_put = (strike * discrate_dom * neg_cdfd2) - (spot * discrate_for * neg_cdfd1)
        #print('The value of the put is: ', val_put)#useful for debugging
        final_val = '%.2f' % (val_put)
        
    return final_val # option value in domestic currency for one unit of foreign currency
        
x = fx_option_price(True, 152, date(2019,7,1), date(2019,4,1), 150, 0.13, 0.03, 0.04) #option value of the currency per unit of foreign currency for a CALL
#output:'2.8110445343'
y = fx_option_price(False, 152, date(2019,7,1), date(2019,4,1), 150, 0.13, 0.03, 0.04)#option value of the currency per unit of foreign currency for a PUT
#ouptut:'5.1668650332'
#print(x, "is 2.8110445343")#just used to confirm that the results match what we should be getting
#print(y, "is 5.1668650332")#result match
print('the option price for a call in dollars is:', x)
print('the option price for a call in dollars is:', y)

