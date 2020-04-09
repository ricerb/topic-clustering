import base64
import datetime
import io
import plotly.graph_objs as go
import numpy as np
from plotly.subplots import make_subplots
import dash_table_experiments as dte

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.H5("Select y-axis"),
    dcc.Dropdown(
        id = 'y-dropdown',
        options = []
        ),
    html.H5("Select x-axis"),
    dcc.Dropdown(
        id = 'x-dropdown',
        options = []
        ),
    dcc.Graph(id='Mygraph'),
    #html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

# update y-dropdown
@app.callback(Output('y-dropdown', 'options'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_y_dropdown(contents, filename):
    if contents is not None:
        contents = contents[0]
        filename = filename[0]
        df = parse_contents(contents, filename)
        columns = list(df.columns.values)
        opts = [ {'label': y, 'value': y} for y in columns ]
        if df is not None:
            return opts
        else:
            return []
    else:
        return []

# update x-dropdown
@app.callback(Output('x-dropdown', 'options'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_x_dropdown(contents, filename):
    if contents is not None:
        contents = contents[0]
        filename = filename[0]
        df = parse_contents(contents, filename)
        columns = list(df.columns.values)
        opts = [ {'label': x, 'value': x} for x in columns ]
        if df is not None:
            return opts
        else:
            return []
    else:
        return []

@app.callback(Output('Mygraph', 'figure'),
            [Input('upload-data', 'filename'),
            Input('upload-data', 'contents'),
            Input('x-dropdown', 'value'),
            Input('y-dropdown', 'value')])
def update_graph(filename, contents, xaxis, yaxis):
    fig = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])}

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_contents(contents, filename)
        df = df[pd.notnull(df[xaxis])]
        df = df[pd.notnull(df[yaxis])]
        df = df.groupby([xaxis, yaxis], sort=False).size().reset_index(name='freq')
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
        legend2 = pd.DataFrame({"yaxis":[df['freq'].min()], 
                    "xaxis":[1.5]}) 
        legend = legend.append(legend2)
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
            '%{xaxis.title.text} : %{x}'+
            '<br>%{yaxis.title.text} : %{y}<br>'+
            'Count: %{text}'), row=1, col=1)

        fig.update_xaxes(linecolor="lightgrey",
                        gridcolor = 'lightgrey',
                       # showticklabels = True,
                     #   type = 'category',
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        mirror = True,
                        automargin = True,
                        title_standoff = 25,
                        dtick = 1,
                        title_text = xaxis, row=1, col=1)

        fig.update_yaxes(linecolor = "lightgrey",
                        gridcolor='lightgrey',
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        automargin = True,
                        mirror = True,
                        dtick = 1,
                        title_text = yaxis,
                      #  title_standoff = 70,
                        tickangle=0, row=1, col=1)

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

        fig.update_xaxes(zeroline = True, 
                        showline = False, 
                        showticklabels = False,
                        showgrid = False,
                        tick0 = 1,
                        range = [1,2],
                        rangemode = 'normal',
                        row=1, col=10)
    
        fig.update_yaxes(showgrid = False,
                        zeroline = True,
                        tickvals = legend['yaxis'],#[0:6],
                        row=1, col=10)

        fig.update_layout(plot_bgcolor = 'white', showlegend = False,
                    #    height = 1300, width = 1300,
                        font=dict(
                                family="Courier New, monospace",
                                size=18,
                                color="black"
                        ),
                        margin=dict(l=120, r=20, t=50, b=20)

        )
    return fig

#    return fig 

#@app.callback(Output('output-data-upload', 'children'),
#              [Input('upload-data', 'contents')],
#              [State('upload-data', 'filename')])

#def update_output(list_of_contents, list_of_names):
#    if list_of_contents is not None:
#        children = [
#            parse_contents(c, n) for c, n in
#            zip(list_of_contents, list_of_names)]
#        return children



if __name__ == '__main__':
    app.run_server(debug=True)