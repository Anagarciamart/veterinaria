import streamlit as st
import requests

# Configurar URL del backend
BACKEND_URL = "http://fastapi:8000"

# Opciones del menú
menu = st.sidebar.selectbox("Menú", ["Registrar Dueño", "Registrar Mascota", "Buscar Dueño", "Eliminar Dueño/Mascota"])

# Función para mostrar mensajes de error o éxito
def mostrar_mensaje(respuesta):
    if respuesta.status_code == 200:
        st.success(respuesta.json()["mensaje"])
    else:
        st.error(f"Error: {respuesta.json()['detail']}")

# Registrar dueño
if menu == "Registrar Dueño":
    st.header("Registrar Dueño")
    with st.form("form_dueño"):
        name = st.text_input("Nombre")
        dni = st.text_input("DNI")
        address = st.text_input("Dirección")
        email = st.text_input("Correo electrónico")
        phone = st.text_input("Teléfono")
        enviado = st.form_submit_button("Registrar")

    if enviado:
        dueño = {
            "name": name,
            "dni": dni,
            "address": address,
            "email": email,
            "phone": phone
        }
        respuesta = requests.post(f"{BACKEND_URL}/registrar-dueño/", json=dueño)
        mostrar_mensaje(respuesta)

# Registrar mascota
if menu == "Registrar Mascota":
    st.header("Registrar Mascota")
    with st.form("form_mascota"):
        owner_dni = st.text_input("DNI del Dueño")
        pet_name = st.text_input("Nombre de la Mascota")
        pet_type = st.text_input("Tipo de Mascota (Perro o Gato)")
        breed = st.text_input("Raza")
        birthdate = st.date_input("Fecha de Nacimiento")
        medical_conditions = st.text_input("Condiciones Médicas")
        enviado = st.form_submit_button("Registrar")

    if enviado:
        # Primero verificar si el dueño está registrado
        respuesta_dueño = requests.get(f"{BACKEND_URL}/buscar-dueño/{owner_dni}")
        if respuesta_dueño.status_code != 200:
            st.error(f"Error: {respuesta_dueño.json()['detail']}")
        else:
            # Si el dueño está registrado, proceder con el registro de la mascota
            mascota = {
                "owner_dni": owner_dni,
                "pet_name": pet_name,
                "pet_type": pet_type,
                "breed": breed,
                "birthdate": str(birthdate),  # Convertir la fecha a string
                "medical_conditions": medical_conditions
            }
            respuesta_mascota = requests.post(f"{BACKEND_URL}/registrar-mascota/", json=mascota)
            mostrar_mensaje(respuesta_mascota)

# Buscar dueño
elif menu == "Buscar Dueño":
    st.header("Buscar Dueño")
    dni = st.text_input("DNI del Dueño")
    if st.button("Buscar"):
        respuesta = requests.get(f"{BACKEND_URL}/buscar-dueño/{dni}")
        if respuesta.status_code == 200:
            datos = respuesta.json()
            st.subheader("Información del Dueño")
            st.write(datos["dueño"])
            st.subheader("Mascotas Registradas")
            st.write(datos["mascotas"])
        else:
            st.error(f"Error: {respuesta.json()['detail']}")

elif menu == "Eliminar Dueño/Mascota":
    st.header("Eliminar Dueño/Mascota")
    opcion = st.radio("¿Qué deseas eliminar?", ["Dueño", "Mascota"])

    if opcion == "Dueño":
        st.subheader("Eliminar Dueño")
        dni = st.text_input("DNI del Dueño a eliminar")
        if st.button("Eliminar Dueño"):
            # Enviar solicitud al backend para eliminar el dueño
            respuesta = requests.delete(f"{BACKEND_URL}/eliminar-dueño/{dni}")
            mostrar_mensaje(respuesta)

    elif opcion == "Mascota":
        st.subheader("Eliminar Mascota")
        dni_dueño = st.text_input("DNI del Dueño")
        nombre_mascota = st.text_input("Nombre de la Mascota a eliminar")
        if st.button("Eliminar Mascota"):
            # Enviar solicitud al backend para eliminar la mascota
            data = {
                "owner_dni": dni_dueño,
                "pet_name": nombre_mascota
            }
            respuesta = requests.delete(f"{BACKEND_URL}/eliminar-mascota/", json=data)
            mostrar_mensaje(respuesta)