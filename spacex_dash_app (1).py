# Import required libraries
import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites = np.unique(spacex_df['Launch Site'].to_numpy())

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
                                {'label': sites[0], 'value': sites[0]},
                                {'label': sites[1], 'value': sites[1]},
                                {'label': sites[2], 'value': sites[2]},
                                {'label': sites[3], 'value': sites[3]},
                                ],
                                value='ALL',
                                placeholder="place holder here",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                    100: '100'},
                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Pie Chart of all Sites')
        return fig
    else:
        data = filtered_df[filtered_df['Launch Site']==str(entered_site)]
        class_1 = sum(data['class']==1.0)/len(data['class'])
        class_0 = sum(data['class']==0.0)/len(data['class'])
        fig = px.pie( values=[class_0, class_1], 
        names=['0','1'], 
        title='Pie Chart of %s Site'%entered_site)
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")
              ])
def get_scatter_plot(entered_site, pyaload_entered):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df[filtered_df['Payload Mass (kg)'].between(float(pyaload_entered[0]), float(pyaload_entered[1]))],x = 'Payload Mass (kg)', 
        y='class',
        color='Booster Version Category')
        return fig
    else:
        df = filtered_df[filtered_df['Launch Site']==str(entered_site)]
        df = df[df['Payload Mass (kg)'].between(float(pyaload_entered[0]), float(pyaload_entered[1])) ]
        fig = px.scatter(df,x = 'Payload Mass (kg)', 
        y='class',
        color='Booster Version Category'
        )
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
