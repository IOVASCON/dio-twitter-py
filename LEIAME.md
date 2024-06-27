# LEIA-ME

## Explicação do Funcionamento do Código

### 1. Problemas com o Acesso à API do Twitter

No início, tentamos utilizar a API do Twitter para obter informações em tempo real. No entanto, devido às limitações do plano gratuito da API do Twitter (ou X), não conseguimos acessar os endpoints necessários para buscar tendências e tweets. A API gratuita fornece acesso limitado e muitas funcionalidades estão disponíveis apenas para planos pagos.

### 2. Armazenamento de Informações

#### Coleta de Dados do Twitter (`collect_data.py`)

O script `collect_data.py` é utilizado para coletar dados do Twitter. Aqui está um resumo do seu funcionamento:

a. collect_data.py

    from src.services import save_tweets

    save_tweets()

b. services.py

    import tweepy
    from src.constants import (
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
        MONGO_CONNECTION_STRING, DB_NAME, COLLECTION_NAME
    )
    from pymongo import MongoClient

    # Autenticação com a API do Twitter
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Conexão com o MongoDB
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Função para coletar tweets do timeline de um usuário
    def _get_user_timeline_tweets(username, api):
        tweets = api.user_timeline(screen_name=username, count=10)
        return [{"text": tweet.text, "created_at": tweet.created_at} for tweet in tweets]

    # Função para salvar os tweets no MongoDB
    def save_tweets():
        tweets = _get_user_timeline_tweets(username="TwitterDev", api=api)
        collection.insert_many(tweets)

## Explicação

Neste exemplo, estamos utilizando o MongoDB para armazenar os dados coletados da API do Twitter.

    Autenticação com a API do Twitter:
        Utilizamos a biblioteca tweepy para autenticação e coleta de dados.
        As credenciais (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) são usadas para autenticar com a API do Twitter.

    Conexão com o MongoDB:
        Utilizamos a biblioteca pymongo para conectar ao MongoDB.
        As informações de conexão (MONGO_CONNECTION_STRING, DB_NAME, COLLECTION_NAME) são usadas para configurar a conexão e selecionar o banco de dados e a coleção onde os dados serão armazenados.

    Função _get_user_timeline_tweets:
        Esta função coleta os tweets mais recentes do timeline de um usuário específico (TwitterDev neste caso) e retorna uma lista de dicionários contendo o texto e a data de criação dos tweets.

    Função save_tweets:
        Esta função chama _get_user_timeline_tweets para obter os tweets e, em seguida, insere esses tweets na coleção do MongoDB.

### Alternativa sem API do Twitter

    Dashboard (dashboard.py)

    import plotly.graph_objs as go
    from plotly.subplots import make_subplots
    import random

    # Dados fictícios
    trend_names = ["#Python", "#DataScience", "#AI", "#MachineLearning", "#DeepLearning", "#BigData", "#Analytics", "#Programming", "#Coding", "#Tech"]
    likes = [random.randint(100, 1000) for _ in trend_names]
    retweets = [random.randint(50, 500) for _ in trend_names]
    engagement = [likes[i] + retweets[i] for i in range(len(trend_names))]

    # Criação dos subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "pie"}], 
            [{"type": "scatter"}, {"type": "table"}]],
        subplot_titles=("Gráfico de Barras", "Gráfico de Pizza", "Gráfico de Dispersão", "Mini Relatório"),
        horizontal_spacing=0.1,
        vertical_spacing=0.15
    )

    # Gráfico de Barras
    fig.add_trace(
        go.Bar(x=trend_names, y=likes, name="Likes", marker=dict(color='lightblue')),
        row=1, col=1
    )

    # Gráfico de Pizza
    fig.add_trace(
        go.Pie(labels=trend_names, values=engagement, name="Engajamento"),
        row=1, col=2
    )

    # Gráfico de Dispersão (Scatter Plot)
    fig.add_trace(
        go.Scatter(x=trend_names, y=retweets, mode='markers', name="Retweets", marker=dict(size=10, color='orange')),
        row=2, col=1
    )

    # Mini Relatório
    fig.add_trace(
        go.Table(
            header=dict(values=["Tendência", "Likes", "Retweets", "Engajamento"], fill_color='paleturquoise', align='left'),
            cells=dict(values=[trend_names, likes, retweets, engagement], fill_color='lavender', align='left')
        ),
        row=2, col=2
    )

    # Layout
    fig.update_layout(
        height=800,
        title_text="Dashboard Personalizado",
        title_x=0.5,
        plot_bgcolor='lightyellow',
        paper_bgcolor='lightcyan',
        margin=dict(t=50, b=50, l=25, r=25),
        showlegend=False,
        shapes=[
            go.layout.Shape(type="line", x0=0.5, y0=0, x1=0.5, y1=1, line=dict(color="Black", width=2)),
            go.layout.Shape(type="line", x0=0, y0=0.5, x1=1, y1=0.5, line=dict(color="Black", width=2))
        ]
    )

    # Anotações
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=14, color='black')

    fig.show()

#### Explicação do Dashboard

    Dados Fictícios:
        Usamos dados gerados aleatoriamente para simular likes, retweets e engajamento de várias tendências.

    Criação de Gráficos:
        Criamos diferentes tipos de gráficos (barras, pizza, dispersão, tabela) e adicionamos aos subplots.

    Layout e Estilo:
        Configuramos o layout para incluir título, bordas visíveis entre os subplots, e cores de fundo para melhorar a visualização.

##### Conclusão

Embora não tenhamos conseguido acessar a API do Twitter devido a limitações do plano, conseguimos criar um dashboard funcional usando dados fictícios para demonstrar a funcionalidade. O MongoDB seria utilizado para armazenar dados reais, caso tivéssemos acesso completo à API. Este exemplo serve como uma base sólida que pode ser expandida quando o acesso à API for obtido ou ao integrar outras fontes de dados.
