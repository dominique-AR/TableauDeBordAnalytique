# Importation des modules
from pathlib import Path
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from tba_path import p

dash.register_page(__name__, path="/marges", order=1)

logo_path = '../assets/logo.png'

# Importation des données de SAARI
ds_tba = pd.read_excel(p/'BA_CHARGES.xlsx', sheet_name='calcul_marge')
ds_tba_prj = pd.read_excel(p/'BA_CHARGES.xlsx', sheet_name='marge_projets')
ds_tba_pj_cum = pd.read_excel(p/'BA_CHARGES.xlsx', sheet_name='marge_pj_cum3')
ds_tba_prj_tf = pd.read_excel(p/'BA_CHARGES.xlsx', sheet_name='marge_pjt_tf')
ds_tba_pj_cum_tf = pd.read_excel(p/'BA_CHARGES.xlsx', sheet_name='marge_pj_cum3_tf')

# Détermination des variables issues des données extraites de SAARI
# Données pour le calcul des marges exercice et cumulées
display_value = ds_tba.iloc[3]['Exercice'] * 100
marge_pc_gb = ds_tba.iloc[3]['Cumulé 6 ans'] * 100
title_gauge_ex = 'Marge globale en % : Exercice en cours'
title_gauge_cum = 'Marge globale cumulée depuis 2017 en %'
delta_ref = ds_tba.iloc[4]['Exercice'] * 100
ths = ds_tba.iloc[5]['Exercice'] * 100

# Données pour le calcul des marges par projet
prjts = ds_tba_prj['Projets']
marge_pjt = ds_tba_prj['Marges_V']
marge_s = ds_tba_prj['Marges_S'] * 100
couleur_pj = ds_tba_prj['Color']

# Données pour le calcul des marges cumulées par projet
prjts_c = ds_tba_pj_cum['Projets']
marge_pjt_c = ds_tba_pj_cum['Marges_P'] * 100
marge_sc = ds_tba_pj_cum['Marges_S'] * 100
couleur_pc = ds_tba_pj_cum['Color']


# Fonction de traitement des gauges pour marge sur coût de revient
def affichage_gauge(display_v, title, delta, threshold):
    figs = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=display_v,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 25}},
        delta={'reference': delta, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 50], 'tickwidth': 0.2, 'tickcolor': "black"},
            'bar': {'color': "black", 'thickness': 0.35},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#66FF00",
            'steps': [
                {'range': [0, 25], 'color': '#FF0000'},
                {'range': [25, 35], 'color': 'yellow'},
                {'range': [35, 50], 'color': '#66FF00'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 1,
                'value': threshold}}))
    figs.update_layout(paper_bgcolor="lavender", font=dict(color="darkblue", family="Arial"))
    return figs
    # figs.show()


# Traitement marge par projet
title_histo_pjt = "Marge par projet de l'exercice en cours"
fig_p = px.bar(ds_tba_prj,
               x=prjts,
               y=marge_pjt,
               color=couleur_pj,
               title=title_histo_pjt,
               color_discrete_map={
                   'Négatif': '#FF0000',
                   'Positif': '#00FF66'
               })
# fig_p.add_trace(go.Scatter(x=prjts, y=marge_s, fillcolor='#FF6600', name='Marge seuil en %'))
fig_p.update_layout(xaxis_title='PROJETS', yaxis_title='Marge en Mio AR')
# fig_p.show()

# Traitement marge cumulée depuis 2017 par projet
title_histo_c3 = "Marge cumulée par projet : BASE 2017"
fig_c = px.bar(ds_tba_pj_cum,
               x=prjts_c,
               y=marge_pjt_c,
               color=couleur_pc,
               title=title_histo_c3,
               color_discrete_map={
                   'Négatif': '#FF0000',
                   'Positif': '#00FF66'
               })
fig_c.add_trace(go.Scatter(x=prjts_c, y=marge_sc, fillcolor='#FF6600', name='Marge seuil en %'))
fig_c.update_layout(xaxis_title='PROJETS', yaxis_title='Marge en %')
# fig_c.show()

# Présentation table récapitulative : Données de l'exercice
title_tab_ex = "Tableau récapitulatif de l'exercice en cours"
fig_t = go.Figure(data=[go.Table(
    header=dict(values=list(ds_tba_prj_tf.columns),
                fill_color='green',
                align='center',
                font=dict(color='white', size=14, family='Arial')),  # bold white font),
    cells=dict(values=[ds_tba_prj_tf.Projets,
                       ds_tba_prj_tf.Redevances,
                       ds_tba_prj_tf.Couts,
                       ds_tba_prj_tf.Marges_V,
                       ds_tba_prj_tf.Marges_P],
               fill_color='#f9f9f9',
               font=dict(color='black'),
               align=['center', 'right', 'right', 'right', 'center'],
               format=["", ",.0f", ",.0f", ",.0f", ".1%"]))
])
fig_t.update_layout(dict(title=title_tab_ex))
# fig_t.show()

# Présentation table récapitulative : Données cumulées 2017 - 2022
title_tab_cum3 = "Tableau cumulé : Base 2017"
fig_t_c = go.Figure(data=[go.Table(
    header=dict(values=list(ds_tba_pj_cum_tf.columns),
                 fill_color='green',
                align='center',
                font=dict(color='white', size=14, family='Arial')),
    cells=dict(values=[ds_tba_pj_cum_tf.Projets,
                       ds_tba_pj_cum_tf.Redevances,
                       ds_tba_pj_cum_tf.Couts,
                       ds_tba_pj_cum_tf.Marges_V,
                       ds_tba_pj_cum_tf.Marges_P],
               fill_color='#dfe3ee',
               align=['center', 'right', 'right', 'right', 'center'],
               format=["", ",.0f", ",.0f", ",.0f", ".1%"]))
])
fig_t_c.update_layout(dict(title=title_tab_cum3))
# fig_t_c.show()

fig_g_mg = affichage_gauge(display_v=display_value, title=title_gauge_ex, delta=delta_ref, threshold=ths)
fig_g_mgc = affichage_gauge(display_v=marge_pc_gb, title=title_gauge_cum, delta=delta_ref, threshold=ths)
now = datetime.date(datetime.now())
date_edition = now.strftime("%m/%d/%Y")

# Element d'affichage du dropdown pour les jauges
options = [
    {'label': "Marge globale de l'exercice en cours: en %", 'value': 'fig_g_mg'},
    {'label': "Marge globale cumulée depuis 2017 en %", 'value': 'fig_g_mgc'}
]
# presentation de la page
layout = dbc.Container(
    [
        dbc.Row(children=[
            html.P("Elements graphiques de l'analyse des Marges", style={'color': 'red',
                                                'margin': '0',
                                                'padding': '0',
                                                'font-weight': 'bold',
                                                'font-size': '15px',
                                                'text-align': 'left',
                                                'display': 'block', 'paddingTop': '20px'}),
            html.Br()
        ]),
        dbc.Row(children=[
            html.P(f'Edition du : {date_edition}', style={'color': 'black',
                                                              'margin': '0',
                                                              'padding': '0',
                                                              'font-weight': 'bold',
                                                              'font-size': '12px',
                                                              'text-align': 'left',
                                                              'display': 'inline', 'padding-bottom': '25px'}),
            html.Br()]),
        dbc.Row(
            html.Div(children=[
                dcc.Dropdown(id='j_dropdown', options=options, value='fig_g_mg'),
                dcc.Graph(id='Gauge')])),
        dbc.Row(children=[
            html.Br(),
            html.Div(style={'display': 'block'},
                     children=[
                         dcc.Graph(
                             id='marge_par_pjt',
                             figure=fig_p
                         )
                     ]),
            html.Div(style={'display': 'block'},
                     children=[
                         dcc.Graph(
                             id='marge_cum3_par_pjt',
                             figure=fig_c
                         )
                     ]),
            html.Div(style={'display': 'block',
                            'margin': '0px',
                            'padding': '0px'},
                     children=[
                         dcc.Graph(
                             id='tableau_ex',
                             figure=fig_t
                         )
                     ]),
            html.Br(),
            html.Div(style={'display': 'block',
                            'margin': '0px',
                            'padding': '0px'},
                     children=[
                         dcc.Graph(
                             id='tableau_cum3',
                             figure=fig_t_c
                         )]
                     )])
    ], fluid=True)


@callback(
    Output('Gauge', 'figure'),
    Input('j_dropdown', 'value')
)
def update_Gauge(value):
    if value == 'fig_g_mg':
        figure = fig_g_mg
    else:
        figure = fig_g_mgc
    return figure

    """
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

    html.P(children=, style={'color': 'black',
                                         'margin': 'auto',
                                         'padding': '0',
                                         'font-weight': 'bold',
                                         'font-size': '15px',
                                         'text-align': 'left',
                                         'display': 'inline'}),
    html.Div(style={'display': 'block'},
             children=[
                 dcc.Graph(
                     id='marge_ex',
                     figure=fig_g_mg
                 )
             ]),
    html.Div(style={'display': 'block'},
             children=[
                 dcc.Graph(
                     id='marge_cum3',
                     figure=fig_g_mgc
                 )
             ]),
    html.Br(),
    html.Div(style={'display': 'block'},
             children=[
                 dcc.Graph(
                     id='marge_par_pjt',
                     figure=fig_p
                 )
             ]),
    html.Div(style={'display': 'block'},
             children=[
                 dcc.Graph(
                     id='marge_cum3_par_pjt',
                     figure=fig_c
                 )
             ]),
    html.Div(style={'display': 'block',
                    'margin': '0px',
                    'padding': '0px'},
             children=[
                 dcc.Graph(
                     id='tableau_ex',
                     figure=fig_t
                 )
             ]),
    html.Br(),
    html.Div(style={'display': 'block',
                    'margin': '0px',
                    'padding': '0px'},
             children=[
                 dcc.Graph(
                     id='tableau_cum3',
                     figure=fig_t_c
                 )
             ]),
])

"""


"""
    """
