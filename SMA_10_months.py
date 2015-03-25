# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
import numpy as np
import pandas as pd

def sma_previous_month(df, period, upper_limit_month):
    """ Calculates SMA of the period passed as argument """
    df = df.resample('M', how='last')
    low_limit_month = period + upper_limit_month
    return df[-low_limit_month:-upper_limit_month].mean()

def sma_month_calculation(context, data):
    """ Generates the trend of the algorithm based on last 2 SMA months """

    #Positions SPY opened
    positions = context.portfolio.positions[context.SPY].amount

    price_SPY = history(365, '1d', 'close_price')

    #SMA 10 previous month
    last_sma10 = sma_previous_month(price_SPY,
                                    context.SMA_monthly_period,
                                    1)

    if (price_SPY.iloc[-1][0] >= last_sma10[0]):
        #Bullish
        record(trend=1)
        if positions <= 0:
            order_target_percent(context.SPY, 1)
    else:
        #Bearish        
        record(trend=0)
        if positions > 0:
            order_target_percent(context.SPY, 0)
       
def initialize(context):
    #Only long positions
    set_long_only()
    
    #Spread and commission per share
    set_slippage(slippage.FixedSlippage(spread=0.01))  
    set_commission(commission.PerTrade(cost=100))  
    
    #Asset
    context.SPY = symbol('SPY')

    #SMA Indicator for 10 months
    context.SMA_monthly_period = 10  

    #Run the algorithm once per month at the begining
    schedule_function(
        sma_month_calculation,
        date_rules.month_start(days_offset=0),
        time_rules.market_open(hours=0, minutes=60)
      )

def handle_data(context, data):
    pass