import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots 
import streamlit as st
import os
from math import log10, floor

# Wine rating data set
#df = pd.read_csv("winemag-data_first150k.csv")

# function definitions
def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

# Initialize variables for if statements
df = None
xaxis = None
yaxis = None 


# Start of script
_max_width_()
st.title('BubblePlot')

uploaded_file = st.file_uploader("Choose a CSV file", type = "csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if st.checkbox('Show raw data'):
        st.subheader('Uploaded Data')
        st.write(df)

if df is not None:
    # Remove rows where country was not reported
    xaxis = st.selectbox("Select x-axis to graph", list(df.columns.values))
    yaxis = st.selectbox("Select y-axis to graph", list(df.columns.values))

    if xaxis is not None and yaxis is not None:
        df = df[pd.notnull(df[xaxis])]
        df = df[pd.notnull(df[yaxis])]


        # Get count of county-point combination
        df = df.groupby([xaxis, yaxis], sort=False).size().reset_index(name='freq')

        # Create legend based on bubble plot data -- uglistest thing I've ever written, also might be wrong  
        df['binned'] = pd.cut(np.array(df['freq']), 5, precision = 0)
        legend = pd.DataFrame(df['binned'].unique(), columns = ['binned'])
        legend['binned'] = legend['binned'].astype('str') 
        legend = legend['binned'].str.split(", ", n = 1, expand = True)
        legend = legend[1].str.split("]", n = 1, expand = True) 
        legend = legend[0].str.split(".0", n=1, expand = True)
        legend[0] = legend[0].astype('str')
        legend[0] = legend[0].astype('float')
        yval = list(legend[0])
        legend = pd.DataFrame(yval, columns = ['yaxis'])
        legend['xaxis']= 1.5
       
        # Create bubble plot with legend
        fig = make_subplots(rows=1, cols=10, 
                            specs = [[{'colspan' :8}, None, None, None, None, None, None, None, None, {}]],
                            subplot_titles=("Bubble Plot", "Legend (Count)"))
        # Bubble plot code
        fig.add_trace(go.Scatter(
            x=df[xaxis], y=df[yaxis],
            text=df['freq'],
            mode='markers',
            marker=dict(
                size=df['freq'],
                sizemode='area',
                sizeref=4.*max(df['freq'])/(40.**2),
                sizemin=2,
                color=df['freq'],
                showscale = False),
            hovertemplate =
            '%{x}'+
            '<br>%{y}<br>'+
            'Count:%{text}'), row=1, col=1)

        fig.update_xaxes(linecolor="lightgrey",
                        gridcolor = 'lightgrey',
                       # showticklabels = True,
                     #   type = 'category',
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        mirror = True,
                        title_text = xaxis, row=1, col=1)

        fig.update_yaxes(linecolor = "lightgrey",
                        gridcolor='lightgrey',
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        mirror = True,
                        title_text = yaxis, row=1, col=1)

        # Legend figure code 
        fig.add_trace(go.Scatter(
            x = legend['xaxis'],
            y = legend['yaxis'],
            mode= 'markers',
            marker= dict(
            size= legend['yaxis'],
            sizemode= 'area',
            sizeref=4.*max(legend['yaxis'])/(40.**2),
            sizemin=2,
            color=legend['yaxis'],
            showscale = True),
            hoverinfo='none'), row=1, col=10)

        fig.update_xaxes(zeroline = False, 
                        showline = False, 
                        showticklabels = False, 
                        showgrid = False,
                        tick0 = 1,
                        range = [1,2],
                        rangemode = 'normal', row=1, col=10)
    
        fig.update_yaxes(showgrid = False,
                        tickvals = legend['yaxis'][0:5],
                        row=1, col=10)

        fig.update_layout(plot_bgcolor = 'white', showlegend = False,
                        height = 1300, width = 1300,
                        font=dict(
                                family="Courier New, monospace",
                                size=18,
                                color="black"
        ))

        st.subheader("Bubble Plot")
        st.plotly_chart(fig)

    else:
        st.write("No CSV Selected Yet")

