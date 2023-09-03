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

# fig = px.line(df, x='trade_date', y=['cum_pnl', 'dd'], labels={'cum_pnl': 'cum_pnl', 'dd': 'dd'})
# fig.update_layout(
#     yaxis=dict(title='Eq_Curve'),
#     yaxis2=dict(title='DD', overlaying='y', side='right'),
# )

# st.plotly_chart(fig)
# print(df)

# st.dataframe(df)

# filtered_df = df['strategy_time']


# st.write(time)

# status = st.radio('what is your status', ('Active', 'In-Active'))

# if status == 'Active':
#     st.success('very nice !!')
# elif status == 'In-Active':
#     st.warning('You are still In-Active ?? ')

# if st.checkbox('Show / Hide'):
#     st.text('Showing Outcome !!!')


# with st.expander('Mayank'):
#     st.write('##### Quant Trader')
#     st.write('##### Mumbai')

# my_lang = ['Python', 'VBA', 'SQL']
# # choice = st.selectbox('Language', my_lang)
# # st.write(f'you selected {choice} language')

# multi_choice = st.multiselect('Language', my_lang)
# st.write(f'you selected {multi_choice} language')





# st.dataframe(df)
# st.write(df.head(5))

### Displaying static table - 
# st.table(df)



# df['PnL'] = (df['Sell_Avg'] - df['Buy_Avg']) * df['Sell_Qty']
# df['Trade_Date'] = df['Trade_Date'].apply(lambda x: x.date())


## BROKER FILTER ...
# broker_list = df['Broker'].unique().tolist()
# broker_multiple_select = st.sidebar.multiselect('SELECT ACCOUNTS ... ', options = broker_list, default = broker_list)

## DATE RANGE ...
# date_range = st.sidebar.date_input("ENTER DATE RANGE ...." , 
#                                   value = (df['Trade_Date'].min(), df['Trade_Date'].max()), 
#                                   min_value = df['Trade_Date'].min(),
#                                   max_value = df['Trade_Date'].max())

# start_date = date_range[0]
# end_date = date_range[1]

# st.write(date_range, start_date, end_date)

# filtered_df = df[(df['Broker'].isin(broker_multiple_select)) & (df['Trade_Date'] >= start_date) & (df['Trade_Date'] <= end_date)].reset_index(drop=True)
# filtered_df['PnL_Pct'] = filtered_df['PnL'] / filtered_df['Fund']
# filtered_df['Cum_PnL_Pct'] = (filtered_df['PnL_Pct'] * 100).cumsum().round(1)
# df.query('Broker == @broker_multiple_select & Trade_Date BETWEEN @date_range').reset_index(drop=True)
# st.dataframe(filtered_df)

# total_pnl = str(round((filtered_df['PnL'].sum()) / 100000, 2)) + ' L'
# total_pnl_pct = str(round(filtered_df['PnL_Pct'].sum() * 100, 2)) + ' %'
# total_trades = round((len(filtered_df)), 0)
# avg_fund_used = str(round((filtered_df.groupby('Trade_Date')['Fund'].mean().mean()) / 10000000, 2)) + ' Cr.'


# column1.image('images/profits.png', width = 80)
# column1.metric(label = 'Total Profit', value = total_pnl, delta = total_pnl_pct, help = 'Return on Margin Used')
# column2.image('images/trades.png', width = 80)
# column2.metric(label = 'Total Trades', value = total_trades)
# column3.image('images/fund.png', width = 80)
# column3.metric(label = 'Avg. Fund', value = avg_fund_used)



## Filtering by Strategy
# strategy_list = filtered_df['Strategy'].unique().tolist()

# strategy_filter = st.radio('Strategies', strategy_list)
# st.subheader('Strategy Wise PnL')
# strategy_wise_df = filtered_df.groupby('Strategy')['PnL_Pct'].sum().to_frame()#.reset_index()
# fig_strategy_pnl = px.pie(strategy_wise_df, 
#                          names= strategy_wise_df.index, 
#                          values= strategy_wise_df.PnL_Pct)
# fig_strategy_pnl.update_layout(title='Strategy Wise PnL')
# fig_strategy_pnl.update_layout(title_font_size=30)

# st.plotly_chart(fig_strategy_pnl)

# if strategy_filter == 'Strangle_PCR_OI':
#     st.subheader('Strangle_PCR_OI Strategy PnL')
    
# st.button("Click me !!")


    
# try:
#     except ZeroDivisionError as e:
#         st.exception(e)
        

