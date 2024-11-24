from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from datetime import datetime

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


# Funciones para manejar archivos JSON
def leer_json(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Devuelve una lista vacía si el archivo no existe


def escribir_json(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as file:
        json.dump(datos, file, indent=4, ensure_ascii=False)


# Endpoints
@app.post("/registrar-dueño/")
def registrar_dueño(dueño: Dueño):
    dueños = leer_json("dueño.json")
    for d in dueños:
        if d["dni"] == dueño.dni:
            raise HTTPException(status_code=400, detail="El DNI ya está registrado.")
    dueños.append(dueño.dict())
    escribir_json("dueño.json", dueños)
    return {"mensaje": "Dueño registrado con éxito."}


@app.post("/registrar-mascota/")
def registrar_mascota(mascota: dict):
    # Leer las listas de dueños y mascotas
    dueños = leer_json("dueño.json")
    mascotas_registradas = leer_json("mascota.json")

    # Verificar si el dueño ya está registrado
    dueño = next((d for d in dueños if d["dni"] == mascota["owner_dni"]), None)
    if not dueño:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")

    # Agregar la nueva mascota a la lista de mascotas registradas
    mascotas_registradas.append(mascota)

    # Guardar los cambios
    escribir_json("mascota.json", mascotas_registradas)

    return {"mensaje": "Mascota registrada correctamente."}

@app.get("/buscar-dueño/{dni}")
def buscar_dueño(dni: str):
    dueños = leer_json("dueño.json")
    mascotas = leer_json("mascota.json")

    dueño = next((d for d in dueños if d["dni"] == dni), None)
    if dueño is None:
        raise HTTPException(status_code=404, detail="No se encontró un dueño con ese DNI.")

    mascotas_dueño = [m for m in mascotas if m["owner_dni"] == dni]
    return {"dueño": dueño, "mascotas": mascotas_dueño}


@app.delete("/eliminar-dueño/{dni}")
def eliminar_dueño(dni: str):
    dueños = leer_json("dueño.json")
    mascotas = leer_json("mascota.json")

    # Filtrar los dueños y mascotas para eliminar el dueño y sus mascotas asociadas
    nuevo_dueños = [d for d in dueños if d["dni"] != dni]
    nuevas_mascotas = [m for m in mascotas if m["owner_dni"] != dni]

    if len(nuevo_dueños) == len(dueños):  # No se eliminó ningún dueño
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")

    escribir_json("dueño.json", nuevo_dueños)
    escribir_json("mascota.json", nuevas_mascotas)

    return {"mensaje": "Dueño y sus mascotas eliminados con éxito."}


@app.delete("/eliminar-mascota/")
def eliminar_mascota(data: dict):
    mascotas = leer_json("mascota.json")

    # Filtrar las mascotas para eliminar la mascota específica
    nuevas_mascotas = [m for m in mascotas if
                       not (m["owner_dni"] == data["owner_dni"] and m["pet_name"] == data["pet_name"])]

    if len(nuevas_mascotas) == len(mascotas):  # No se eliminó ninguna mascota
        raise HTTPException(status_code=404, detail="Mascota no encontrada o datos incorrectos.")

    escribir_json("mascota.json", nuevas_mascotas)

    return {"mensaje": "Mascota eliminada con éxito."}
