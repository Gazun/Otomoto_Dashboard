import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


df = pd.read_csv('oto_moto_czyste.csv')

# Filtrowany df
filtered_df = df

# Lista marek
marki_vc = df['Marka pojazdu'].value_counts()

app = dash.Dash(__name__)

app.layout = html.Div(
    id='container',
    children=[

        html.Div(
            id='mini_container',
            style={'width':'300px'},
            children=[

                html.Div(
                    id='tytul',
                    children=['Wybór auta:'],
                ),

                html.Br(),

                dcc.Dropdown(
                    id='marka',
                    className='dropdown-class',
                    options=[{'label':i,'value':i} for i in marki_vc.index],
                    value='BMW'
                ),

                dcc.Dropdown(
                    id='model',
                    className='dropdown-class',
                    value='Seria 3'
                ),

                html.Br()
            ]),

            html.Div(
                id='graph_container',
                children=[

                dcc.Graph(
                    id='wykres',
                    config={'displayModeBar':False}
                )

            ])
    ])



@app.callback(
    Output('model', 'options'),
    [Input('marka','value')]
)
def filtruj_marke(marka):
    global filtered_df
    filtered_df = df[df['Marka pojazdu'] == marka]
    modele_vc = filtered_df['Model pojazdu'].value_counts()

    return [{'label':i,'value':i} for i in modele_vc.index]

@app.callback(

    [Input('marka','value'), Input('model','value')]
)
def filtruj_marke_model(marka, model):

    global filtered_df

    war_1 = df['Marka pojazdu'] == marka
    war_2 = df['Model pojazdu'] == model

    filtered_df = df[war_1 & war_2].copy()


@app.callback(
    Output('wykres','figure'),
    [Input('marka','value'), Input('model','value')]
)
def filtruj_wykres(marka, model):

    global filtered_df

    war_1 = df['Marka pojazdu'] == marka
    war_2 = df['Model pojazdu'] == model

    filtered_df = df[war_1 & war_2].copy()

    return px.box(filtered_df, x='Rok produkcji', y='Cena')


if __name__ == '__main__':
    app.run_server(debug=True)
