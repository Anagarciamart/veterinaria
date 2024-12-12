import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import requests

@st.cache_data
def load_data(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    return pd.DataFrame.from_records(data['owners'])  # Cambia a la clave que corresponda en tu API


def info_box(texto, color=None):
    st.markdown(
        f'<div style="background-color:#4EBAE1;opacity:70%">'
        f'<p style="text-align:center;color:white;font-size:30px;">{texto}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


# Carga de datos
df_merged = load_data('http://fastapi:8000/retrieve_data')

# Cálculos para métricas clave
num_owners = df_merged['owner_id'].nunique()
num_pets = df_merged['pet_id'].nunique()
pets_per_owner = round(df_merged.groupby('owner_id')['pet_id'].nunique().mean(), 2)
num_treatments = df_merged['treatment_id'].nunique()
avg_appointments_per_pet = round(df_merged.groupby('pet_id')['appointment_id'].nunique().mean(), 2)

sns.set_palette("pastel")

# Título
st.title("Dashboard de Dueños y Mascotas 🐾")

st.header("Información General")

# Métricas clave
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

with col1:
    col1.subheader('# Dueños')
    info_box(num_owners)
with col2:
    col2.subheader('# Mascotas')
    info_box(num_pets)
with col3:
    col3.subheader('Mascotas por dueño (promedio)')
    info_box(pets_per_owner)
with col4:
    col4.subheader('# Tratamientos únicos')
    info_box(num_treatments)
with col5:
    col5.subheader('Citas por mascota (promedio)')
    info_box(avg_appointments_per_pet)

# Gráficos
tab1, tab2 = st.tabs(["Distribución de especies", "Citas por mes/año"])

# Gráfico de torta o barra para distribución de especies
fig1 = px.pie(
    df_merged,
    names='species',
    title='Distribución de especies de mascotas',
    hole=0.4,
)

# Gráfico de citas por mes
df_merged['appointment_month'] = pd.to_datetime(df_merged['appointment_date']).dt.to_period('M')
appointments_by_month = df_merged.groupby('appointment_month').size().reset_index(name='count')
fig2 = px.bar(
    appointments_by_month,
    x='appointment_month',
    y='count',
    title='Citas por mes',
    labels={'appointment_month': 'Mes', 'count': 'Número de citas'},
)

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme=None, use_container_width=True)