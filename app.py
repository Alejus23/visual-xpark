import streamlit as st
import pandas as pd
import psycopg2
import os

# Conexión a la base de datos Supabase usando variables de entorno
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname="postgres",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port="5432"
)

# Consulta 1: Total recaudado por tipo de vehículo
df_recaudo = pd.read_sql("""
    SELECT t.tipo_vehiculo, SUM(s.total_pago) AS total_recaudado
    FROM xpark.salida s
    JOIN xpark.ingreso i ON s.id_ingreso = i.id_ingreso
    JOIN xpark.vehiculo v ON i.id_vehiculo = v.id_vehiculo
    JOIN xpark.tarifa t ON v.id_tarifa = t.id_tarifa
    GROUP BY t.tipo_vehiculo;
""", conn)

# Consulta 2: Ingresos por fecha
df_ingresos = pd.read_sql("""
    SELECT fecha_ingreso, COUNT(*) AS cantidad
    FROM xpark.ingreso
    GROUP BY fecha_ingreso
    ORDER BY fecha_ingreso;
""", conn)

conn.close()

# Interfaz en Streamlit
st.title("📊 Panel de Visualización XPark")

st.subheader("Recaudo por tipo de vehículo")
st.bar_chart(df_recaudo.set_index("tipo_vehiculo"))

st.subheader("Ingresos por fecha")
st.line_chart(df_ingresos.set_index("fecha_ingreso"))
