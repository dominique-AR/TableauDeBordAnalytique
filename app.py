# Import modules
import dash
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import dash_auth
import user
from waitress import serve


"""
This is the main app that drives everything
"""

# Keep this out of source code repository - save in a file or a database
#VALID_USERNAME_PASSWORD_PAIRS = {"daf": "daf"}
VALID_USERNAME_PASSWORD_PAIRS = user.VALID_USERNAME_PASSWORD_PAIRS
#This create a Dash app instance
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],use_pages=True)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS)




#This is the logo path
logo_path = '/assets/Logo_apave.jpg'
logo = html.Img(src=logo_path, style={'height':'100%', 'width':'100%'})
#, style={'display': 'inline'})

#This is the  header:
header = html.H1("Tableau de bord Analytique  de l'AGETIPA", style={'text-align':'center', 'color':'green', 'font-size':'20px'})


#This define the navbar used
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page d'accueil", href="/", active="exact", style={'border-style': 'black 2px dotted', 'text-transform': 'uppercase'})),
        dbc.NavItem(dbc.NavLink("Analyse des marges", href="/marges", active="exact", style={'border-style': 'black 2px dotted', 'text-transform': 'uppercase'})),
        dbc.NavItem(dbc.NavLink("Redevances", href="/redevances_et_cout", active="exact", style={'border-style': 'black 2px dotted', 'text-transform': 'uppercase'})),
        dbc.NavItem(dbc.NavLink("Coût-processus", href="/cout_processus", active="exact", style={'border-style': 'black 2px dotted', 'text-transform': 'uppercase'})),        
    ],
    id="menu_accueil",
    #brand="TABLEAU DE BORD ANALYTIQUE DE GESTION",
    brand_href="#",
    color="#3d8a18",
    dark=True,
)

body = html.Div(children=[
        dbc.Row([
            dbc.Col(logo, width="2"),
            dbc.Col(header, width="10", style={"flex": "1"})

        ], align="center"

        ),
        dbc.Row(navbar, style={"flex": "1"})
])

app.layout = dbc.Container([body, dash.page_container], fluid=True)

#server = app.server


if __name__ == "__main__":
    serve(app, host='192.168.88.65', port=8050, url_scheme='http')
   # app.run_server(host='192.168.8.131', port=8050, debug=True)
    #app.run_server(debug=True)


"""

# Keep this out of source code repository - save in a file or a database
#VALID_USERNAME_PASSWORD_PAIRS = {"daf": "daf"}

# Change from Column to Row in Layout: children=[dbc.Col(logo, width="auto"), dbc.Col(navbar, style={"flex": "1"})], align="center")
#Layout Brouillon: dbc.Row(dash.page_container, style={"margin-top": "20px"})
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(page["name"], href=page["path"])
                for page in dash.page_registry.values()
                if page["module"] != "pages.not_found_404"
            ],
            nav=True,
            in_navbar=True,
            label="Menu déroulant",
        ),
"""