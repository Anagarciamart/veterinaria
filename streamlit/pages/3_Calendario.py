import streamlit as st
from streamlit_calendar import calendar
import requests
from datetime import datetime, time

st.title("Gestión de citas 📆")

BACKEND_URL = "http://fastapi:8000"  # URL del backend FastAPI

# Inicialización de variables de sesión
if "events" not in st.session_state:
    st.session_state["events"] = []

if "selected_date" not in st.session_state:
    st.session_state["selected_date"] = None

# Función para enviar datos al backend
def send_cita(data):
    try:
        response = requests.post(f"{BACKEND_URL}/crear-cita", json=data)
        if response.status_code == 200:
            cita_creada = response.json()
            return True, cita_creada  # Devuelve la cita completa con el ID asignado
        else:
            return False, response.json().get("detail", "Error desconocido")
    except Exception as e:
        return False, str(e)

# Función para mover una cita
def update_cita(cita_id, nueva_fecha):
    try:
        response = requests.put(f"{BACKEND_URL}/modificar-cita/{cita_id}", json={"nueva_fecha": nueva_fecha})
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Error desconocido")
    except Exception as e:
        return False, str(e)


# Función para cancelar una cita
def cancel_cita(cita_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/cancelar-cita/{cita_id}")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Error desconocido")
    except Exception as e:
        return False, str(e)


# Formulario para agregar citas
def agregar_cita_popup():
    with st.form("form_cita"):
        st.write("Ingrese los detalles de la cita:")

        # Fecha seleccionada automáticamente
        fecha_seleccionada = st.session_state["selected_date"]
        st.write(f"Fecha seleccionada: {fecha_seleccionada}")

        # Inputs para las horas
        hora_inicio = st.time_input("Selecciona la hora de inicio:", value=time(9, 0))
        hora_fin = st.time_input("Selecciona la hora de fin:", value=time(10, 0))

        tratamiento = st.text_input("Tratamiento:")
        dni_dueño = st.text_input("DNI del dueño:")
        mascota = st.text_input("Nombre de la mascota:")

        enviado = st.form_submit_button("Crear cita")

        if enviado:
            # Combinar fecha seleccionada con las horas
            fecha_hora_inicio = datetime.combine(fecha_seleccionada, hora_inicio).isoformat() + "Z"
            fecha_hora_fin = datetime.combine(fecha_seleccionada, hora_fin).isoformat() + "Z"

            nueva_cita = {
                "id": len(st.session_state["events"]) + 1,
                "owner_dni": dni_dueño,
                "pet_name": mascota,
                "treatment": tratamiento,
                "start_time": fecha_hora_inicio,
                "end_time": fecha_hora_fin,
            }
            success, response = send_cita(nueva_cita)
            if success:
                st.success("Cita creada con éxito.")
                st.session_state["events"].append({
                    "id": nueva_cita["id"],
                    "title": f"{mascota} - {tratamiento}",
                    "color": "#FF6C6C",
                    "start": fecha_hora_inicio,
                    "end": fecha_hora_fin,
                })
            else:
                st.error(f"Error al crear cita: {response}")


# Función para editar citas
def editar_cita_popup(event_id):
    with st.form(f"edit_cita_{event_id}"):
        st.write("Modifique los detalles de la cita:")
        tratamiento = st.text_input("Tratamiento:")
        nueva_fecha_inicio = st.date_input("Nueva fecha de inicio:")
        nueva_fecha_fin = st.date_input("Nueva fecha de fin:")

        enviado = st.form_submit_button("Modificar cita")

        if enviado:
            success, response = update_cita(event_id, nueva_fecha_inicio)
            if success:
                st.success("Cita modificada con éxito.")
                for event in st.session_state["events"]:
                    if event["id"] == event_id:
                        event["start"] = str(nueva_fecha_inicio)
                        event["end"] = str(nueva_fecha_fin)
            else:
                st.error(f"Error al modificar la cita: {response}")

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

def events():
    return[
    {
        "id": 1,
        "title": "Consulta Perrito",
        "color": "#FF6C6C",
        "start": "2024-11-03",
        "end": "2024-11-05",
        "resourceId": "a",
    },
    {
        "id": 2,
        "title": "Consulta Gatito",
        "color": "#FFBD45",
        "start": "2024-11-01",
        "end": "2024-11-10",
        "resourceId": "b",
    },
    {
        "id": 3,
        "title": "Consulta Perrito",
        "color": "#FF4B4B",
        "start": "2024-11-20",
        "end": "2024-11-20",
        "resourceId": "c",
    },
]

if not st.session_state["events"]:
    st.session_state["events"] = events()

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

if state.get("eventClick"):
    event_data = state["eventClick"]["event"]
    cita_id = event_data.get("id")


# Manejar selección de rango en el calendario
if state.get("select") is not None:
    st.session_state["time_inicial"] = state["select"]["start"]
    st.session_state["time_final"] = state["select"]["end"]

    with st.form("crear_cita_form"):
        tratamiento = st.text_input("Tratamiento:")
        dni_dueno = st.text_input("DNI del dueño:")
        mascota = st.text_input("Nombre de la mascota:")
        enviado = st.form_submit_button("Crear Cita")

        if enviado:
            nueva_cita = {
                "id": len(st.session_state["events"]) + 1,
                "title": f"{mascota} - {tratamiento}",
                "start": st.session_state["time_inicial"],
                "end": st.session_state["time_final"],
                "color": "#FF6C6C",
            }
            st.session_state["events"].append(nueva_cita)
            st.success("Cita creada exitosamente.")

# Manejar selección de rango en el calendario
if state.get("dateClick") is not None:
    clicked_date = state["dateClick"]["date"]
    # Extraer la fecha sin modificarla
    selected_date = datetime.strptime(clicked_date.split("T")[0], "%Y-%m-%d").date()
    st.session_state["selected_date"] = selected_date
    agregar_cita_popup()

# Mover cita en el calendario
if state.get("eventChange"):
    event_data = state["eventChange"]["event"]
    cita_id = event_data["id"]
    nueva_fecha = event_data["start"]

    response = requests.put(f"{BACKEND_URL}/modificar-cita/{cita_id}", json={"nueva_fecha": nueva_fecha})
    if response.status_code == 200:
        st.success("Cita actualizada exitosamente.")
    else:
        st.error("Error al actualizar la cita.")

# Cancelar cita
if state.get("eventClick"):
    if st.button("Eliminar Cita"):
        event_data = state["eventClick"]["event"]
        cita_id = event_data["id"]

        success, response = cancel_cita(cita_id)
        if success:
            st.success("Cita cancelada exitosamente.")
            st.session_state["events"] = [e for e in st.session_state["events"] if e["id"] != cita_id]
            st.rerun()
        else:
            st.error(f"Error al cancelar la cita: {response}")