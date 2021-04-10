import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import os

csv_files_path = os.path.join('data/oto_moto_czyste.csv')
df = pd.read_csv(csv_files_path)

rok_min = df['Rok produkcji'].min()
rok_max = df['Rok produkcji'].max()

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

default_fig = go.Figure()

default_fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color':'rgb(127,175,223)'
})

app.layout = html.Div(
    children=[

    html.Div(
        id='container_header',
        children=[

            html.Div('Samochody osobowe z Otomoto')

        ]
    ),

    html.Div(
        className='container',
        children=[

            html.Div(
                className='container_medium',
                children=[

                    dcc.Graph(
                    id='wykres-2',
                    config={'displayModeBar':False},
                    figure=default_fig
                    )

                ]
            ),

            html.Div(
                className='filtry',
                children=[

                    html.Div('Marka'),

                    dcc.Dropdown(
                        id='drop_marka',
                        options=[{'label':i,'value':i} \
                            for i in df['Marka pojazdu'].unique()],
                        value=None,
                        style = {
                            'background-color':'#52708E',
                            'color': 'rgb(37,46,63)',
                            'font-weight':'bold'
                            }
                    ),

                    html.Br(),
                    html.Div('Model'),

                    dcc.Dropdown(
                        id='drop_model',
                        options=[{'label':i,'value':i} \
                            for i in df['Model pojazdu'].unique()],
                        value=None,
                        style = {
                            'background-color':'#52708E',
                            'color': 'rgb(37,46,63)',
                            'font-weight':'bold'
                            }
                    ),

                    html.Br(),
                    html.Div('Rok'),

                    dcc.RangeSlider(
                        id='slider-1',
                        count=1,
                        min=rok_min,
                        max=rok_max,
                        step=1,
                        value=[rok_min+5, rok_max]
                    ),

                    html.Div(id='div-rok'),

                    html.Div(id='test')

                ]
            ),

            html.Div(
                className='container_mini',
                children=[

                    dcc.Graph(
                        id='wykres-1',
                        config={'displayModeBar':False},
                        figure=default_fig
                    )

                ]
            ),

            html.Div(style={'clear':'both'})

    ])

    ]
)

# Wyswietlenie roku filtra
@app.callback(
    Output('div-rok', 'children'),
    [Input('slider-1','value')]
)
def wyswietl_rok(value):
    min_v = value[0]
    max_v = value[1]
    return f'{min_v} do {max_v}'

# Zmiana modelu do wybrania
@app.callback(
    Output('drop_model', 'options'),
    [Input('drop_marka','value')]
)
def zmien_marke(value):
    global df
    df_temp = df[df['Marka pojazdu'] == value]

    return [{'label':i,'value':i} \
        for i in df_temp['Model pojazdu'].unique()]


@app.callback(
    Output('wykres-1', 'figure'),
    [Input('drop_marka','value'),
    Input('drop_model','value'),
    Input('slider-1','value')]
)
def update_wykres_1(marka, model, lata):

    dff = df.copy()

    if marka is not None:
        dff = dff[dff['Marka pojazdu'] == marka]

    if model is not None:
        dff = dff[dff['Model pojazdu'] == model]

    rok_od = lata[0]
    rok_do = lata[1]

    dff = dff[dff['Rok produkcji'] > rok_od]
    dff = dff[dff['Rok produkcji'] < rok_do]

    fig_1 = px.box(
        dff,
        x='Rok produkcji',
        y='Cena',
        color='Rodzaj paliwa')

    fig_1.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font_color':'rgb(127,175,223)'
    })

    return fig_1

@app.callback(
    Output('wykres-2', 'figure'),
    [Input('slider-1','value')]

)
def update_wykres_2(lata):

    dff = df.copy()

    rok_od = lata[0]
    rok_do = lata[1]

    dff = dff[dff['Rok produkcji'] > rok_od]
    dff = dff[dff['Rok produkcji'] < rok_do]

    df_group = dff.groupby(['Marka pojazdu']) \
    .agg({'Cena':'count'}) \
    .rename(columns={'Cena':'Liczba'}) \
    .reset_index() \
    .sort_values(by='Liczba', ascending=False)

    df_group = df_group

    fig = px.bar(
        df_group,
        x='Marka pojazdu',
        y='Liczba',
        height=300)

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font_color':'rgb(127,175,223)'
    })

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
