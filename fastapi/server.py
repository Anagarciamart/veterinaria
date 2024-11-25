from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Union

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
    # Verificar si el dueño ya está registrado
    for d in dueños_db:
        if d.dni == dueño.dni:
            raise HTTPException(status_code=400, detail="El DNI ya está registrado.")

    # Agregar dueño a la lista en memoria
    dueños_db.append(dueño)
    return {"mensaje": "Dueño registrado con éxito."}


@app.post("/registrar-mascota/")
def registrar_mascota(mascota: Mascota):
    # Verificar si el dueño está registrado
    dueño = next((d for d in dueños_db if d.dni == mascota.owner_dni), None)
    if not dueño:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")

    # Agregar mascota a la lista en memoria
    mascotas_db.append(mascota)
    return {"mensaje": "Mascota registrada correctamente."}


@app.get("/buscar-dueño/{dni_o_tel}")
def buscar_dueño(dni_o_tel: str):
    # Buscar dueño por DNI o teléfono
    dueño = next((d for d in dueños_db if d.dni == dni_o_tel or d.phone == dni_o_tel), None)
    if not dueño:
        raise HTTPException(status_code=404, detail="No se encontró un dueño con ese DNI o teléfono.")

    # Buscar las mascotas asociadas a este dueño
    mascotas_dueño = [m for m in mascotas_db if m.owner_dni == dueño.dni]
    return {"dueño": dueño, "mascotas": mascotas_dueño}


@app.delete("/eliminar-dueño-y-mascotas/")
def eliminar_dueño_y_mascotas(dni_o_tel: str):
    global dueños_db, mascotas_db

    # Buscar dueño por DNI o teléfono
    dueño = next((d for d in dueños_db if d.dni == dni_o_tel or d.phone == dni_o_tel), None)
    if not dueño:
        raise HTTPException(status_code=404, detail="No se encontró un dueño con ese DNI o teléfono.")

    # Filtrar dueños y mascotas para eliminarlos
    dueños_db = [d for d in dueños_db if d.dni != dueño.dni]
    mascotas_db = [m for m in mascotas_db if m.owner_dni != dueño.dni]

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
