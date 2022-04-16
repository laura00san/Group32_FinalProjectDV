import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

data_moods = pd.read_csv(r'C:\Users\User\Downloads\data_moods.csv')

#DATASETS FOR ARTISTS COMPARISON
df_mood = data_moods[data_moods['artist'] !='Various Artists']
df_mood = df_mood.drop_duplicates('artist', keep='last')

df_sad = data_moods[data_moods['mood'] == 'Sad']
df_calm = data_moods[data_moods['mood'] == 'Calm']
df_happy = data_moods[data_moods['mood'] == 'Happy']
df_energetic = data_moods[data_moods['mood'] == 'Energetic']

music_characteristics = ['danceability', 'acousticness', 'energy', 'instrumentalness','liveness', 'valence', 'speechiness']

# DATASETS FOR TOP 10 BARPLOT BY MOOD
top10_sad = data_moods[data_moods['mood'] == 'Sad'].sort_values("popularity")[-10:]
top10_calm = data_moods[data_moods['mood'] == 'Calm'].sort_values("popularity")[-10:]
top10_happy = data_moods[data_moods['mood'] == 'Happy'].sort_values("popularity")[-10:]
top10_energetic = data_moods[data_moods['mood'] == 'Energetic'].sort_values("popularity")[-10:]


# DATASETS FOR TOP LINEPLOT OF MUSIC CHARACTERISTICS
data_moods['year'] = pd.DatetimeIndex(data_moods['release_date']).year
data_moods = data_moods.sort_values("year")


# DATASETS FOR TOP ARTISTS AND MUSIC
top_data = data_moods[data_moods["year"] >= 2010]

# DATASETS FOR NUMBER OF SONGS PER MOOD
numero = ["140", "197", "154", "195"]
caracteristicas = ['Happy', 'Sad', 'Energetic', 'Calm']
moods = ["Mood","Mood","Mood","Mood"]
df = pd.DataFrame(
    dict(numero=numero, caracteristicas=caracteristicas, moods=moods)
)

#FIGURE NUMBER OF SONGS PER MOOD
fig_moods = px.sunburst(df, path=['moods', 'caracteristicas', 'numero'],
                        )



#MUSIC CHARACTERISTICS
def create_music_characteristics_plot():
    fig_char_years = go.Figure()
    years = data_moods['year'].unique()
    columns = ["acousticness", "danceability", "energy", "speechiness", "liveness", "valence", "instrumentalness"]
    for col in columns:
        line_info = data_moods.groupby("year")[col].mean()
        fig_char_years.add_trace(go.Scatter(x=years, y=line_info, mode='lines', name=col))

    fig_char_years.update_layout(
        width=800,
        height=500,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return fig_char_years


###################################################   Interactive Components   #########################################
# ARTISTS COMPARISON - choice of the players
artists_options_sad = []
for i in df_sad.index:
    artists_options_sad.append({'label': df_sad['artist'][i], 'value':  df_sad['artist'][i]})

artists_options_calm = []
for i in df_calm.index:
    artists_options_calm.append({'label': df_calm['artist'][i], 'value':  df_calm['artist'][i]})

artists_options_happy = []
for i in df_happy.index:
    artists_options_happy.append({'label': df_happy['artist'][i], 'value':  df_happy['artist'][i]})

artists_options_energetic = []
for i in df_energetic.index:
    artists_options_energetic.append({'label': df_energetic['artist'][i], 'value':  df_energetic['artist'][i]})


# ARTISTS COMPARISON - dropdowns of artists per mood
dropdown_mood_sad = dcc.Dropdown(
        id='artist1',
        options=artists_options_sad,
        value='Kodaline',
        style ={'width' :250, "font-size": 13, 'top': -8, 'left': 30}
    )

dropdown_mood_calm = dcc.Dropdown(
        id='artist2',
        options=artists_options_calm,
        value='Martin Gauffin',
        style ={'width' :250,"font-size": 13, 'top': -8, 'left': 30}
    )

dropdown_mood_happy = dcc.Dropdown(
        id='artist3',
        options=artists_options_happy,
        value='Elton John',
        style ={'width' :250, "font-size": 13, 'top': -8, 'left': 30}
    )

dropdown_mood_energetic = dcc.Dropdown(
        id='artist4',
        options=artists_options_energetic,
        value='Thirty Seconds To Mars',
        style ={'width' :250, "font-size": 13, 'top': -8, 'left': 30}
    )

# TOP 10 BARPLOT BY MOOD - options of moods
radio_moods = dbc.RadioItems(
        id='mood',
        className='radio',
        options=[dict(label='Sad', value=0, style={'padding': 70}), dict(label='Happy', value=1),
                 dict(label='Calm', value=2), dict(label='Energetic', value=3)],
        value=0,
        style={"font-size": 13, 'top': 30, 'left': 600},
        inline=True,

    )
##SLIDER FOR TOP ARTISTS AND MUSIC
slider_top = dcc.Slider(
        id='slider_years',
        marks={str(i): str(i) for i in [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]},
        min=2010,
        value = top_data['year'].min(),
        step = 1
    )





# TOP 10 BARPLOT BY MOOD
album = data_moods['album'].to_list()

options_sad = [dict(label=name, value=name) for name in top10_sad['album'].to_list()[::-1] if name in album]
options_calm = [dict(label=name, value=name) for name in top10_calm['album'].to_list()[::-1] if name in album]
options_happy = [dict(label=name, value=name) for name in top10_happy['album'].to_list()[::-1] if name in album]
options_energetic = [dict(label=name, value=name) for name in top10_energetic['album'].to_list()[::-1] if name in album]

bar_colors = ['#8bacd6', '#eb8181', '#a79ce1', '#1DB954',]
bar_options = [top10_sad, top10_calm, top10_happy, top10_energetic]

###############################3 Dash App Layout ##################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

server = app.server



navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src="https://cdn2.downdetector.com/static/uploads/logo/Spotify_Logo_RGB_Green.png", height="80px"),width=3),
                    dbc.Col(
                        [html.Label("WHAT CAN MUSIC TELL ABOUT YOUR MOOD? ",id = "label1", style={"font-weight": "bold", 'color':'#1DB954', "font-size": 30}),
                        html.Br(),
                         html.Label("Explore Spotify music and relationship with listener's mood",className = "label2", style={"font-weight": "bold", "font-size": 25}),
                         html.Br()],width=6),
                    dbc.Col(
                        [html.Img(src="https://scannables.scdn.co/uri/plain/jpeg/24E07D/white/640/spotify:playlist:0RH319xCjeU8VyTSqCF6M4", style={'height': "70px"}),
                                     html.Label("Scan me for good music! ",id = "label_scanner", style={"font-size": 15})],width=3),

                ],
                align="between",
                #no_gutters=True,
            ), style={'width': '100%'}
        ),
    ],
)


#ARTISTS COMPARISON - "card" a dropdown list
controls_mood_sad = dbc.Card(
    [
        dbc.CardGroup(
            [   html.Label('Feeling sad? Choose an artist:   ', style={"font-size": 15}),
                dropdown_mood_sad,
            ]
        ),
    ],
    body=True,
    className="controls_artists",
    )

controls_mood_calm = dbc.Card(
    [
        dbc.CardGroup(
            [
                html.Label('Feeling calm? Choose an artist:   ', style={"font-size": 15}),
                html.Br(),
                dropdown_mood_calm,
            ]
        ),
    ],
    body=True,
    className="controls_artists",
)

controls_mood_happy = dbc.Card(
    [
        dbc.CardGroup(
            [
                html.Label('Feeling happy? Choose an artist:   ', style={"font-size": 15}),
                html.Br(),
                dropdown_mood_happy
            ]
        ),
    ],
    body=True,
    className="controls_artists",
)

controls_mood_energetic = dbc.Card(
    [
        dbc.CardGroup(
            [
                html.Label('Feeling energetic? Choose an artist:   ', style={"font-size": 15}),
                html.Br(),
                dropdown_mood_energetic

            ]
        ),
    ],
    body=True,
    className="controls_artists"
)

# TOP 10 BARPLOT BY MOOD - "card" to choose mood
choose_mood = dbc.Card(
    [
        dbc.CardGroup(
            [
                html.Label('Choose the Mood:   ', style={"font-size": 15}),
                html.Br(),
                radio_moods,
            ]
        ),
    ],
    body=True,
    className="controls_moods",
)


# TOP ARTISTS AND MUSIC - "card" for top 1
podium_1 = dbc.Card(
    [
        dbc.CardGroup(
            [
                dbc.Row([
                    html.P('Number 1',style={"font-size": 20, "font-weight": "bold",  "text-align": "center"}),
                    html.Hr()
                ]),
                dbc.Row([
                html.P(id='song_name_1', className='song_podium'),
                html.P(id='artist_name_1', className='artist_podium'),
                ])
            ], style={'background': '#8bacd6'}
        ),
    ],
    body=True,
    className="podium_1",
)

# TOP ARTISTS AND MUSIC - "card" for top 2
podium_2 = dbc.Card(
    [
        dbc.CardGroup(
            [
                dbc.Row([
                html.P('Number 2', style={"font-size": 20, "font-weight": "bold",  "text-align": "center"}),
                html.Hr()
                ]),
                dbc.Row([
                html.P(id='song_name_2', className='song_podium'),
                html.P(id='artist_name_2', className='artist_podium'),
                ]),

            ] , style={'background': '#8bacd6'}
        ),
    ],
    body=True,
    className="podium_2",
)



# TOP ARTISTS AND MUSIC - "card" for top 2
podium_3 = dbc.Card(
    [
        dbc.CardGroup(
            [
                dbc.Row([
                    html.P('Number 3', style={"font-size": 20, "font-weight": "bold",  "text-align": "center"}),
                    html.Hr()
                ]),
                dbc.Row([
                html.P(id='song_name_3', className='song_podium'),
                html.P(id='artist_name_3', className='artist_podium'),
                ])
            ] , style={'background': '#8bacd6'}
        ),
    ],
    body=True,
    className="podium_3",
)


# ERAS
music_80 = dbc.Card(
    [
        dbc.CardGroup(
            [
                dbc.Row([
                    html.P('80s Music', style={"font-size": 20, "font-weight": "bold",  "text-align": "center"}),
                    dbc.Col(html.Img(src='https://cdn-icons-png.flaticon.com/512/1378/1378161.png', height="80px", style={'text-align':'center', 'position':'relative', 'left':65, 'padding':10})),
                    html.P('Happy Era', style={"font-size": 15, "font-weight": "bold",  "text-align": "center"}),
                    html.P('All the artists from the 80s brought something unique to 80s music. Full of energy, the music stands out because of its danceability and positive energy. ', style={"font-size": 13, "text-align": "center"}),
                ]),
            ] , style={'background': '#8bacd6'}
        ),
    ],
    body=True,
    className="music_80",
)

music_90 = dbc.Card(
    [
        dbc.CardGroup(
            [
                dbc.Row([
                    html.P('90s Music', style={"font-size": 20, "font-weight": "bold",  "text-align": "center"}),
                    dbc.Col(html.Img(src='https://static.vecteezy.com/system/resources/previews/001/207/865/large_2x/rapper-png.png', height="80px", style={'text-align':'center', 'position':'relative', 'left':65, 'padding':10})),
                    html.P('Urban Music', style={"font-size": 15, "font-weight": "bold",  "text-align": "center"}),
                    html.P('The beauty of 90s music was its diversity. From hip-hop, rap, reggae, contemporary R&B to urban music, this period comes first when it comes to songs speechiness.',
                        style={"font-size": 13, "text-align": "center"}),
                ]),
            ] , style={'background': '#8bacd6'}
        ),
    ],
    body=True,
    className="music_90",
)

music_10_20 = dbc.Card(
    [
        dbc.CardGroup(
            [
                dbc.Row([
                    html.P('2010 to 2020 Music', style={"font-size": 20, "font-weight": "bold",  "text-align": "center"}),
                    dbc.Col(html.Img(src='https://static.thenounproject.com/png/3658423-200.png', height="80px", style={'text-align':'center', 'position':'relative', 'left':65, 'padding':10})),
                    html.Br(),
                    html.Br(),
                    html.P('Low Energy Music', style={"font-size": 15, "font-weight": "bold",  "text-align": "center"}),
                    html.P('Music industry took a turn after 2000. Music became more instrumental with a trend for low-energy and acoustic music.',
                        style={"font-size": 12, "text-align": "center"}),

                ]),
            ] , style={'background': '#8bacd6'}
        ),
    ],
    body=True,
    className="music_10_20",
)



conteudo = html.Div([
    html.A([
        dbc.Col([
            dbc.Row([
                #BAR PLOT CONTENT
                dbc.Card(
                    dbc.CardBody([

                        html.H2('Top 10 albums', style={"font-weight": "bold", "font-size": 20}),
                        html.Hr(),

                        dbc.Row([
                        dbc.Col([
                           dbc.Row(choose_mood)], sm=20),
                            dbc.Col(html.Div([
                                html.Label(id='title_bar'),
                                dcc.Graph(id='bar_fig')],
                                className='box', style={'padding-bottom': '15px'}), ),
                        ], justify="between")
                    ])

                )
            ]),
            dbc.Row([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                                html.Label('Year Slider'),
                                slider_top]),
                        dbc.Row([
                            html.H2('Podium of songs', style={"font-weight": "bold", "font-size": 20}),
                            html.Hr()
                        ]),
                        dbc.Row([
                            dbc.Col(podium_1, style={'wdth': 2}),
                            dbc.Col(podium_2,style={'wdth': 2}),
                            dbc.Col(podium_3, style={'wdth': 2})
                        ])
                    ])
                )
            ]),
            dbc.Row([
                dbc.Card(
                    dbc.CardBody([
                        html.H2('Music characteristics', style={"font-weight": "bold", "font-size": 20}),
                        html.Hr(),
                        html.Label(
                            'It is possible to notice that the characteristics of the songs change every year. Instrumentalness appears to be high in the 90s, 2010 and through the roof in 2020. Songs with substantial values of valence are present in the 70s, 80s, 90s and decrease from the beggining of 00s until 2020. The presence of an audience in the  recording was a trend in the 70s. It the 90s, rap and hip hop started to become a major trend, hence the high values for speechness that later became less evident. The 80s are known for their positive and happy vibes, which can be seen through high values of energy and danceability, whereas in 2020 energy is the lowest ever and majority of tracks are acoustic.'
                            , style={"font-size": 13}),
                        dbc.Col(dcc.Graph(id='graph', figure=create_music_characteristics_plot()), sm=20, align = 'around'),
                        dbc.Row([
                            dbc.Col(music_80, style={'wdth': 2}),
                            dbc.Col(music_90,style={'wdth': 2}),
                            dbc.Col(music_10_20, style={'wdth': 2})
                        ])

                    ])
                )
            ])
        ],style={'width':'56%', 'float': 'left'}),
        dbc.Col([
            dbc.Row([
                dbc.Card(
                    dbc.CardBody([
                        html.H2('Artist Comparison', style={"font-weight": "bold", "font-size": 20}),
                        html.Hr(),
                        html.Label(
                        'Music characteristics can influence a lot how they make you feel. Choose one artist from each category of mood and explore the characteristics of the overall songs of that artist',
                            style={"font-size": 14}),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col([dbc.Row(controls_mood_sad)], sm=20),
                            dbc.Col([dbc.Row(controls_mood_calm)], sm=20),
                            dbc.Col([dbc.Row(controls_mood_happy)], sm=20),
                            dbc.Col([dbc.Row(controls_mood_energetic)], sm=30),
                            dbc.Col(dcc.Graph(id='graph_example'), sm=20)
                        ]),
                        dbc.Row([
                            html.Label('Energy', style={"font-weight": "bold", "font-size": 12}),
                            html.Label('Measure of intensity and activity. Typically, energetic tracks feel fast, loud and noisy', style={"font-size": 12}),
                            html.Hr(),
                            html.Label('Danceability', style={"font-weight": "bold", "font-size": 12}),
                            html.Label('How suitable a track is for dancing based on a combination of musical elements' , style={"font-size": 12}),
                            html.Hr(),
                            html.Label('Acousticness', style={"font-weight": "bold", "font-size": 12}),
                            html.Label('Confidence measure of whether the track is acoustic ', style={"font-size": 12}),
                            html.Hr(),
                            html.Label('Instrumentalness', style={"font-weight": "bold", "font-size": 12}),
                            html.Label('Instrumentalness: represents the amount of vocals in the song ', style={"font-size": 12}),
                            html.Hr(),
                            html.Label('Liveness', style={"font-weight": "bold", "font-size": 12}),
                            html.Label('Detects the presence of an audience in the recording', style={"font-size": 12}),
                            html.Hr(),
                            html.Label('Valence', style={"font-weight": "bold", "font-size": 12}),
                            html.Label('Describes the musical positiveness conveyed by a track ', style={"font-size": 12}),
                            html.Hr(),
                            html.Label('Speechiness', style={"font-weight": "bold", "font-size": 12}),
                            html.Label('Detects the presence of spoken words in a track ', style={"font-size": 12}),
                            html.Hr(),

                        ])
                    ])
                )
            ]),
        dbc.Row([
            html.H2("Number of songs per mood", style={"font-weight": "bold", "font-size": 20}),
            html.Hr(),
            html.Div([dcc.Graph(figure=fig_moods)])

        ])
        ] , style={'width':'40%', 'float': 'right'})
    ])
])

footer = html.Div([
        dbc.Row([
            html.H2('Authors', style={"font-weight": "bold", 'font-size': 14, "text-align": "center", "color": 'white'}),
            html.Label("Dashboard created by: Ana Leonor Vital, Joana Tavares, Laura Santos, Maria Oliveira",className = "label3",style={'font-size': 12, "text-align": "center", "color": 'white'})
        ]),
        dbc.Row([
            html.H2('Sources', style={"font-weight": "bold", 'font-size': 14, "text-align": "center", "color": 'white'}),
            html.Label("Spotify data: https://www.kaggle.com/datasets/musicblogger/spotify-music-data-to-identify-the-moods",className = "label3",style={'font-size': 12, "text-align": "center", "color": 'white'})
        ])
        ] , style={'position':'absolute', 'bottom':-1400, 'width':'100%', 'height':'95px','background':'#1DB954'})

app.layout = dbc.Container([
        navbar,
        conteudo,
        footer
    ],
    fluid=True,
)

################### APP CALLBACK ################33

# TOP 10 BARPLOT BY MOOD
@app.callback(
    [
        Output('title_bar', 'children'),
        Output('bar_fig', 'figure'),

    ],
    [
        Input('mood', 'value')
    ],
)

def bar_chart(top10_select):
    ################## Top10 Plot ##################
    title = ''
    df = bar_options[top10_select]
    ################## Dropdown Bar ##################
    bar_fig = dict(type='bar',
                   x=df.popularity,
                   y=df.album,
                   orientation='h',
                   marker_color=bar_colors[top10_select])

    return title, \
           go.Figure(data=bar_fig, layout=dict(height=300, font_color='#363535', paper_bgcolor='rgba(0,0,0,0)',
                                               plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                                               margin_pad=10))


# ARTISTS COMPARISON
@app.callback(
    [
        Output('graph_example', 'figure'),
    ],
    [
        Input('artist1', 'value'),
        Input('artist2', 'value'),
        Input('artist3', 'value'),
        Input('artist4', 'value')
    ]
)



def tab_1_function(artist1, artist2, artist3, artist4):

    # scatterpolar
    df1_for_plot = pd.DataFrame(df_sad[df_sad['artist'] == artist1][music_characteristics].iloc[0])
    df1_for_plot.columns = ['score']
    df2_for_plot = pd.DataFrame(df_calm[df_calm['artist'] == artist2][music_characteristics].iloc[0])
    df2_for_plot.columns = ['score']
    df3_for_plot = pd.DataFrame(df_happy[df_happy['artist'] == artist3][music_characteristics].iloc[0])
    df3_for_plot.columns = ['score']
    df4_for_plot = pd.DataFrame(df_energetic[df_energetic['artist'] == artist4][music_characteristics].iloc[0])
    df4_for_plot.columns = ['score']

    list_scores = [df1_for_plot.index[i].capitalize() +' = ' + str(df1_for_plot['score'][i]) for i in range(len(df1_for_plot))]
    text_scores_1 = artist1
    for i in list_scores:
        text_scores_1 += '<br>' + i

    list_scores = [df2_for_plot.index[i].capitalize() +' = ' + str(df2_for_plot['score'][i]) for i in range(len(df2_for_plot))]
    text_scores_2 = artist2
    for i in list_scores:
        text_scores_2 += '<br>' + i

    list_scores = [df3_for_plot.index[i].capitalize() + ' = ' + str(df3_for_plot['score'][i]) for i in
                   range(len(df3_for_plot))]
    text_scores_3 = artist3
    for i in list_scores:
        text_scores_3 += '<br>' + i

    list_scores = [df4_for_plot.index[i].capitalize() + ' = ' + str(df4_for_plot['score'][i]) for i in
                   range(len(df4_for_plot))]
    text_scores_4 = artist4
    for i in list_scores:
        text_scores_4 += '<br>' + i


    fig = go.Figure(data=go.Scatterpolar(
        r=df1_for_plot['score'],
        theta=df1_for_plot.index,
        fill='toself',
        marker_color = 'rgb(45,0,198)',
        opacity =1,
        hoverinfo = "text" ,
        name = text_scores_1,
        text = [df1_for_plot.index[i] +' = ' + str(df1_for_plot['score'][i]) for i in range(len(df1_for_plot))]
    ))
    fig.add_trace(go.Scatterpolar(
        r=df2_for_plot['score'],
        theta=df2_for_plot.index,
        fill='toself',
        marker_color = '#1DB954',
        hoverinfo = "text" ,
        name= text_scores_2,
        text  = [df2_for_plot.index[i] +' = ' + str(df2_for_plot['score'][i]) for i in range(len(df2_for_plot))]
        ))
    fig.add_trace(go.Scatterpolar(
        r=df3_for_plot['score'],
        theta=df3_for_plot.index,
        fill='toself',
        marker_color='rgb(235,129,129)',
        hoverinfo="text",
        name=text_scores_3,
        text=[df3_for_plot.index[i] + ' = ' + str(df3_for_plot['score'][i]) for i in range(len(df3_for_plot))]
    ))
    fig.add_trace(go.Scatterpolar(
        r=df4_for_plot['score'],
        theta=df4_for_plot.index,
        fill='toself',
        marker_color='rgb(167,156,225)',
        hoverinfo="text",
        name=text_scores_4,
        text=[df4_for_plot.index[i] + ' = ' + str(df4_for_plot['score'][i]) for i in range(len(df4_for_plot))]
    ))

    fig.update_layout(
        polar=dict(
            hole=0.1,
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                type='linear',
                autotypenumbers='strict',
                autorange=False,
                range=[0, 1],
                angle=90,
                showline=False,
                showticklabels=False, ticks='',
                gridcolor='black'),
                ),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="black",
        font_size= 13
    )

    return [go.Figure(data=fig)]

# callback functions for TOP ARTISTS AND MUSIC

@app.callback(
    [
        Output("song_name_1", "children"),
        Output("artist_name_1", "children"),
        Output("song_name_2", "children"),
        Output("artist_name_2", "children"),
        Output("song_name_3", "children"),
        Output("artist_name_3", "children"),
    ],
    [
        Input("slider_years", "value"),
    ]
)
def indicator(year):
    artist_name_1 =  top_data.loc[top_data['year'] == year].sort_values(by='popularity', ascending=False)['artist'].values[0]
    song_name_1 = top_data.loc[top_data['year'] == year].sort_values(by='popularity', ascending=False)['name'].values[0]
    artist_name_2 = top_data.loc[top_data['year'] == year].sort_values(by='popularity', ascending=False)['artist'].values[1]
    song_name_2 = top_data.loc[top_data['year'] == year].sort_values(by='popularity', ascending=False)['name'].values[1]
    artist_name_3 = top_data.loc[top_data['year'] == year].sort_values(by='popularity', ascending=False)['artist'].values[2]
    song_name_3 = top_data.loc[top_data['year'] == year].sort_values(by='popularity', ascending=False)['name'].values[2]

    return 'Top song is ' + song_name_1, \
           'Top artist is ' +artist_name_1, \
           'Top song is ' + song_name_2 + '    ', \
           'Top artist is ' + artist_name_2, \
           'Top song is ' + song_name_3, \
           'Top artist is ' + artist_name_3



if __name__ == '__main__':
    app.run_server(debug=True)