from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# Modelos
class Dueño(BaseModel):
    name: str
    dni: str
    address: str
    email: str
    phone: str
    date: str = datetime.now().strftime("%Y-%m-%d")

class Mascota(BaseModel):
    owner_dni: str
    pet_name: str
    pet_type: str
    breed: str
    birthdate: str
    medical_conditions: str

# Base de datos en memoria
dueños_db: List[Dueño] = []
mascotas_db: List[Mascota] = []

# Endpoints
@app.post("/registrar-dueño/")
def registrar_dueño(dueño: Dueño):
    for d in dueños_db:
        if d.dni == dueño.dni:
            raise HTTPException(status_code=400, detail="El DNI ya está registrado.")
    dueños_db.append(dueño)
    return {"mensaje": "Dueño registrado con éxito."}

@app.post("/registrar-mascota/")
def registrar_mascota(mascota: Mascota):
    if mascota.pet_type not in ["Perro", "Gato"]:
        raise HTTPException(status_code=400, detail="Solo se permiten mascotas de tipo 'Perro' o 'Gato'.")

    dueño = next((d for d in dueños_db if d.dni == mascota.owner_dni), None)
    if not dueño:
        raise HTTPException(status_code=404, detail="Dueño no encontrado. Registre al dueño primero.")

    mascotas_db.append(mascota)
    return {"mensaje": "Mascota registrada correctamente."}

@app.get("/buscar-dueño/{dni}")
def buscar_dueño(dni: str):
    dueño = next((d for d in dueños_db if d.dni == dni), None)
    if not dueño:
        raise HTTPException(status_code=404, detail="No se encontró un dueño con ese DNI.")

    mascotas_dueño = [m for m in mascotas_db if m.owner_dni == dni]
    return {"dueño": dueño, "mascotas": mascotas_dueño}

@app.delete("/eliminar-dueño/{dni}")
def eliminar_dueño(dni: str):
    global dueños_db, mascotas_db
    nuevo_dueños = [d for d in dueños_db if d.dni != dni]
    nuevas_mascotas = [m for m in mascotas_db if m.owner_dni != dni]

    if len(nuevo_dueños) == len(dueños_db):
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")

    dueños_db = nuevo_dueños
    mascotas_db = nuevas_mascotas

    return {"mensaje": "Dueño y sus mascotas eliminados con éxito."}

@app.delete("/eliminar-mascota/")
def eliminar_mascota(data: Mascota):
    global mascotas_db

    # Filtrar las mascotas para eliminar la mascota específica
    nuevas_mascotas = [m for m in mascotas_db if
                       not (m.owner_dni == data.owner_dni and m.pet_name == data.pet_name)]

    if len(nuevas_mascotas) == len(mascotas_db):  # No se eliminó ninguna mascota
        raise HTTPException(status_code=404, detail="Mascota no encontrada o datos incorrectos.")

    # Actualizar la base de datos en memoria
    mascotas_db = nuevas_mascotas

    return {"mensaje": "Mascota eliminada con éxito."}


@app.put("/actualizar-estado-mascota/")
def actualizar_estado_mascota(data: dict):
    global mascotas_db

    # Buscar la mascota en la base de datos
    mascota = next((m for m in mascotas_db if m.owner_dni == data["owner_dni"] and m.pet_name == data["pet_name"]), None)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada.")

    # Actualizar el estado de la mascota
    mascota_index = mascotas_db.index(mascota)
    mascotas_db[mascota_index].medical_conditions += f"; Estado: {data['status']}"

    return {"mensaje": "Estado de la mascota actualizado correctamente."}
