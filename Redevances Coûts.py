from pathlib import Path
import dash
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from tba_path import p

dash.register_page(__name__, path="/redevances_et_cout", order=2)


# Importation des données de SAARI
ds_tba = pd.read_excel(p/'pages'/'BA_CHARGES_details.xlsx', sheet_name='evolution_2017')
ds_tba_ev_R = pd.read_excel(p/'pages'/'BA_CHARGES_details.xlsx', sheet_name='evol_Redv_2017')
ds_tba_ev_CR = pd.read_excel(p/'pages'/'BA_CHARGES_details.xlsx', sheet_name='evol_Cout_2017')

# Données pour Redevances et Coût de revient : Réalisations Fig 1 & 2
periode = ds_tba['Années']
redevances = ds_tba['Redevances']
c_revient = ds_tba['Coût de revient']
couleur_pc = ds_tba['Color']

now = datetime.date(datetime.now())
date_edition = now.strftime("%m/%d/%Y")

# Données pour le calcul evolution annuelle des redevances Fig 3
per_eR = ds_tba_ev_R['Années']
red_eR = ds_tba_ev_R['Redevances_R']
red_eB = ds_tba_ev_R['Redevances_Bgt']

# Données pour le calcul evolution annuelle des coût de revient Fig 4
per_eC = ds_tba_ev_CR['Années']
red_eCr = ds_tba_ev_CR['Cout_Revient_R']
red_eCb = ds_tba_ev_CR['Cout_Revient_Bgt']

# Création figure1
fig_p = px.bar(ds_tba,
               x=periode,
               y=redevances,
               title='Evolution annuelle des Redevances (en vert) et Coût de revient (couleur signal) : Réalisations',
               color_discrete_sequence=['#00FE35'] * len(ds_tba),
               )
fig_p.add_trace(go.Bar(name='Echelle des écarts : Redevances/Coût de revient',
                       x=periode,
                       y=c_revient,
                       textposition="outside",  # Set the text position to 'outside'
                       marker=dict(
                           color=abs((redevances - c_revient) / redevances),
                           colorscale="RdYlGn_r",
                           showscale=True
                       )
                       ))
fig_p.update_layout(barmode='group', xaxis_title='Périodes', yaxis_title='Montant en Mio AR',      legend=dict(
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
# fig_p.show()

# Création figure2
fig_2 = go.Figure(go.Scatter(x=periode,
                             y=redevances,
                             mode='lines+markers',
                             name='Montant des redevances',
                             line=dict(width=3, color='#33CC00'),
                             fill='tonexty'
                             ))
fig_2.add_trace(go.Scatter(x=periode, mode='lines+markers',
                           y=c_revient,
                           name='Coût de revient',
                           line=dict(width=3, color='#FF0000'),
                           stackgroup='one')
                )
fig_2.update_layout(barmode='group', xaxis_title='Périodes', yaxis_title='Montant en Mio AR')
# fig_2.show()

# Création figure3
fig3_p = px.bar(ds_tba_ev_R,
                x=per_eR,
                y=red_eB,
                title='Evolution annuelle des Redevances : Budget (en vert) par rapport aux Réalisations (couleur '
                      'signal)',
                color_discrete_sequence=['#00FE35'] * len(ds_tba_ev_R),
                )
fig3_p.add_trace(go.Bar(name='Echelle des écarts : Réalisations/Budgets',
                        x=per_eR,
                        y=red_eR,
                        marker=dict(
                            color=abs((red_eR - red_eB) / red_eB),
                            colorscale="RdYlGn_r",
                            showscale=True
                        )
                        ))
fig3_p.update_layout(barmode='group', xaxis_title='Périodes', yaxis_title='Montant en Mio AR',      legend=dict(
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
# fig_p.show()

# Création figure4
fig4_p = px.bar(ds_tba_ev_CR,
                x=per_eC,
                y=red_eCb,
                title='Evolution annuelle des Coût de revient : Budget (en vert) par rapport aux Réalisations (couleur '
                      'signal)',
                color_discrete_sequence=['#00FE35'] * len(ds_tba_ev_CR),
                )
fig4_p.add_trace(go.Bar(name='Echelle des écarts : Réalisations/Budgets',
                        x=per_eC,
                        y=red_eCr,
                        marker=dict(
                            color=abs((red_eCr - red_eCb) / red_eCb),
                            colorscale="RdYlGn_r",
                            showscale=True
                        )
                        ))
fig4_p.update_layout(barmode='group', xaxis_title='Périodes', yaxis_title='Montant en Mio AR',      legend=dict(
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
# fig_p.show()

#logo_path = '../assets/logo.png'


layout = html.Div(children=[
    #html.Img(src=logo_path, style={'display': 'inline'}),
    html.P(children="Elements graphiques de l'analyse comparative des Redevances et des Coûts de revient", style={'color': 'red',
                                                                                      'margin': '0',
                                                                                       'padding': '0',
                                                                                       'font-weight': 'bold',
                                                                                       'font-size': '15px',
                                                                                       'text-align': 'left',
                                                                                       'display': 'block', 'paddingTop': '20px'}),
    html.P(children="Données : Exercice en cours", style={'color': 'black',
                                                          'margin': '0',
                                                          'padding': '0',
                                                          'font-weight': 'bold',
                                                          'font-size': '12px',
                                                          'text-align': 'left',
                                                          'display': 'inline'}),
    html.P(children="Données cumulées : Depuis 2017", style={'color': 'black',
                                                             'margin': '0',
                                                             'padding': '0',
                                                             'font-weight': 'bold',
                                                             'font-size': '12px',
                                                             'text-align': 'left',
                                                             'display': 'block'}),
    html.P(children=f'Edition du : {date_edition}', style={'color': 'black',
                                            'margin': '0',
                                            'padding': '0',
                                            'font-weight': 'bold',
                                            'font-size': '12px',
                                            'text-align': 'left',
                                            'display': 'inline'}),
    html.Div(style={'display': 'block'},
             children=[
                 dcc.Graph(
                     id='redevances',
                     figure=fig_p
                 )
             ]),
    html.Div(style={'display': 'block'},
             children=[
                 dcc.Graph(
                     id='revient',
                     figure=fig_2
                 )
             ]),
    html.Div(style={'display': 'block'},
             children=[
                 dcc.Graph(
                     id='red_bgt_real',
                     figure=fig3_p
                 )
             ]),
    html.Div(style={'display': 'block'},
             children=[
                 dcc.Graph(
                     id='cout_bgt_real',
                     figure=fig4_p
                 )
             ])

])


