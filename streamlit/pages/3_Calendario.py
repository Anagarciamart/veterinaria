import streamlit as st

from streamlit_calendar import calendar

import requests

st.title("Gestión de citas 📆")

BACKEND_URL = "http://fastapi:8000/citas"  # URL del backend FastAPI

# Función para enviar datos al backend
def send_cita(data):
    try:
        response = requests.post(f"{BACKEND_URL}/crear-cita/", json=data)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

@st.dialog("Agregar nueva cita")
def agregar_cita_popup():
    st.write(f"Ingrese los detalles de la cita:")
    with st.form("form_cita"):
        tratamiento = st.text_input("Tratamiento:")
        dni_dueño = st.text_input("DNI del dueño:")
        mascota = st.text_input("Nombre de la mascota:")
        hora_inicio = st.session_state.get("time_inicial")
        hora_fin = st.session_state.get("time_final")

        enviado = st.form_submit_button("Crear cita")

    if enviado:
        nueva_cita = {
            "id": len(st.session_state.get("events", [])) + 1,
            "owner_dni": dni_dueño,
            "pet_name": mascota,
            "treatment": tratamiento,
            "start_time": hora_inicio,
            "end_time": hora_fin,
        }
        success, response = send_cita(nueva_cita)
        if success:
            st.success("Cita creada con éxito.")
            st.session_state["events"].append(nueva_cita)
        else:
            st.error(f"Error al crear cita: {response}")

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
        "title": "Consulta Perrito",
        "color": "#FF6C6C",
        "start": "2024-11-03",
        "end": "2024-11-05",
        "resourceId": "a",
    },
    {
        "title": "Consulta Gatito",
        "color": "#FFBD45",
        "start": "2024-11-01",
        "end": "2024-11-10",
        "resourceId": "b",
    },
    {
        "title": "Consulta Perrito",
        "color": "#FF4B4B",
        "start": "2024-11-20",
        "end": "2024-11-20",
        "resourceId": "c",
    },
    {
        "title": "Consulta Gatito",
        "color": "#FF6C6C",
        "start": "2024-11-23",
        "end": "2024-11-25",
        "resourceId": "d",
    },
    {
        "title": "Consulta Loro",
        "color": "#FFBD45",
        "start": "2024-11-29",
        "end": "2024-11-30",
        "resourceId": "e",
    },
    {
        "title": "Consulta Guacamayo Ibérico",
        "color": "#FF4B4B",
        "start": "2024-11-28",
        "end": "2024-11-20",
        "resourceId": "f",
    },
    {
        "title": "Estudio",
        "color": "#FF4B4B",
        "start": "2024-11-01T08:30:00",
        "end": "2024-11-01T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Recados",
        "color": "#3D9DF3",
        "start": "2024-11-01T07:30:00",
        "end": "2024-11-01T10:30:00",
        "resourceId": "b",
    },
    {
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

# Manejar selección de rango en el calendario
if state.get("select") is not None:
    st.session_state["time_inicial"] = state["select"]["start"]
    st.session_state["time_final"] = state["select"]["end"]
    agregar_cita_popup()

# Manejar cambios en los eventos
if state.get("eventChange") is not None:
    data = state.get("eventChange")["event"]
    # Aquí puedes llamar a un endpoint para actualizar el evento en el backend
    st.success("Cita actualizada con éxito.")