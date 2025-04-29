import dash
from dash import html, dcc, Input, Output, State
import random

app = dash.Dash(__name__)
server = app.server

# Liste fixe d’activités
activites = ["Jeu de société", "Karaoké", "Dessiner", "Quiz", "Danse", "Mime"]

app.layout = html.Div([
    html.H1("Tirage au sort : nom & activité"),

    html.H2("Ajouter un nom :"),
    dcc.Input(id='input-nom', type='text', placeholder='Entrez un nom'),
    html.Button('Ajouter', id='btn-ajouter', n_clicks=0),
    html.Button('Réinitialiser', id='btn-reset', n_clicks=0, style={'marginLeft': '10px'}),

    html.H3("Liste des noms :"),
    html.Ul(id='liste-noms'),

    html.H4("Noms activés pour le tirage :"),
    dcc.Checklist(id='checklist-noms', options=[], value=[], labelStyle={'display': 'block'}),

    html.Button("Tirer un nom et une activité", id='btn-tirer', n_clicks=0),
    html.Div(id='resultat-tirage', style={'marginTop': '20px', 'fontSize': '20px'}),

    dcc.Store(id='noms-stockes', data=[])
])

# Ajouter un nom ou réinitialiser la liste
@app.callback(
    Output('noms-stockes', 'data'),
    Output('input-nom', 'value'),
    Input('btn-ajouter', 'n_clicks'),
    Input('btn-reset', 'n_clicks'),
    State('input-nom', 'value'),
    State('noms-stockes', 'data'),
    prevent_initial_call=True
)
def maj_liste(btn_ajouter, btn_reset, nom, noms):
    triggered = dash.callback_context.triggered_id
    if triggered == 'btn-reset':
        return [], ""
    if triggered == 'btn-ajouter' and nom and nom.strip():
        noms.append(nom.strip())
    return noms, ""

# Afficher la liste des noms (simple)
@app.callback(
    Output('liste-noms', 'children'),
    Input('noms-stockes', 'data')
)
def afficher_noms(noms):
    return [html.Li(n) for n in noms]

# Mettre à jour la checklist des noms activés
@app.callback(
    Output('checklist-noms', 'options'),
    Output('checklist-noms', 'value'),
    Input('noms-stockes', 'data'),
)
def maj_checklist(noms):
    return [{'label': n, 'value': n} for n in noms], noms  # tous activés par défaut

# Tirer au sort uniquement parmi les noms cochés
@app.callback(
    Output('resultat-tirage', 'children'),
    Input('btn-tirer', 'n_clicks'),
    State('checklist-noms', 'value'),
    prevent_initial_call=True
)
def tirer_nom(n_clicks, noms_actifs):
    if not noms_actifs:
        return "Aucun nom actif pour le tirage !"
    nom = random.choice(noms_actifs)
    activite = random.choice(activites)
    return f"{nom} va faire : {activite}"

if __name__ == '__main__':
    app.run_server(debug=True)
