import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import psycopg2

# Configura tu conexión (usa tu contraseña real)
conn = psycopg2.connect(
    host="db.texgcqrbzuuwrfrcsxkm.supabase.co",
    port="5432",
    dbname="postgres",
    user="postgres",
    password="Alejo23*"
)

# Realiza una consulta SQL
df = pd.read_sql_query("SELECT * FROM xpark.vehiculos", conn)

# Crea un gráfico (ejemplo: número de vehículos por color)
fig = px.histogram(df, x="color", title="Cantidad de Vehículos por Color")

# Cierra la conexión
conn.close()

# Inicializa la app Dash
app = dash.Dash(__name__)

# Layout de la app
app.layout = html.Div(children=[
    html.H1("Panel de X-PARK"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)
