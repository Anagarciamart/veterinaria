import streamlit as st
import requests
from datetime import datetime
import re  # Para las expresiones regulares

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

    # Funciones de validación para los campos
    def validar_dni(dni):
        return bool(re.match(r"^\d{8}[A-Za-z]$", dni))  # 8 dígitos seguidos de una letra

    def validar_telefono(telefono):
        return bool(re.match(r"^\d{9}$", telefono))  # 9 dígitos

    def validar_direccion(direccion):
        return bool(re.match(r"^[a-zA-Z0-9\s,.-]+$", direccion))  # letras, números y algunos símbolos

    def validar_email(email):
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))  # formato básico de email

    # Formulario para registrar un dueño
    with st.form("form_dueño"):
        name = st.text_input("Nombre del Dueño")
        dni = st.text_input("DNI del Dueño")
        address = st.text_input("Dirección del Dueño")
        email = st.text_input("Correo Electrónico del Dueño")
        phone = st.text_input("Teléfono del Dueño")
        date = st.date_input("Fecha de Registro")
        submit_button = st.form_submit_button(label="Registrar Dueño")

    if submit_button:
        # Validar cada campo
        if not name or not dni or not address or not email or not phone:
            st.error("Por favor, complete todos los campos.")
        elif not validar_dni(dni):
            st.error("El DNI debe tener el formato 12345678A (8 dígitos seguidos de una letra).")
        elif not validar_telefono(phone):
            st.error("El teléfono debe tener 9 dígitos numéricos.")
        elif not validar_direccion(address):
            st.error("La dirección debe contener letras, números y algunos símbolos como , . y -.")
        elif not validar_email(email):
            st.error("El correo electrónico debe tener el formato: ejemplo@dominio.com.")
        else:
            # Si todas las validaciones son correctas, enviar los datos al microservicio
            payload = {
                "option": "Registrar Dueño",
                "name": name,
                "dni": dni,
                "address": address,
                "email": email,
                "phone": phone,
                "date": date.isoformat(),
                # Proporcionar valores predeterminados para amount y description
                "description": "Registro automático",  # Texto predeterminado
                "amount": 0.0  # Valor numérico predeterminado
            }

            try:
                response = requests.post(url, json=payload)

                if response.status_code == 200:
                    st.success("Dueño registrado correctamente.")
                    # Volver al menú principal automáticamente
                    st.session_state.page = 'inicio'
                else:
                    # Mostrar el mensaje del error que envía el servidor
                    st.error(f"Error al registrar el dueño: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error al conectar con el servidor: {e}")

# Página para registrar mascota
elif st.session_state.page == 'registrar_mascota':
    st.subheader("Registrar Mascota")


    # Funciones de validación para los campos
    def validar_nombre(nombre):
        return bool(re.match(r"^[a-zA-Z\s]+$", nombre))  # Solo letras y espacios


    def validar_raza(raza):
        return bool(re.match(r"^[a-zA-Z\s]+$", raza))  # Solo letras y espacios


    # Formulario para registrar una mascota
    with st.form("form_mascota"):
        pet_name = st.text_input("Nombre de la Mascota")
        pet_type = st.selectbox("Tipo de Mascota", ["Perro", "Gato"])
        breed = st.text_input("Raza de la Mascota")
        birthdate = st.date_input("Fecha de Nacimiento de la Mascota")
        medical_conditions = st.text_area("Patologías Previas de la Mascota")

        # Campos relacionados con el dueño
        owner_dni = st.text_input("DNI del Dueño (existente o nuevo)")
        submit_button = st.form_submit_button(label="Registrar Mascota")

    if submit_button:
        # Validar campos de la mascota
        if not pet_name or not pet_type or not breed or not owner_dni:
            st.error("Por favor, complete todos los campos.")
        elif not validar_nombre(pet_name):
            st.error("El nombre de la mascota solo puede contener letras y espacios.")
        elif not validar_raza(breed):
            st.error("La raza de la mascota solo puede contener letras y espacios.")
        elif not re.match(r"^\d{8}[A-Za-z]$", owner_dni):
            st.error("El DNI del dueño debe tener el formato 12345678A (8 dígitos seguidos de una letra).")
        else:
            # Si todas las validaciones son correctas, enviar los datos al microservicio
            payload = {
                "option": "Registrar Mascota",
                "pet_name": pet_name,
                "pet_type": pet_type,
                "breed": breed,
                "birthdate": birthdate.isoformat(),
                "medical_conditions": medical_conditions,
                "owner_dni": owner_dni,
                # Campos adicionales requeridos por el microservicio
                "date": birthdate.isoformat(),  # Por ejemplo, puedes usar la fecha de nacimiento como registro
                "description": "Registro de mascota",  # Texto predeterminado
                "amount": 0.0  # Valor numérico predeterminado
            }

            try:
                response = requests.post(url, json=payload)

                if response.status_code == 200:
                    st.success("Mascota registrada correctamente.")
                    # Volver al menú principal automáticamente
                    st.session_state.page = 'inicio'
                else:
                    # Mostrar el mensaje del error que envía el servidor
                    st.error(f"Error al registrar la mascota: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error al conectar con el servidor: {e}")

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
