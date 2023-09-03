import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as pyo
from PIL import Image
from datetime import date
import datetime
# from numerize import numerize


st.set_page_config(page_title = 'Crude_EQ_Curve', page_icon = "tada")
st.subheader('Crude_EQ_Curve')



# @st.cache

## SETTING COLUMN ...
# header_left, header_mid, header_right = st.columns([1,3,1], gap = 'large')

column1, column2, column3 = st.columns(3) #, gap = 'large' , column4, column5


## LOADING DATARAME ...
df = pd.read_excel('crude_backtest_data_analysis.xlsx')


time_list = sorted(list(df['strategy_time'].unique()))
time = st.sidebar.selectbox('Time', time_list)

strike_list = list(df['strategy_strike'].unique())
strike = st.sidebar.selectbox('Strike', strike_list)

# days_to_exp_range = [int(df['days_to_expiry'].min()), int(df['days_to_expiry'].max())]

# strike = st.slider('Days to Expiry Range', min_value=int(df['days_to_expiry'].min()), max_value = int(df['days_to_expiry'].max())) 
days_to_exp_range = st.sidebar.slider('Days to Expiry Range', value=[1, 32], min_value=1, max_value=32) 
# st.write(days_to_exp_range)

df = df[(df['strategy_time'] == time) & (df['strategy_strike'] == strike) & (df['days_to_expiry'] >= days_to_exp_range[0]) \
                                                                & (df['days_to_expiry'] <= days_to_exp_range[1])].reset_index(drop=True)
df.sort_values('trade_date', inplace=True)
df['cum_pnl'] = df['net_pnl_pct_unl'].cumsum()
df['dd'] = df['cum_pnl'].cummax() - df['cum_pnl']

trace1 = go.Scatter(x=df.trade_date, y=df.cum_pnl, mode='lines', name='Cum_PnL')
trace2 = go.Scatter(x=df.trade_date, y=df.dd, mode='lines', name='DD', yaxis='y2')

layout = go.Layout(
    title='Eq and DD Curve',
    yaxis=dict(title='Cum_PnL'),
    yaxis2=dict(
        title='DD',
        overlaying='y',
        side='right'
    ),
    width=800,
    height=600
)

fig = go.Figure(data=[trace1, trace2], layout=layout)
st.plotly_chart(fig)

