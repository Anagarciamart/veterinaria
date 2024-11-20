import streamlit as st
import requests
from datetime import datetime

# URL del microservicio FastAPI
url = "http://fastapi:8000/envio/"

# Título principal de la app
st.title("Ejemplo: formulario para dar la entrada de datos 🖥️🖥")

# Usamos st.session_state para mantener el estado entre las páginas
if 'page' not in st.session_state:
    st.session_state.page = 'inicio'

# Página de inicio
if st.session_state.page == 'inicio':
    st.subheader("Selecciona una opción para continuar:")

    # Selección de la opción principal
    option = st.selectbox("Opción",
                          ["Registrar Dueño", "Registrar mascota", "Buscar Dueño/Mascota", "Eliminar Dueño/Mascota"])

    # Botón para enviar y redirigir a la página correspondiente
    if st.button('Enviar'):
        # Cambiar el estado de la página según la opción elegida
        if option == "Registrar Dueño":
            st.session_state.page = 'registrar_dueño'
        elif option == "Registrar mascota":
            st.session_state.page = 'registrar_mascota'
        elif option == "Buscar Dueño/Mascota":
            st.session_state.page = 'buscar_dueño_mascota'
        elif option == "Eliminar Dueño/Mascota":
            st.session_state.page = 'eliminar_dueño_mascota'

# Página para registrar dueño
elif st.session_state.page == 'registrar_dueño':
    st.subheader("Registrar Dueño")

    # Formulario para registrar un dueño
    with st.form("form_dueño"):
        name = st.text_input("Nombre del Dueño")
        contact = st.text_input("Contacto del Dueño")
        submit_button = st.form_submit_button(label="Registrar Dueño")

    if submit_button:
        # Aquí puedes enviar los datos a tu microservicio o almacenarlos
        payload = {
            "option": "Registrar Dueño",
            "name": name,
            "contact": contact
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("Dueño registrado correctamente")
        else:
            st.error("Error al registrar el dueño")

    # Botón para volver a la página principal
    if st.button('Volver'):
        st.session_state.page = 'inicio'

# Página para registrar mascota
elif st.session_state.page == 'registrar_mascota':
    st.subheader("Registrar Mascota")

    # Formulario para registrar una mascota
    with st.form("form_mascota"):
        pet_name = st.text_input("Nombre de la Mascota")
        pet_type = st.selectbox("Tipo de Mascota", ["Perro", "Gato", "Otro"])
        pet_age = st.number_input("Edad de la Mascota", min_value=0, step=1)
        submit_button = st.form_submit_button(label="Registrar Mascota")

    if submit_button:
        # Aquí puedes enviar los datos a tu microservicio o almacenarlos
        payload = {
            "option": "Registrar Mascota",
            "pet_name": pet_name,
            "pet_type": pet_type,
            "pet_age": pet_age
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("Mascota registrada correctamente")
        else:
            st.error("Error al registrar la mascota")

    # Botón para volver a la página principal
    if st.button('Volver'):
        st.session_state.page = 'inicio'

# Página para buscar dueño o mascota
elif st.session_state.page == 'buscar_dueño_mascota':
    st.subheader("Buscar Dueño/Mascota")

    # Formulario para realizar la búsqueda
    with st.form("form_buscar"):
        search_query = st.text_input("Buscar por Nombre o ID")
        submit_button = st.form_submit_button(label="Buscar")

    if submit_button:
        # Aquí puedes hacer la solicitud para buscar dueño o mascota
        payload = {"option": "Buscar Dueño/Mascota", "search_query": search_query}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("Resultado de la búsqueda:")
            st.json(response.json())
        else:
            st.error("Error al realizar la búsqueda")

    # Botón para volver a la página principal
    if st.button('Volver'):
        st.session_state.page = 'inicio'

# Página para eliminar dueño o mascota
elif st.session_state.page == 'eliminar_dueño_mascota':
    st.subheader("Eliminar Dueño/Mascota")

    # Formulario para eliminar dueño o mascota
    with st.form("form_eliminar"):
        delete_id = st.text_input("ID del Dueño o Mascota a Eliminar")
        submit_button = st.form_submit_button(label="Eliminar")

    if submit_button:
        # Aquí puedes hacer la solicitud para eliminar dueño o mascota
        payload = {"option": "Eliminar Dueño/Mascota", "delete_id": delete_id}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("Dueño o Mascota eliminados correctamente")
        else:
            st.error("Error al eliminar el dueño o mascota")

    # Botón para volver a la página principal
    if st.button('Volver'):
        st.session_state.page = 'inicio'
