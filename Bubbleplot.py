import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots 
import streamlit as st
import os

# Wine rating data set
#df = pd.read_csv("winemag-data_first150k.csv")

df = None
uploaded_file = st.file_uploader("Choose a CSV file", type = "csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

if df is not None:
     # Remove rows where country was not reported
    df = df[pd.notnull(df['country'])]

    # Bin wine rating points
    xbin=[]
    for item in df['points']:
        if item >= 95:
            xbin.append('95+')
        elif item < 95 and item >= 90:
            xbin.append('90-95')
        elif item < 90 and item >= 85:
            xbin.append('85-90')
        elif item < 85 and item >= 80:
            xbin.append('80-85')
        else:
            xbin.append('<80')

    df['bins'] = xbin

    # Get count of county-point combination
    df = df.groupby(['country', 'bins'], sort=False).size().reset_index(name='freq')

    # Legend size -- should be made into function
    Y = [100, 200, 300, 400, 500]

    # Create heatmap with legend
    fig = make_subplots(rows=1, cols=10, 
                        specs = [[{'colspan' :8}, None, None, None, None, None, None, None, None, {}]],
                        subplot_titles=("Bubble Plot", "Legend"))

    fig.add_trace(go.Scatter(
        x=df['country'], y=df['bins'],
        text=df['freq'],
        mode='markers',
        marker=dict(
            size=df['freq'],
            sizemode='area',
            sizeref=5.*max(df['freq'])/(40.**2),
            sizemin=2,
            color=df['freq'],
            showscale = False)), row=1, col=1)

    fig.add_trace(go.Scatter(
        x = [1.5,1.5,1.5,1.5,1.5],
        y = Y,
        mode= 'markers',
        marker= dict(
        size= Y,
        sizemode= 'area',
        sizeref=5.*max(Y)/(40.**2),
        sizemin=2,
        color=Y,
        showscale = True)), row=1, col=10)

    fig.update_xaxes(linecolor="lightgrey",
                    gridcolor = 'lightgrey',
                    showgrid = True,
                    zeroline = True,
                    showline = True,
                    mirror = True,
                    title_text = "Country", row=1, col=1)
    fig.update_xaxes(zeroline = False, 
                    showline = False, 
                    showticklabels = False, 
                    showgrid = False,
                    tick0 = 1,
                    range = [1,2],
                    rangemode = 'normal', row=1, col=10)
    fig.update_yaxes(linecolor = "lightgrey",
                    gridcolor='lightgrey',
                    showgrid = True,
                    zeroline = True,
                    showline = True,
                    mirror = True,
                    title_text = "Points", row=1, col=1)
    fig.update_yaxes(showgrid = False,
                    tickvals = Y, row=1, col=10)

    fig.update_layout(plot_bgcolor = 'white', showlegend = False, height = 700, width = 1100)

    st.plotly_chart(fig)

else:
    st.write("No CSV Selected Yet")