# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS_LC'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB_SLC'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC_LC'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS_SLC'}
                                            ],
                                            value='ALL',
                                            placeholder='Select Launch Site',
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000,
                                                step=1000, value=[min_payload, max_payload], allowCross=False),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

mapping = {
            'CCAFS_LC': 'CCAFS LC-40',
            'CCAFS_SLC': 'CCAFS SLC-40',
            'VAFB_SLC': 'VAFB SLC-4E',
            'KSC_LC': 'KSC LC-39A'
        }

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
                    names='Launch Site',
                    title='Total Success Launches per Launch Site')

        return fig
    
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == mapping[entered_site]]['class'].value_counts().reset_index()
        filtered_df.columns = ['class', 'Count']
        fig = px.pie(filtered_df, values='Count',
                    names='class',
                    title='Total Success Launches for Site: ' + mapping[entered_site])
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_chart(entered_site, payload_range):
    range_min = payload_range[0]
    range_max = payload_range[1]

    ranged_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= range_min) &
                          (spacex_df['Payload Mass (kg)'] <= range_max)]

    if entered_site == 'ALL':
        fig = px.scatter(ranged_df, x='Payload Mass (kg)', y='class',
                        color='Booster Version Category',
                        title='Correlation between Payload and Success for all Sites')
        
        return fig

    else:
        filtered_ranged_df = ranged_df[ranged_df['Launch Site'] == mapping[entered_site]]
        fig = px.scatter(filtered_ranged_df, x='Payload Mass (kg)',
                    y='class', color='Booster Version Category',
                    title='Correlation between Payload and Success for Site: ' + mapping[entered_site])
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
