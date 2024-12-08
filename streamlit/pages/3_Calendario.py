import streamlit as st

from streamlit_calendar import calendar

import requests


st.title("Gestión de citas 📆")

BACKEND_URL = "http://fastapi:8000/citas"  # URL del backend FastAPI


def enviar_cita(cita):
    respuesta = requests.post(f"{BACKEND_URL}/citas/", json=cita)
    return respuesta

def eliminar_cita(id_cita):
    respuesta = requests.delete(f"{BACKEND_URL}/citas/{id_cita}")
    return respuesta

mode = st.selectbox(
    "Calendar Mode:",
    (
        "daygrid",
        "timegrid",
        "timeline",
        "resource-daygrid",
        "resource-timegrid",
        "resource-timeline",
        "list",
        "multimonth",
    ),
)

events = [
    {
        "id": "1",  # Añadido id único
        "title": "Consulta Perrito",
        "color": "#FF6C6C",
        "start": "2024-11-03",
        "end": "2024-11-05",
        "resourceId": "a",
    },
    {
        "id": "2",  # Añadido id único
        "title": "Consulta Gatito",
        "color": "#FFBD45",
        "start": "2024-11-01",
        "end": "2024-11-10",
        "resourceId": "b",
    },
    {
        "id": "3",  # Añadido id único
        "title": "Consulta Perrito",
        "color": "#FF4B4B",
        "start": "2024-11-20",
        "end": "2024-11-20",
        "resourceId": "c",
    },
    {
        "id": "4",  # Añadido id único
        "title": "Consulta Gatito",
        "color": "#FF6C6C",
        "start": "2024-11-23",
        "end": "2024-11-25",
        "resourceId": "d",
    },
    {
        "id": "5",  # Añadido id único
        "title": "Consulta Loro",
        "color": "#FFBD45",
        "start": "2024-11-29",
        "end": "2024-11-30",
        "resourceId": "e",
    },
    {
        "id": "6",  # Añadido id único
        "title": "Consulta Guacamayo Ibérico",
        "color": "#FF4B4B",
        "start": "2024-11-28",
        "end": "2024-11-20",
        "resourceId": "f",
    },
    {
        "id": "7",  # Añadido id único
        "title": "Estudio",
        "color": "#FF4B4B",
        "start": "2024-11-01T08:30:00",
        "end": "2024-11-01T10:30:00",
        "resourceId": "a",
    },
    {
        "id": "8",  # Añadido id único
        "title": "Recados",
        "color": "#3D9DF3",
        "start": "2024-11-01T07:30:00",
        "end": "2024-11-01T10:30:00",
        "resourceId": "b",
    },
    {
        "id": "9",  # Añadido id único
        "title": "Revisión Perrito",
        "color": "#3DD56D",
        "start": "2024-11-02T10:40:00",
        "end": "2024-11-02T12:30:00",
        "resourceId": "c",
    },
]

calendar_resources = [
    {"id": "a", "building": "Clinica 1", "title": "Consulta A"},
    {"id": "b", "building": "Clinica 1", "title": "Consulta A"},
    {"id": "c", "building": "Clinica 1", "title": "Consulta B"},
    {"id": "d", "building": "Clinica 1", "title": "Consulta B"},
    {"id": "e", "building": "Clinica 1", "title": "Consulta A"},
    {"id": "f", "building": "Clinica 1", "title": "Consulta B"},
]

calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "resources": calendar_resources,
    "selectable": "true",
    "initialDate": "2024-11-01",
    "initialView": "resourceTimeGridDay",
    "resourceGroupField": "building",
}

state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key='timegrid',
)

# Alta de cita
if state.get("select"):
    st.sidebar.header("Registrar Cita")
    with st.sidebar.form("form_cita"):
        animal = st.text_input("Nombre del Animal")
        dueno = st.text_input("Nombre del Dueño")
        tratamiento = st.text_input("Tratamiento")
        enviado = st.form_submit_button("Registrar")

    if enviado:
        cita = {
            "animal": animal,
            "dueno": dueno,
            "tratamiento": tratamiento,
            "fecha": state["select"]["start"],
        }
        respuesta = enviar_cita(cita)
        if respuesta.status_code == 200:
            st.success("Cita registrada correctamente")
        else:
            st.error("Error al registrar cita")

# Modificación o cancelación de citas
if state.get("eventChange"):
    # Verificamos que el evento tenga un id
    if "id" in state["eventChange"]["event"]:
        cita_id = state["eventChange"]["event"]["id"]
        st.sidebar.header("Actualizar o Cancelar Cita")
        with st.sidebar.form("form_actualizar"):
            fecha = st.text_input("Nueva Fecha", value=state["eventChange"]["event"]["start"])
            enviado = st.form_submit_button("Actualizar")

        if enviado:
            respuesta = eliminar_cita(cita_id)
            if respuesta.status_code == 200:
                st.success("Cita actualizada correctamente")
            else:
                st.error("Error al actualizar cita")
    else:
        st.error("Este evento no tiene un ID asignado.")