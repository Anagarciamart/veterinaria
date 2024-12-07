import streamlit as st
import requests

# Configurar URL del backend
BACKEND_URL = "http://fastapi:8000"

st.title("🐾🐾 Gestión de dueños y mascotas 🐾🐾")
# Menú principal
menu = st.selectbox("Bienvenido al Sistema Veterinario, seleccione una opción", [
    "Registrar Dueño",
    "Registrar Mascota",
    "Buscar Dueño",
    "Eliminar Dueño/Mascota"
])


# Función para mostrar mensajes de error o éxito
def mostrar_mensaje(respuesta):
    if respuesta.status_code == 200:
        st.success(respuesta.json()["mensaje"])
    else:
        st.error(f"Error: {respuesta.json()['detail']}")


# Registrar Dueño
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
        dueno = {
            "name": name,
            "dni": dni,
            "address": address,
            "email": email,
            "phone": phone
        }
        respuesta = requests.post(f"{BACKEND_URL}/registrar-dueño/", json=dueno)
        mostrar_mensaje(respuesta)

# Registrar Mascota
elif menu == "Registrar Mascota":
    st.header("Registrar Mascota")

    # Primero, preguntar si el dueño existe
    owner_exists = st.radio("¿El dueño ya está registrado?", ["Sí", "No"])

    if owner_exists == "Sí":
        # Formulario para dueño existente
        with st.form("form_mascota_existente"):
            owner_dni = st.text_input("DNI del Dueño")
            pet_name = st.text_input("Nombre de la Mascota")
            pet_type = st.radio("Tipo de Mascota", ["Perro", "Gato"])
            breed = st.text_input("Raza")
            birthdate = st.date_input("Fecha de Nacimiento")
            medical_conditions = st.text_input("Condiciones Médicas")
            enviado = st.form_submit_button("Registrar Mascota")

        if enviado:
            # Verificar si el dueño existe
            respuesta_dueno = requests.get(f"{BACKEND_URL}/buscar-dueño/{owner_dni}")

            if respuesta_dueno.status_code == 200:
                # Registrar mascota para dueño existente
                mascota = {
                    "owner_dni": owner_dni,
                    "pet_name": pet_name,
                    "pet_type": pet_type,
                    "breed": breed,
                    "birthdate": str(birthdate),
                    "medical_conditions": medical_conditions,
                }
                respuesta_mascota = requests.post(f"{BACKEND_URL}/registrar-mascota/", json=mascota)
                mostrar_mensaje(respuesta_mascota)
            else:
                st.error(f"Error: {respuesta_dueno.json()['detail']}")

    else:
        # Formulario para registrar dueño y mascota simultáneamente
        with st.form("form_mascota_nuevo_dueno"):
            # Datos del dueño
            name = st.text_input("Nombre del Dueño")
            dni = st.text_input("DNI del Dueño")
            address = st.text_input("Dirección")
            email = st.text_input("Correo electrónico")
            phone = st.text_input("Teléfono")

            # Datos de la mascota
            pet_name = st.text_input("Nombre de la Mascota")
            pet_type = st.radio("Tipo de Mascota", ["Perro", "Gato"])
            breed = st.text_input("Raza")
            birthdate = st.date_input("Fecha de Nacimiento")
            medical_conditions = st.text_input("Condiciones Médicas")

            enviado = st.form_submit_button("Registrar Dueño y Mascota")

        if enviado:
            # Primero registrar dueño
            dueno = {
                "name": name,
                "dni": dni,
                "address": address,
                "email": email,
                "phone": phone
            }
            respuesta_dueno = requests.post(f"{BACKEND_URL}/registrar-dueño/", json=dueno)

            if respuesta_dueno.status_code == 200:
                # Luego registrar mascota
                mascota = {
                    "owner_dni": dni,
                    "pet_name": pet_name,
                    "pet_type": pet_type,
                    "breed": breed,
                    "birthdate": str(birthdate),
                    "medical_conditions": medical_conditions,
                }
                respuesta_mascota = requests.post(f"{BACKEND_URL}/registrar-mascota/", json=mascota)
                mostrar_mensaje(respuesta_mascota)
            else:
                st.error(f"Error al registrar dueño: {respuesta_dueno.json()['detail']}")

# Buscar Dueño
elif menu == "Buscar Dueño":
    st.header("Buscar Dueño")
    dni_o_tel = st.text_input("DNI o Teléfono del Dueño")
    if st.button("Buscar"):
        if not dni_o_tel:
            st.error("Por favor, ingrese un DNI o teléfono para realizar la búsqueda.")
        else:
            # Enviar solicitud al backend con el parámetro proporcionado
            respuesta = requests.get(f"{BACKEND_URL}/buscar-dueño/{dni_o_tel}")
            if respuesta.status_code == 200:
                datos = respuesta.json()
                st.subheader("Información del Dueño")
                st.write(datos["dueño"])
                st.subheader("Mascotas Registradas")
                st.write(datos["mascotas"])
            else:
                st.error(f"Error: {respuesta.json()['detail']}")

# Eliminar Dueño/Mascota
elif menu == "Eliminar Dueño/Mascota":
    st.header("Eliminar Dueño/Mascota")
    opcion = st.radio("¿Qué deseas gestionar?", ["Mascota", "Dueño"])

    # Gestión de Mascota
    if opcion == "Mascota":
        st.subheader("Gestión de Mascota")
        dni_dueno = st.text_input("DNI del Dueño")
        nombre_mascota = st.text_input("Nombre de la Mascota")
        accion = st.radio("Acción", ["Marcar como Fallecido", "Eliminar datos"])

        if st.button("Aplicar Acción a Mascota"):
            if not dni_dueno or not nombre_mascota:
                st.error("Por favor, ingrese tanto el DNI del dueño como el nombre de la mascota.")
            else:
                if accion == "Marcar como Fallecido":
                    data = {"owner_dni": dni_dueno, "pet_name": nombre_mascota, "status": "fallecido"}
                    respuesta = requests.put(f"{BACKEND_URL}/actualizar-estado-mascota/", json=data)
                    mostrar_mensaje(respuesta)
                elif accion == "Eliminar datos":
                    data = {"owner_dni": dni_dueno, "pet_name": nombre_mascota}
                    respuesta = requests.delete(f"{BACKEND_URL}/eliminar-mascota/", json=data)
                    mostrar_mensaje(respuesta)

    # Gestión de Dueño
    elif opcion == "Dueño":
        st.subheader("Eliminar Dueño y Mascotas Asociadas")
        dni_o_tel = st.text_input("DNI o Teléfono del Dueño a eliminar")

        if st.button("Eliminar Dueño"):
            if dni_o_tel:
                respuesta = requests.delete(f"{BACKEND_URL}/eliminar-dueño-y-mascotas/?dni_o_tel={dni_o_tel}")
                mostrar_mensaje(respuesta)
            else:
                st.error("Por favor, ingrese un DNI o un Teléfono para eliminar un dueño.")