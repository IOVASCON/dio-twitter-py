import requests
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import random

# Obtenha os dados da API
response = requests.get("http://localhost:8000/trends")
trends = response.json()

# Dados adicionais
likes = [random.randint(100, 1000) for _ in trends]
retweets = [random.randint(50, 500) for _ in trends]
engagement = [likes[i] + retweets[i] for i in range(len(trends))]

# Extraia os nomes das tendências
trend_names = [trend["name"] for trend in trends]

# Crie um subplot com 2 linhas e 2 colunas
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "bar"}, {"type": "pie"}],
           [{"type": "scatter", "rowspan": 1}, {"type": "table"}]],
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

# Atualize o layout
fig.update_layout(
    height=800,
    title_text="Dashboard Personalizado",
    title_x=0.5,
    plot_bgcolor='lightyellow',
    paper_bgcolor='lightcyan',
    margin=dict(t=50, b=50, l=25, r=25),
    showlegend=False,
    shapes=[
        # Bordas verticais
        go.layout.Shape(type="line", x0=0.5, y0=0, x1=0.5, y1=1, line=dict(color="Black", width=2)),
        # Bordas horizontais
        go.layout.Shape(type="line", x0=0, y0=0.5, x1=1, y1=0.5, line=dict(color="Black", width=2))
    ]
)

# Adicionar bordas visíveis entre as partes
for annotation in fig['layout']['annotations']:
    annotation['font'] = dict(size=14, color='black')

# Exiba o dashboard
fig.show()
