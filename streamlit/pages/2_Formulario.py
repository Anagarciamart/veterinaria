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
    with st.form("form_mascota"):
        owner_dni = st.text_input("DNI del Dueño")
        pet_name = st.text_input("Nombre de la Mascota")
        pet_type = st.radio("Tipo de Mascota", ["Perro", "Gato"])
        breed = st.text_input("Raza")
        birthdate = st.date_input("Fecha de Nacimiento")
        medical_conditions = st.text_input("Condiciones Médicas")
        enviado = st.form_submit_button("Registrar")

    if enviado:
        # Verificar si el dueño ya existe
        respuesta_dueno = requests.get(f"{BACKEND_URL}/buscar-dueño/{owner_dni}")

        if respuesta_dueno.status_code == 404:  # Dueño no existe, pedir datos
            st.warning("Dueño no encontrado. Por favor, ingrese los datos para registrarlo.")
            with st.form("form_dueño_nuevo"):
                name = st.text_input("Nombre del Dueño")
                address = st.text_input("Dirección del Dueño")
                email = st.text_input("Correo Electrónico")
                phone = st.text_input("Teléfono")
                registrar_dueno = st.form_submit_button("Registrar Dueño")

            if registrar_dueno:
                # Registrar al nuevo dueño en el backend
                nuevo_dueno = {
                    "name": name,
                    "dni": owner_dni,  # Reutilizar el DNI ingresado en el formulario principal
                    "address": address,
                    "email": email,
                    "phone": phone,
                }
                respuesta_nuevo_dueno = requests.post(f"{BACKEND_URL}/registrar-dueño/", json=nuevo_dueno)

                if respuesta_nuevo_dueno.status_code == 200:
                    st.success("Dueño registrado con éxito. Procediendo a registrar la mascota...")
                else:
                    st.error(f"Error: {respuesta_nuevo_dueno.json()['detail']}")
                    st.stop()  # Detener la ejecución si no se pudo registrar el dueño

        elif respuesta_dueno.status_code != 200:
            st.error(f"Error: {respuesta_dueno.json()['detail']}")
            st.stop()

        # Registrar mascota después de verificar o crear el dueño
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
