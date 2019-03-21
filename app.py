"""
Dash App - Interactive SOG Tool data

"""
# Generic Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd


# Custom Imports
import parse_data


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__)

dfs = parse_data.parse_data()

def generate_table(dataframe, max_rows=10):
    """
    Generate a table from a pandas dataframe.

    This code borrowed from dash tutorial.

    """
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# HEADER
header_children = [
    html.H1(children='SOG Tools'),
    html.Hr(),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000, # in milliseconds
        n_intervals=0,
    ),
]

# FILTERED DATA
filtered_children = [
    html.H2(children='Filtered Data'),
    html.Div([
        html.H3(children='Select Section'),
        dcc.Dropdown(
            id='section-dropdown',
            options=[{'label': k, 'value': k} for k in dfs.keys()],
            value='TOOLS',
        ),
    ], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
    ], style={'width': '.5%', 'display': 'inline-block'}),
    html.Div([
        html.H3(children='Select SubSection'),
        dcc.Dropdown(id='subsection-dropdown'),
    ], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
        html.H3(children='Select Item'),
        dcc.Dropdown(id='items-dropdown'),
    ], style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),
    html.Div(id='display-selected-values'),
    html.Hr(),
]

# ALL DATA
unfiltered_children = [
    html.H2(children='All Data'),
]
for section in dfs:
    unfiltered_children.append(html.H4(children=section))
    unfiltered_children.append(generate_table(dfs[section]))

# LAYOUT
app.layout = html.Div([
    html.Div(children=header_children + filtered_children + unfiltered_children),
    html.Hr(),
])


# CALLBACKS
@app.callback(
    Output('subsection-dropdown', 'options'),
    [Input('section-dropdown', 'value')])
def set_section_options(selected_section):
    return [{'label': i, 'value': i} for i in dfs[selected_section][1:]]


@app.callback(
    Output('items-dropdown', 'options'),
    [Input('section-dropdown', 'value'),
     Input('subsection-dropdown', 'value')])
def set_items_options(selected_section, selected_subsection):
    return [{'label': i, 'value': i}
            for i in dfs[selected_section][selected_subsection].unique()]


@app.callback(
    Output('subsection-dropdown', 'value'),
    [Input('subsection-dropdown', 'options')])
def set_subsection_options(available_options):
    return available_options[0]['value']


@app.callback(
    Output('items-dropdown', 'value'),
    [Input('items-dropdown', 'options')])
def set_item_options(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('items-dropdown', 'value'),
     Input('section-dropdown', 'value'),
     Input('subsection-dropdown', 'value')])
def set_display_children(selected_item, selected_section, selected_subsection):
    details = dfs[selected_section][dfs[selected_section][selected_subsection] == selected_item]
    return generate_table(details)


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8096, debug=True)
