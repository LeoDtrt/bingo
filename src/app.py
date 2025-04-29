import dash
from dash import html, dcc, Input, Output, State
import random

app = dash.Dash(__name__)
server = app.server

# Liste fixe d’activités
activites = [
    """faire une imitation de Max""",
    """improviser un petit discours faisant l'éloge de Max""",
    """boire un shot""",
    """porter la perruque de la honte pendant 20 minutes""",
    """faire 10 pompes""",
    """faire 10 burpees""",
    """faire 10 squats""",
    """faire 1 minutes de planche""",
    """aller être dans le bain nordique dans moins de 5 minutes""",
    """faire le poirier sur le tapis magique""",
    """faire 5 roulades sur le tapis magique""",
    """s'adresser aux vainqueurs en les nommant "Master of the puppets" pendant une heure""",
    """s'adresser aux vainqueurs en les nommant "Oh capitaine mon capitaine" pendant une heure""",
    """s'adresser aux vainqueurs en les nommant "Numéro Uno" pendant une heure""",
    """manger une dragée surprise de Bertie Crochue""",
    """demander l’avis de l’audience pour son action"""
]





app.layout = html.Div([
    html.Div([
        html.H1("Bingo : Tirage au sort"),

        html.H2("Ajouter un nom :"),
        dcc.Input(id='input-nom', type='text', placeholder='Entrez un nom', className='input-nom'),
        html.Button('Ajouter', id='btn-ajouter', n_clicks=0, className='dash-button'),
        html.Button('Réinitialiser', id='btn-reset', n_clicks=0, className='dash-button'),

        html.H3("Liste des noms :"),
        html.Ul(id='liste-noms'),

        html.H3("Noms activés pour le tirage :"),
        dcc.Checklist(id='checklist-noms', options=[], value=[], className='checklist-style'),

        html.Button("Tirer un nom et une activité", id='btn-tirer', n_clicks=0, className='dash-button'),
        html.Br(),
        html.Br(),
        html.Div(id='resultat-tirage'),

        dcc.Store(id='noms-stockes', data=[])        
    ], className='container')

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
    return f"{nom} doit {activite}"

if __name__ == '__main__':
    app.run_server(debug=True)
