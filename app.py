import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

import plotly.graph_objs as go
df = pd.read_csv('covid.csv')
pv = pd.pivot_table(df, index=['location'], columns=["continent"], values=['total_cases'], aggfunc=sum, fill_value=0)
trace1 = go.Bar(x=df["continent"], y=df[('total_cases')], name='Asia')
trace2 = go.Bar(x=df["continent"], y=pv[('total_cases')], name='Eu')
trace3 = go.Bar(x=df["continent"], y=pv[('total_cases')], name='Af')
trace4 = go.Bar(x=df["continent"], y=pv[('total_cases')], name='NA')
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(children=[
    html.H1(children='Sales Funnel Report'),
    html.Div(children='''National Sales Funnel Report.'''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1],
            'layout':
            go.Layout(title='Order Status by Customer', barmode='stack')
        })
])
if __name__ == '__main__':
    app.run_server(debug=True)
