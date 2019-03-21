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

## Uncomment the following to use external stylesheets instead of the ones
## included in this repository
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__)

# Generate pandas dataframe from data.txt
dfs = parse_data.parse_data()


# FUNCTIONS
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


def get_data():
    dfs = parse_data.parse_data()
    return dfs


# CONTENT
## HEADER
header_children = [
    html.H1(children='SOG Tools'),
    html.Hr(),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000, # in milliseconds
        n_intervals=0,
    ),
]

## FILTERED DATA
filtered_children = [
    html.H2(children='Filtered Data'),
    html.Div(children=[
        html.Div([
            html.H3(children='Select Section'),
            dcc.Dropdown(
                id='section-dropdown',
                options=[{'label': k, 'value': k} for k in dfs.keys()],
                value='TOOLS',
            ),
        ], className="three columns"),
        html.Div([
            html.H3(children='Select SubSection'),
            dcc.Dropdown(id='subsection-dropdown'),
        ], className="three columns"),
        html.Div([
            html.H3(children='Select Item'),
            dcc.Dropdown(id='items-dropdown'),
        ], className="three columns"),
    ], className="row"),
    html.Div(id='display-selected-values', className="centered row"),
    html.Hr(),
]

## ALL DATA
unfiltered_children = [
    html.H2(children='All Data', className="row"),
]
for section in dfs:
    unfiltered_children.append(html.H4(children=section, className="row"))
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
    """
    Filter subsections based on section selection.

    """
    return [{'label': i, 'value': i} for i in dfs[selected_section][1:]]


@app.callback(
    Output('items-dropdown', 'options'),
    [Input('section-dropdown', 'value'),
     Input('subsection-dropdown', 'value')])
def set_items_options(selected_section, selected_subsection):
    """
    Filter items based on section and subsection selections.

    """
    return [{'label': i, 'value': i}
            for i in dfs[selected_section][selected_subsection].unique()]


@app.callback(
    Output('subsection-dropdown', 'value'),
    [Input('subsection-dropdown', 'options')])
def set_subsection_options(available_options):
    """
    Populate default selected subsection.

    """
    return available_options[0]['value']


@app.callback(
    Output('items-dropdown', 'value'),
    [Input('items-dropdown', 'options')])
def set_item_options(available_options):
    """
    Populate default selected item.

    """
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('items-dropdown', 'value'),
     Input('section-dropdown', 'value'),
     Input('subsection-dropdown', 'value')])
def set_display_children(selected_item, selected_section, selected_subsection):
    """
    Build table of filtered data based on selected section, subsection, and item.

    """
    details = dfs[selected_section][dfs[selected_section][selected_subsection] == selected_item]
    return generate_table(details)


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8096, debug=True)
