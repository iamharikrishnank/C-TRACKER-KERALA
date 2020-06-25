import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests

url = 'https://keralastats.coronasafe.live/hotspots.json'
r = requests.get(url)
x = r.json()
df=pd.DataFrame(x['hotspots'])
def generate_table(dataframe, max_rows=len(df)):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H4(children='Hot spots in Kerala'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in df.district.unique()
    ], multi=True, placeholder='Filter by district...'),
    html.Div(id='table-container')
])

@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):
    if dropdown_value is None:
        return generate_table(df)

    dff = df[df.district.str.contains('|'.join(dropdown_value))]
    return generate_table(dff)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
