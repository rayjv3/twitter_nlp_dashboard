import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
from scraper import *
from figures import *
from nlp import *
from sankey_dash import *
from collections import Counter


"""Creates a plotly dashboard granting the user the ability to interact with indicators of sunspot activity
"""

def blank_fig():
    """ generates blank figure with no visual elements so default dcc.graph doesnt show """
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig


# create the layout
app = Dash(__name__)

# define the layout
app.layout = html.Div([
    html.Div([
        html.H1('Twitter NLP Dashboard',
                style={'font-size': '3em', 'text-align': 'center', 'margin': '0px', 'text-stroke-width': '2px',
                       'text-stroke-color': 'black'}),
        html.P(['Welcome to the Twitter NLP Dashboard!', html.Br(),
                'Perform sentiment analysis on tweets about any topic you want,'
                'whenever you want, straight from Twitter!'],
                 style={'text-align': 'center', 'font-size': '20px', 'marginTop': '10px'})
    ], id='top-container',
        style={'width': '100%', 'background-color': '#266150', 'border-radius': '22px', 'height': '110px',
               'color': 'white'}),

    html.Div([
        html.Div([
            html.Plaintext("What/Who do you want to see analysis on?",
                           style={'font-family': 'Times New Roman', 'font-size': '18px',
                                  'font-weight': 'bold', 'marginTop': '60px'}),
            dcc.Input(id="search_query", type="text", placeholder="",
                      style={'height': '40px', 'width': '300px',
                             'text-align': 'center', 'marginTop': '5px'}),
            html.Br(),
            html.Div([
                html.Plaintext('Enter dates to search between or leave blank to search all of Twitter',
                               style={'font-family': 'Times New Roman', 'marginBottom': '2px', 'font-size': '18px'}),
                dcc.Input(id='start-date', type='text', placeholder='YYYY-MM-DD',
                          style={'height': '20px', 'width': '100px', 'marginRight': '5px', 'text-align': 'center',
                                 'marginTop': '2px'}),
                html.Plaintext(' - ',
                               style={'marginLeft': '2.5px', 'marginRight': '2.5px', 'display': 'inline-block'}),
                dcc.Input(id='end-date', type='text', placeholder='YYYY-MM-DD',
                          style={'height': '20px', 'width': '100px', 'marginRight': '5px', 'text-align': 'center',
                                 'display': 'inline-block'}),
                     ], id='date-collector-elements'),
            html.Div([
                html.Plaintext('How many tweets would you like to search?',
                               style={'font-family': 'Times New Roman', 'marginBottom': '2px', 'font-size': '18px'}),
                html.Plaintext('*Note that the more tweets you collect, the longer the page will take to load!',
                               style={'font-family': 'Time New Roman', 'font-size': '16px', 'marginTop': '0px',
                                      'marginBottom': '1px'}),
                dcc.Slider(10, 1000, 5,
                           value=500,
                           id='num-tweets-slider',
                           marks=None,
                           tooltip={'placement': 'top', 'always_visible': True})
            ], id='num-tweets-elements'),
            html.Button('search', id='search_button', n_clicks=None,
                        style={'width': '400px', 'height': '60px',
                               'cursor': 'pointer', 'border': '0px',
                               'border-radius': '5px', 'background-color': '#266150',
                               'color': 'white', 'text-transform': 'uppercase',
                               'font-size': '15px', 'marginTop': '10px'}),
            ], id='left-container',
                style={'height': '500px', 'width': '500px', 'background-color': '#E8CEBF',
                       'float': 'left', 'marginTop': '5px', 'text-align': 'center', 'border-radius': '20px'}),

        html.Div([
            dcc.Dropdown(['Sentiment Pie Chart', 'Sankey Diagram', 'Sentiment Distribution'], 'Sentiment Pie Chart',
                         id='graph-dropdown',
                         style={'width': '300px', 'height': '15px'}),
            dcc.Graph(id="pie_chart", figure=blank_fig(),
                      style={'height': '465px', 'width': '615px', 'marginLeft': '10px', 'marginTop': '21px'})

        ], id='middle-container',
            style={'marginLeft': '10px', 'height': '500px', 'width': '410px',
                   'display': 'inline-block', 'marginTop': '5px', 'border-radius': '20px'}),

        html.Div([
            html.Div([
                html.Plaintext('Most Positive Tweet:',
                               style={'font-family': 'Times New Roman',
                                      'font-weight': 'bold', 'marginTop': '140px', 'font-size': '18px'}),
                html.Br(),
                html.Div(id='positive-output', style={'marginLeft': '20px'}),
                html.Br(),
                html.Br(),
                html.Plaintext('Most Negative Tweet:',
                               style={'font-family': 'Times New Roman',
                                      'font-weight': 'bold', 'font-size': '18px'}),
                html.Div(id='negative-output',  style={'marginLeft': '20px'})
                    ])
        ], id="right-container",
            style={'float': 'right', 'background-color': '#E8CEBF', 'width': '400px', 'height': '500px',
                   'marginTop': '5px', 'display': 'inline-block', 'text-align': 'center', 'border-radius': '20px'}),

        ]),

    html.Div([
        html.Br(),
        html.P('All Collected Tweets and Their Sentiment Score',
               style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold'}),
        dash_table.DataTable(
            id='data-table',
            data=[],
            columns=[{'name': 'Tweet', 'id': 'Text'},
                     {'name': 'Sentiment Score', 'id': 'sentiments'}],
            style_cell={'textAlign': 'center', 'width': '40%'},
            style_header={'backgroundColor': '#266150', 'textAlign': 'center', 'fontWeight': 'Bold', 'color': 'white'},
            style_table={'height': '300px', 'overflowY': 'auto'},
            fixed_rows={'headers': True},
            style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'}
        )

        ], id='bottom-container',
       style={'width': '100%', 'height': '400px', 'background-color': '#DDAF94', 'marginTop': '5px',
              'border-radius': '20px'}),

    html.Div([
        html.Div([
            html.P('Created by Catherine Eng, Denneen Macariola, and Raymond Valenzuela',
                   style={'marginLeft': '10px', 'marginTop': '20px', 'marginBottom': '2px'}),
            html.P('DS3500 Final Project, 4/19/2023',
                   style={'marginLeft': '10px', 'marginTop': '2px'})
        ]),
    ], id='footer-container', style={'background-color': '#4F4846', 'width': '100%', 'height': '45px',
                                     'marginTop': '5px', 'border-radius': '20px', 'color': 'white'})
    ])


# make functional
@app.callback(
    Output('pie_chart', 'figure'),
    Input('search_button', 'n_clicks'),
    Input('search_query', 'value'),
    Input('start-date', 'value'),
    Input('end-date', 'value'),
    Input('num-tweets-slider', 'value'),
    Input('graph-dropdown', 'value')
)
def display_figures(n_clicks, query, start, end, n, dropdown):

    if n_clicks == None:
        return go.Figure()

    else:
        tweet_data = scrape(query, start=start, end=end, n=n)
        tweet_data = clean_tweets(tweet_data)

        if dropdown == 'Sentiment Pie Chart':
            fig = create_pie(tweet_data, query)

        if dropdown == 'Sankey Diagram':
            # count total words in tweets
            words = []
            for tweet in tweet_data['Text']:
                tweet = tweet.split(" ")
                for word in tweet:
                    if word not in query.lower():
                        words.append(word)

            # get word count in series
            wordcount = Counter(words)

            # convert wordcount to df
            wordcount_df = pd.DataFrame.from_dict(wordcount, orient='index').reset_index()
            wordcount_df = wordcount_df.rename(columns={'index': 'word', 0: 'count'})
            wordcount_df['topic'] = query
            print(wordcount_df)

            fig = make_sankey(wordcount_df[0:30], 'topic', 'word', vals='count')
            fig.update_layout(title_text = f"30 Most Common Words Found in Tweets Mentioning {query}")

        if dropdown == "Sentiment Distribution":

            #Creates histogram
            fig = create_hist(tweet_data, query)

        return fig


@app.callback(
    Output('positive-output', 'children'),
    Output('negative-output', 'children'),
    Output('data-table', 'data'),
    Input('search_button', 'n_clicks'),
    Input('search_query', 'value'),
    Input('start-date', 'value'),
    Input('end-date', 'value'),
    Input('num-tweets-slider', 'value')
)
def display_tweets(n_clicks, query, start, end, n):
    """ Displays most positive tweet found """
    if n_clicks is None:
        return "", "", [{"Text" : "", "sentiments": ""}]

    else:
        raw_data = scrape(query, start=start, end=end, n=n)
        tweet_data = clean_tweets(raw_data)

        analyzed = analyze_sentiment(tweet_data, sorted=True)
        neg_tweet = analyzed['Raw Text'][0]
        pos_tweet = analyzed['Raw Text'][len(analyzed)-1]

        non_sorted = analyze_sentiment(tweet_data)
        #print(non_sorted.iloc[:, [5, 6]])
        #data = non_sorted.iloc[:, [3, 6]].to_dict(orient='records')

        #print(non_sorted[["stopwords_in", "sentiments"]])
        data = non_sorted[["Text", "sentiments"]].to_dict(orient='records')

        return pos_tweet, neg_tweet, data



# run the server
app.run_server(debug=False)

