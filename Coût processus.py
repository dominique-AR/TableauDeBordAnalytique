# Importation des modules
#from pathlib import Path
import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from tba_path import p

dash.register_page(__name__, path="/cout_processus", order=3)

# Importation des données de SAARI
ds_tba_rep = pd.read_excel(p/'BA_CHARGES.xlsx',
                           sheet_name='vent_cout_mrg')
ds_tba_cout_par_pr = pd.read_excel(p/'BA_CHARGES.xlsx',
                                   sheet_name='cout_processus')
ds_tba_cp_rb = pd.read_excel(p/'BA_CHARGES.xlsx',
                             sheet_name='vent_cp_real_bgt')

# Données pour la répartition coût et marges par rapport aux redevances : 2022
valeurs = ds_tba_rep['Valeurs']

# Données pour la répartition coût et marges par rapport aux redevances : 2022
proc = ds_tba_cout_par_pr['PROCESSUS']
c_proc = ds_tba_cout_par_pr['Cout_Processus']

# Données pour la ventilation des coûts budgétisés vs réels : 2022
rub = ds_tba_cp_rb['Rubriques']
cout_bgt = ds_tba_cp_rb['Budget']
cout_real = ds_tba_cp_rb['Réalisations']
now = datetime.date(datetime.now())
date_edition = now.strftime("%m/%d/%Y")

# Création figure1
fig1 = px.pie(ds_tba_rep, values=valeurs, names='PROCESSUS', title='Ventilation des redevances en % : 2022')

# Création figure2
fig2 = px.pie(ds_tba_cout_par_pr, values=c_proc, names='PROCESSUS', title='Coûts des processus en % : 2022')

# Création figure3
fig3 = px.bar(ds_tba_cp_rb,
              x=rub,
              y=cout_bgt,
              title='Coût de revient : Budget (en vert) par rapport aux Réalisations (couleur '
                    'signal)',
              color_discrete_sequence=['#00FE35'] * len(ds_tba_cp_rb),
              )
fig3.add_trace(go.Bar(name='Echelle des écarts : Réalisations/Budgets',
                      x=rub,
                      y=cout_real,
                      marker=dict(
                          color=abs((cout_real - cout_bgt) / cout_bgt),
                          colorscale="RdYlGn_r",
                          showscale=True
                      )
                      ))
fig3.update_layout(barmode='group', xaxis_title='Périodes', yaxis_title='Montant en Mio AR',     legend=dict(
        x=1.02,  # Position the legend to the right of the chart
        y=-0.1,  # Position the legend vertically centered in the chart
        orientation='v',  # Display the legend vertically
        bgcolor='rgba(255, 255, 255, 0.5)',  # Set the background color of the legend to white with 50% transparency
        bordercolor='gray',  # Set the border color of the legend to gray
        borderwidth=1,  # Set the border width of the legend to 1 pixel
        font=dict(  # Set the font style of the legend
            family='sans-serif',
            size=12,
            color='black'
        )))

dropdown_options = [
    {'label': 'Ventilation des processus en %: 2022', 'value': 'fig1'},
    {'label': 'Coûts des processus en % : 2022', 'value': 'fig2'}
]

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.P('Elements graphiques indicatifs des Coûts de processus', style={'color': 'red',
                                                                       'margin': '0',
                                                                       'padding': '0',
                                                                       'font-weight': 'bold',
                                                                       'font-size': '15px',
                                                                       'text-align': 'left',
                                                                       'display': 'block'}),
                    width=8,
                )], style={'paddingTop': '20px'}),
        dbc.Row([dbc.Col(
                    html.P(f'Edition du : {date_edition}', style={'color': 'black',
                                                                  'margin': 'auto',
                                                                  'padding': '0',
                                                                  'font-weight': 'bold',
                                                                  'font-size': '12px',
                                                                  'text-align': 'left',
                                                                  'display': 'inline'}),
                    width=12,)], style={'padding-bottom': '25px'},
           
        ),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown',
                    options=dropdown_options,
                    value='fig1')
            ], width=9)]),
        dbc.Row([dbc.Col([
                dcc.Graph(id='pie-chart')
            ], width=9)
        ]),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='comp_cout', figure=fig3),
                    style={'display': 'block'},
                    width=12)

            ],
            justify='center',
            align='center',
            style={'paddingTop': '10px'}
        ),
    ],
    fluid=True,
)


# create the callback
@callback(
    Output('pie-chart', 'figure'),
    Input('dropdown', 'value')
)
def update_pie_chart(selected_value):
    if selected_value == 'fig1':
        fig = fig1
    else:
        fig = fig2
    return fig


"""

dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown('#  AGETIPA: TABLEAU DE BORD  ANALYTIQUE'),
                    width={'size': 6, 'offset': 3}
                ),
                dbc.Col(
                    html.Img(src='/assets/logo.png'),
                    width=3,
                ),
            ],
            justify='center',
            align='center',
            style={'paddingTop': '50px'}
        ),

layout = html.Div(children=[
    html.Img(src='../assets/logo.png', style={'display': 'inline'}),
    html.P(children="TABLEAU DE BORD ANALYTIQUE: Coût des processus", style={'color': 'red',
                                                                             'margin': '0',
                                                                             'padding': '0',
                                                                             'font-weight': 'bold',
                                                                             'font-size': '40px',
                                                                             'text-align': 'center',
                                                                             'display': 'block'}),
    html.P(children="Données : Exercice en cours", style={'color': 'black',
                                                          'margin': '0',
                                                          'padding': '0',
                                                          'font-weight': 'bold',
                                                          'font-size': '15px',
                                                          'text-align': 'left',
                                                          'display': 'inline'}),
    html.P(children="Données cumulées : Depuis 2017", style={'color': 'black',
                                                             'margin': '0',
                                                             'padding': '0',
                                                             'font-weight': 'bold',
                                                             'font-size': '15px',
                                                             'text-align': 'left',
                                                             'display': 'block'}),
    html.P(children="Edition du : ", style={'color': 'black',
                                            'margin': '0',
                                            'padding': '0',
                                            'font-weight': 'bold',
                                            'font-size': '15px',
                                            'text-align': 'left',
                                            'display': 'inline'}),
    html.P(children=date_edition, style={'color': 'black',
                                         'margin': 'auto',
                                         'padding': '0',
                                         'font-weight': 'bold',
                                         'font-size': '15px',
                                         'text-align': 'left',
                                         'display': 'inline'}),
    html.Div(style={'display': 'block'},
             children=[
                 html.Div(children=[
                     dcc.Graph(
                         id='rep_red',
                         figure=fig1
                     )
                 ])
             ]),
    html.Div(style={'display': 'block'},
             children=[
                 html.Div(children=[
                     dcc.Graph(
                         id='c_processus',
                         figure=fig2
                     )
                 ])
             ]),
    html.Div(style={'display': 'block'},
             children=[
                 html.Div(children=[
                     dcc.Graph(
                         id='comp_cout',
                         figure=fig3
                     )
                 ])
             ]),

])

"""
