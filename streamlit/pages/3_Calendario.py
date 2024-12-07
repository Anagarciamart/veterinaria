import streamlit as st

from streamlit_calendar import calendar

import requests


st.title("Gestión de citas 📆")

backend = "http://fastapi:8000/citas"  # URL del backend FastAPI

def send(data):
    try:
        response = requests.post(backend, json=data)
        return response.status_code
    except Exception as e:
        st.error(f"Error al enviar datos: {e}")
        return None

def update_cita(cita_id, data):
    try:
        response = requests.put(f"{backend}/{cita_id}", json=data)
        return response.status_code
    except Exception as e:
        st.error(f"Error al actualizar cita: {e}")
        return None

@st.dialog("Información de la cita")
def popup():
    st.write(f'Fecha de la cita: {st.session_state.get("time_inicial", "")}')
    with st.form("cita_form"):
        tratamiento = st.text_input("Ingrese el tratamiento:")
        animal = st.text_input("Ingrese el nombre del animal:")
        dueno = st.text_input("Ingrese el nombre del dueño:")
        submitted = st.form_submit_button("Guardar")

    if submitted:
        data = {
            "animal": animal,
            "dueno": dueno,
            "tratamiento": tratamiento,
            "fecha": st.session_state.get("time_inicial", "")
        }
        envio = send(data)
        if envio == 200:
            st.success("Cita guardada con éxito, puede cerrar.")
        else:
            st.error("Error al guardar la cita. Código de estado: {}".format(envio))


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
        "title": "Consulta Gatito ",
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

if state.get('select') is not None:
    st.session_state["time_inicial"] = state["select"]["start"]
    st.session_state["time_final"] = state["select"]["end"]
    popup()

if state.get('eventChange') is not None:
    event_data = state['eventChange']['event']
    cita_id = event_data.get('id')
    new_data = {
        "start": event_data.get('start'),
        "end": event_data.get('end'),
    }
    response_code = update_cita(cita_id, new_data)
    if response_code == 200:
        st.success("Cita actualizada con éxito.")
    else:
        st.error("Error al actualizar la cita. Código de estado: {}".format(response_code))

if st.session_state.get("fecha") is not None:
    st.write('Fecha seleccionada:', st.session_state["fecha"])
