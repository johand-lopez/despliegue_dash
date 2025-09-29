import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# ============================
# Datos base
# ============================
df = px.data.gapminder().query("year == 2007")

# Inicializar la app
app = dash.Dash(__name__)
server = app.server  # necesario para despliegue (por ejemplo en Heroku)

# ============================
# Layout
# ============================
app.layout = html.Div([
    html.H1("Análisis de Población por Continente (2007)", style={'textAlign': 'center'}),

    # Dropdown para elegir continente
    dcc.Dropdown(
        id='dropdown-continent',
        options=[{'label': cont, 'value': cont} for cont in df['continent'].unique()],
        value='Asia',
        clearable=False
    ),

    # Gráfico 1: Barras población
    dcc.Graph(id='grafico-poblacion'),

    # Gráfico 2: Pastel porcentaje de población
    dcc.Graph(id='grafico-pastel'),

    # Gráfico 3: Dispersión PIB per cápita vs esperanza de vida
    dcc.Graph(id='grafico-dispersion'),

    # Gráfico 4: Boxplot de esperanza de vida
    dcc.Graph(id='grafico-box')
])

# ============================
# Callbacks
# ============================

# Gráfico de barras
@app.callback(
    dash.dependencies.Output('grafico-poblacion', 'figure'),
    [dash.dependencies.Input('dropdown-continent', 'value')]
)
def actualizar_barras(continente):
    filtro = df[df['continent'] == continente]
    fig = px.bar(
        filtro,
        x='country',
        y='pop',
        title=f'Población en {continente} (2007)',
        labels={'pop': 'Población', 'country': 'País'}
    )
    return fig


# Gráfico de pastel
@app.callback(
    dash.dependencies.Output('grafico-pastel', 'figure'),
    [dash.dependencies.Input('dropdown-continent', 'value')]
)
def actualizar_pastel(continente):
    filtro = df[df['continent'] == continente]
    fig = px.pie(
        filtro,
        names='country',
        values='pop',
        title=f'Participación porcentual de población en {continente} (2007)'
    )
    return fig


# Gráfico de dispersión
@app.callback(
    dash.dependencies.Output('grafico-dispersion', 'figure'),
    [dash.dependencies.Input('dropdown-continent', 'value')]
)
def actualizar_dispersion(continente):
    filtro = df[df['continent'] == continente]
    fig = px.scatter(
        filtro,
        x='gdpPercap',
        y='lifeExp',
        size='pop',
        color='country',
        hover_name='country',
        title=f'PIB per cápita vs. esperanza de vida en {continente} (2007)',
        labels={'gdpPercap': 'PIB per cápita (US$)', 'lifeExp': 'Esperanza de vida (años)'},
        size_max=60
    )
    return fig


# Gráfico de boxplot
@app.callback(
    dash.dependencies.Output('grafico-box', 'figure'),
    [dash.dependencies.Input('dropdown-continent', 'value')]
)
def actualizar_box(continente):
    filtro = df[df['continent'] == continente]
    fig = px.box(
        filtro,
        y='lifeExp',
        points='all',
        title=f'Distribución de la esperanza de vida en {continente} (2007)',
        labels={'lifeExp': 'Esperanza de vida (años)'}
    )
    return fig


# ============================
# Run server
# ============================
if __name__ == '__main__':
    app.run(debug=True)
