import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd
import os
from dash.dependencies import Input, Output

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go


energy_df = pd.read_csv('https://raw.githubusercontent.com/RaphaelNash/CUNY-DATA-608-VisualAnalytics/master/Final/Energy.csv')
energy_df.columns =['year', 'state', 'type', 'source', 'consumption']
energy_df['source'] = energy_df['source'].str.lower()
energy_df['state'] = energy_df['state'].str.upper()
energy_df = energy_df.loc[energy_df['type']=='Total Electric Power Industry']


states = energy_df.state.unique()

states_list_for_dropdown = []

for state in states:
    d = {}
    d['label'] = state
    d['value'] = state
    states_list_for_dropdown.append(d)


def set_layout_dict (title):
    return dict(
        title = title,

        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),

        )
def set_data_dict(    states , energy_consumption):
    scl = [[0.0, 'rgb(242,240,247)'],
        [0.2   , 'rgb(165,0,38)'],
        [0.4  , 'rgb(215,48,39)'],
        [0.6  , 'rgb(253,174,97)'],
        [0.8  , 'rgb(254,224,144)'],
        [1.0 , 'rgb(171,217,233)']]


    data = [ dict(
        type='choropleth',
        colorscale = scl,
        showscale = False,
        autocolorscale = False,
        locations = states,
        z = energy_consumption.astype('float'),
        locationmode = 'USA-states',
        #text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) )
        ) ]

    return data

def get_data_for_cloropeth(year, energy_type):

    df_for_energy = pd.DataFrame()

    energy_year_df = energy_df.loc[energy_df['year'] == year]

    if energy_type == 'coal':
        df_for_energy = energy_year_df.loc[energy_year_df['source']=='coal (short tons)']

    if energy_type == 'geo':
        df_for_energy = energy_year_df.loc[energy_year_df['source']=='geothermal (billion btu)']

    if energy_type == 'nat_gas':
        df_for_energy = energy_year_df.loc[energy_year_df['source']=='natural gas (mcf)']

    if energy_type == 'other':
        df_for_energy = energy_year_df.loc[energy_year_df['source']=='other gases (billion btu)']

    if energy_type == 'petro':
        df_for_energy = energy_year_df.loc[energy_year_df['source']=='petroleum (barrels)']

    return df_for_energy



def create_cloropeth_coal(year):

    energy_coal = get_data_for_cloropeth(year, 'coal')
    figure = dict( data=set_data_dict(energy_coal['state'], energy_coal['consumption'] ) ,
                     layout=set_layout_dict('Coal (Short Tons)' ))

    return figure

def create_cloropeth_nat_gas(year):


    energy_nat_gas = get_data_for_cloropeth (year, 'nat_gas')
    figure = dict( data=set_data_dict(energy_nat_gas['state'], energy_nat_gas['consumption']  ),
                        layout=set_layout_dict('Natural Gas (Mcf)') )

    return figure

def create_cloropeth_petro(year):


    energy_petro = get_data_for_cloropeth(year, 'petro')
    figure = dict( data=set_data_dict(energy_petro['state'], energy_petro['consumption']  ),
                        layout=set_layout_dict('Petroleum (Barrels)') )

    return figure

def create_cloropeth_geo(year):


    energy_geo = get_data_for_cloropeth(year, 'geo')
    figure = dict( data=set_data_dict(energy_geo['state'], energy_geo['consumption']  ),
                        layout=set_layout_dict('Geothermal (Billion Btu)') )

    return figure



def create_cloropeth_other(year):


    energy_other_gas = get_data_for_cloropeth(year, 'other')

    figure = dict( data=set_data_dict(energy_other_gas['state'], energy_other_gas['consumption']  ),
                        layout=set_layout_dict('Other Gases (Billion Btu)') )

    return figure


def create_cloropeth(year):

    return create_cloropeth_coal(year),\
           create_cloropeth_nat_gas(year), \
           create_cloropeth_petro(year), \
           create_cloropeth_geo(year), \
           create_cloropeth_other(year)




def create_state_subplots(state):

    energy_curr_state = energy_df.loc[energy_df['state'].str.contains(state)]

    trace1 = go.Scatter(
        y=energy_curr_state.loc[energy_curr_state['source']=='coal (short tons)']['consumption'],
        x=energy_curr_state.loc[energy_curr_state['source']=='coal (short tons)']['year'],
        name = 'Coal (Short Tons'
    )
    trace2 = go.Scatter(
        y=energy_curr_state.loc[energy_curr_state['source']=='geothermal (billion btu)']['consumption'],
        x=energy_curr_state.loc[energy_curr_state['source']=='geothermal (billion btu)']['year'],
        name = 'Geothermal (Billion Btu)'
    )

    trace3 = go.Scatter(
        y=energy_curr_state.loc[energy_curr_state['source']=='natural gas (mcf)']['consumption'],
        x=energy_curr_state.loc[energy_curr_state['source']=='natural gas (mcf)']['year'],
        name = 'Natural Gas (Mcf)'
    )

    trace4 = go.Scatter(
        y=energy_curr_state.loc[energy_curr_state['source']=='other gases (billion btu)']['consumption'],
        x=energy_curr_state.loc[energy_curr_state['source']=='other gases (billion btu)']['year'],
        name = 'Other Gases (Billion BTU)'
    )
    trace5 = go.Scatter(
        y=energy_curr_state.loc[energy_curr_state['source']=='petroleum (barrels)']['consumption'],
        x=energy_curr_state.loc[energy_curr_state['source']=='petroleum (barrels)']['year'],
        name = 'Petroleum (Barrels)'
    )

    fig = tools.make_subplots(rows=5, cols=1, shared_xaxes=True)

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 3, 1)
    fig.append_trace(trace4, 4, 1)
    fig.append_trace(trace5, 5, 1)

    fig['layout'].update(height=768, width=1024, title='')

    return fig


fig = create_state_subplots('US')

app = dash.Dash()

fig_map_coal, fig_natgas_map, fig_petro_map, fig_geo_map, fig_other_gas_map = create_cloropeth(1990)

app.layout = html.Div([
    dcc.Tabs(
        tabs=[
             {'label': '1. Overview', 'value': 3},
            {'label': '2. Energy Input Cholorpeths', 'value': 1} ,
             {'label': '3. Energy Inputs Time Varying', 'value': 2}
        ],
        value=3,
        id='tabs'
    ),
    html.Div(id='tab-output', className = 'container')
], style={
    'width': '100%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})





def display_maps():

    return html.Div([



        html.Div (
        [ ], className = 'Row' , ),

        html.Div ([
            html.Div ([
                dcc.Graph(animate=True,
                    id='coal_map'#,
                    #figure=fig_map_coal
                )  ,
                ], className = "five columns"),

            html.Div ([
                dcc.Graph(
                    id='nat_gas_map'#,
                    #figure=fig_natgas_map
                )], className = "five columns"),

    ], className = "row"),

     html.Div ([
            html.Div ([
                dcc.Graph(
                    id='petro_map'
                    #,
                    #figure=fig_petro_map
                )  ,
                ], className = "five columns"),

            html.Div ([
                dcc.Graph(
                    id='other_gas_map'
                    #,
                    #figure=fig_other_gas_map
                )], className = "five columns"),

    ], className = "row"),

         html.Div ([
            html.Div ([
                dcc.Graph(
                    id='fig_geo_map'
                    #,
                    #figure=fig_geo_map
                )  ,
                ], className = "five columns")



    ], className = "row"),

           html.Div (
        [
            html.Div ([], className = "one columns") ,
             html.Div ([dcc.Slider( id = 'slider',
                    min=1990,
                    max=2016,
                    step=2,
                marks =  {i: '{}'.format(i) for i in range(1990, 2016,2)},

                    value=1990,
)], className = "ten columns" ) ,
            html.Div ([], className = "") ,

        ], className = 'row', id= 'outer-slider',




    ),
],  )


def display_overview():
    return html.Div([
           dcc.Markdown('''
### Consumption of Enery Inputs for Electricity

##### CUNY DATA 608 Visual Analytics
##### Raphael Nash


This project explorers how various energy inputs have changed overtime.  This inspiration of this project was President 
Donald Trump's proclimations that Former President Barak Obama's policies killed coal in the United States. It is pretty 
well established that Natural Gas has been winning out over coal due to the cost of natural gas due to increase 
domestic production of natural gas.    
 For reference
the terms of the last several presidents are as follows:


1. 2017- present: Donald Trump (R) 
2. 2009-2017: Barak Obama (D)
3. 2001-2009: George W. Bush (R)
4. 1993-2001: Bill Clinton (D)
5. 1989- 1993: George H.W. Bush (R) 


#### Tab 2: " Energy Input Cholorpeths"

This tab has 5 cloropeths.  The cloropeths represent each of the 5 major inputs to U.S. electircal production.
They colors are wihin each cloropeth to what state uses more or less of that input.  The brighter red the more of that 
input the state uses.  the cloropeths are not comparable to each other.  There is a range slider at the bottom of the 
page so you can see how each states proportion changes over time.


#### Tab 3:  "Energy Inputs Time Varying" 

This tab thas line graphs that shows the change of each input overtime.   The tab opens with totals for the U.S. however;
you can.

#### Conclusions

One of the main take aways is that coal peaks around 2000 while natural gas steadily rises from 1990-present.  2000 is 
Bill Clintons last year in office and George W. Bush took over in 2001.   


#### Notes

The data is from the US Energy information agency.  

Source URL: https://www.eia.gov/electricity/data.php#consumption


File is a csv download from the tab "Consumption of fuels used to generate electricity" and is the 
file titled "Annual (Back to 1990).

The only transform that was done outside of python was to convert the excel to csv.   I only select the rows
where type of "Type of Producer" == "Total Electric Power Industry".  




 
''')
        ], style={'marginBottom': 50, 'marginTop': 25})




def display_subplots():
    return html.Div(children=[
    html.H1(children=''),

    html.Div(children='''
        Select A State:.
    '''),


    dcc.Dropdown(
        id='state-select',
        options = states_list_for_dropdown,

        value ='US-TOTAL'

    ),

    dcc.Graph(
        id='energy-subplots',
        figure=fig
    )


])

app.config['suppress_callback_exceptions']=True

@app.callback(
    dash.dependencies.Output('energy-subplots', 'figure'),
    [dash.dependencies.Input('state-select', 'value')])
def update_output(value):
    return create_state_subplots(value)


@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    if value == 2:
        return display_subplots()
    elif value == 1:
        return display_maps()
    else:
        return display_overview();

@app.callback(
    dash.dependencies.Output('coal_map', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_output(value):
    return create_cloropeth_coal(value)
@app.callback(
    dash.dependencies.Output('nat_gas_map', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_output(value):
    return create_cloropeth_nat_gas(value)
@app.callback(
    dash.dependencies.Output('petro_map', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_output(value):
    return create_cloropeth_petro(value)
@app.callback(
    dash.dependencies.Output('other_gas_map', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_output(value):
    return create_cloropeth_other(value)
@app.callback(
    dash.dependencies.Output('fig_geo_map', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_output(value):
    return create_cloropeth_geo(value)

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':

      app.run_server(debug=True, host='0.0.0.0')
