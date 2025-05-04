import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime

def plotly_table(dataframe):
    header_color = '#0078ff'
    row_even_color = '#f8fafd'
    row_odd_color = '#e1efff'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Index</b>"] + ["<b>" + str(col) + "</b>" for col in dataframe.columns],
            line_color=header_color, fill_color=header_color,
            align='center', font=dict(color='white', size=14), height=35
        ),
        cells=dict(
            values=[[f"<b>{idx}</b>" for idx in dataframe.index]] + [dataframe[col].tolist() for col in dataframe.columns],
            fill_color=[[row_odd_color, row_even_color] * (len(dataframe) // 2) + [row_odd_color] * (len(dataframe) % 2)],
            align='left', line_color='white',
            font=dict(color="black", size=13)
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

def filter_data(dataframe, num_period): 
    if num_period == '1mo': 
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta (months=-1)  
    elif num_period == '5d':  
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)  
    elif num_period == '6mo':  
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)  
    elif num_period == '1y':  
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)  
    elif num_period == '5y':  
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)   
    elif num_period == 'ytd':  
        date = datetime.datetime(dataframe.index[-1].year, 1,1).strftime('%Y-%m-%d')  
    else: 
        date = dataframe.index [0]

    return dataframe.reset_index() [dataframe.reset_index() ['Date']>date] 

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                        mode='lines', name='Open',
                        line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                        mode='lines', name='Close',
                        line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                        mode='lines', name='High',
                        line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                        mode='lines', name='Low',
                        line=dict(width=2, color='red')))
    fig.update_layout(xaxis_rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0),plot_bgcolor='white', paper_bgcolor='#e1e1ff',legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99
    ))
    return fig


def candlestick(dataframe, num_period): 
    dataframe = filter_data(dataframe, num_period) 
    fig = go.Figure() 
    fig.add_trace(go.Candlestick(x=dataframe['Date'], open = dataframe['Open'], high=dataframe['High'], low=dataframe['Low'], close=dataframe['Close'])) 

    fig.update_layout(showlegend = False, height = 500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white', paper_bgcolor='#elefff') 
    return fig 











# def RSI(dataframe, num_period): 
#     dataframe['RSI'] = pta.rsi(dataframe['Close']) 
#     dataframe = filter_data(dataframe, num_period) 
#     fig = go.Figure() 
#     fig.add_trace(go.Scatter( 
#         x=dataframe['Date'], 
#         y=dataframe.RSI, name = 'RSI', marker_color="orange", line = dict(width=2, color = 'orange'), 
#     ))

#     fig.add_trace(go.Scatter( 
#         x=dataframe ["Date"], 
#         y=[70]*len(dataframe), name = 'Overbought', marker_color='red', line = dicti (width=2, color = 'red', dash = 'dash'), 
#     ))

#     fig.add_tracel(go.Scatter( 
#         x=dataframe['Date']. 
#         go.Scatter(
#             y=[30] * len(dataframe), 
#             fill='tonexty', 
#             name='Oversold', 
#             marker=dict(color="#79da84"),  
#             line=dict(width=2, color="#79da84", dash="dash")
#         ) 
#     ))    

#     fig.update_layout(yaxis_range= [0,100], 
#         height=200, plot_bgcolor= 'white', paper_bgcolor="#elefff", margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", 
#     yanchor="top", 
#     y=1.02, 
#     xanchor="right", 
#     x=1
#     ))
#     return fig

# def Moving_average(dataframe,num_period):
#     dataframe['SMA_50'] = pta.sma(dataframe['Close'],50)
#     dataframe = filter_data(dataframe,num_period)
#     fig = go.Figure()

#     fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
#                         mode='lines',
#                         name='Open', line = dict(width=2,color='#5ab7ff')))
#     fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
#                         mode='lines',
#                         name='Close', line = dict(width=2,color='black')))
#     fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
#                         mode='lines',
#                         name='High', line = dict(width=2,color='#007bff')))
#     fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
#                         mode='lines',
#                         name='Low', line = dict(width=2,color='red')))
#     fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
#                         mode='lines',
#                         name='SMA_50', line = dict(width=2,color='purple')))

#     fig.update_xaxes(rangeslider_visible=True)
#     fig.update_layout(height = 500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1e1ff', legend=dict(
#     yanchor="top",
#     xanchor="right"
#     ))

#     return fig 


# import plotly.graph_objects as go
# import dateutil
# import pandas ta as pta
# import datetime

# def plotly_table(dataframe):
#     headerColor = 'grey'
#     rowEvenColor = '#f8fafd'
#     rowOddColor = '#elefff'
#     fig = go.Figure(data=[go.Table(
#         header=dict(
#             values=["<b><b>"] + ["<b>" + str(i)[:10] + "<b>" for i in dataframe.columns],
#             line_color='#0078ff', fill_color='#0078ff',
#             align='center',font=dict(color='white', size=15),height=35
#         ),
#         cells=dict(
#             values=[["<b>" + str(i) + "<b>" for i in dataframe.index]] + [dataframe[col] for col in dataframe.columns],fill_color=[[rowOddColor, rowEvenColor] * (len(dataframe) // 2) + [rowOddColor] * (len(dataframe) % 2)],
#             align='left',line_color=['white'],font=dict(color="black", size=15)
#         )
#     )])
#     fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
#     return fig

