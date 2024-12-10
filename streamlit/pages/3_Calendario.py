import streamlit as st

from streamlit_calendar import calendar

import requests


st.title("Gestión de citas 📆")

BACKEND_URL = "http://fastapi:8000/citas"  # URL del backend FastAPI

# Funciones auxiliares
def enviar_cita(animal, dueno, tratamiento, inicio, fin):
    data = {
        "animal": animal,
        "dueno": dueno,
        "tratamiento": tratamiento,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
    }
    response = requests.post(BACKEND_URL, json=data)
    return response

def obtener_citas():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        return response.json()
    return []

def actualizar_cita(cita_id, inicio, fin, tratamiento):
    data = {
        "animal": "Actualizado",
        "dueno": "Actualizado",
        "tratamiento": tratamiento,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
    }
    response = requests.put(f"{BACKEND_URL}/{cita_id}", json=data)
    return response

def eliminar_cita(cita_id):
    response = requests.delete(f"{BACKEND_URL}/{cita_id}")
    return response

# Estado inicial
if "citas" not in st.session_state:
    st.session_state["citas"] = obtener_citas()

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

if "resource" in mode:
    if mode == "resource-daygrid":
        calendar_options = {
            **calendar_options,
            "initialDate": "2024-11-01",
            "initialView": "resourceDayGridDay",
            "resourceGroupField": "building",
        }
    elif mode == "resource-timeline":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            },
            "initialDate": "2024-11-01",
            "initialView": "resourceTimelineDay",
            "resourceGroupField": "building",
        }
    elif mode == "resource-timegrid":
        calendar_options = {
            **calendar_options,
            "initialDate": "2023-07-01",
            "initialView": "resourceTimeGridDay",
            "resourceGroupField": "building",
        }
else:
    if mode == "daygrid":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "initialDate": "2024-11-01",
            "initialView": "dayGridMonth",
        }
    elif mode == "timegrid":
        calendar_options = {
            **calendar_options,
            "initialView": "timeGridWeek",
        }
    elif mode == "timeline":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "timelineDay,timelineWeek,timelineMonth",
            },
            "initialDate": "2024-11-01",
            "initialView": "timelineMonth",
        }
    elif mode == "list":
        calendar_options = {
            **calendar_options,
            "initialDate": "2024-11-01",
            "initialView": "listMonth",
        }
    elif mode == "multimonth":
        calendar_options = {
            **calendar_options,
            "initialView": "multiMonthYear",
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
    key=mode,
)

# Manejo de clic en un evento
if state.get("select"):
    with st.form("registro_cita"):
        animal = st.text_input("Animal")
        dueno = st.text_input("Dueño")
        tratamiento = st.text_input("Tratamiento")
        enviado = st.form_submit_button("Registrar")
    if enviado:
        inicio = state["select"]["start"]
        fin = state["select"]["end"]
        response = enviar_cita(animal, dueno, tratamiento, inicio, fin)
        if response.status_code == 200:
            st.session_state["citas"] = obtener_citas()
            st.success("Cita registrada correctamente")
        else:
            st.error(f"Error: {response.text}")

if state.get("eventClick"):
    evento_id = state["eventClick"]["event"]["id"]
    st.info(f"Evento seleccionado: {evento_id}")
    if st.button("Eliminar cita"):
        response = eliminar_cita(evento_id)
        if response.status_code == 200:
            st.session_state["citas"] = obtener_citas()
            st.success("Cita eliminada correctamente")
        else:
            st.error(f"Error al eliminar cita: {response.text}")

if state.get("eventChange"):
    evento_id = state["eventChange"]["event"]["id"]
    inicio = state["eventChange"]["event"]["start"]
    fin = state["eventChange"]["event"]["end"]
    tratamiento = state["eventChange"]["event"]["title"]
    response = actualizar_cita(evento_id, inicio, fin, tratamiento)
    if response.status_code == 200:
        st.session_state["citas"] = obtener_citas()
        st.success("Cita actualizada correctamente")
    else:
        st.error(f"Error al actualizar cita: {response.text}")
