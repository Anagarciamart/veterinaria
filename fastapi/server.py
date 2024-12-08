from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

# Modelos
class Dueno(BaseModel):
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

class Cita(BaseModel):
    id: int
    animal: str
    dueno: str
    tratamiento: str
    fecha: str

class Factura(BaseModel):
    id_cita: int
    tratamientos: List[str]
    total: float
    forma_pago: str
    pagada: bool

# Base de datos en memoria
duenos_db: List[Dueno] = []
mascotas_db: List[Mascota] = []
citas = []
facturas = []

# Endpoints
@app.post("/registrar-dueño/")
def registrar_dueno(dueno: Dueno):
    for d in duenos_db:
        if d.dni == dueno.dni:
            raise HTTPException(status_code=400, detail="El DNI ya está registrado.")
    duenos_db.append(dueno)
    return {"mensaje": "Dueño registrado con éxito."}

@app.post("/registrar-mascota/")
def registrar_mascota(mascota: Mascota):
    if mascota.pet_type not in ["Perro", "Gato"]:
        raise HTTPException(status_code=400, detail="Solo se permiten mascotas de tipo 'Perro' o 'Gato'.")

    # Validar que el dueño existe
    dueno = next((d for d in duenos_db if d.dni == mascota.owner_dni), None)
    if not dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado. Registre al dueño primero.")

    # Validar que la mascota no está ya registrada
    mascota_existente = next(
        (m for m in mascotas_db if m.owner_dni == mascota.owner_dni and m.pet_name.lower() == mascota.pet_name.lower()),
        None
    )
    if mascota_existente:
        raise HTTPException(status_code=400, detail="La mascota ya está registrada para este dueño.")

    mascotas_db.append(mascota)
    return {"mensaje": "Mascota registrada correctamente."}

@app.get("/buscar-dueño/{dni_o_tel}")
def buscar_dueno(dni_o_tel: str):
    """
    Busca un dueño por DNI o teléfono y devuelve sus datos junto con sus mascotas registradas.
    """
    # Buscar dueño por DNI o teléfono
    dueno = next((d for d in duenos_db if d.dni == dni_o_tel or d.phone == dni_o_tel), None)
    if not dueno:
        raise HTTPException(status_code=404, detail="No se encontró un dueño con ese DNI o teléfono.")

    # Buscar mascotas asociadas al dueño
    mascotas_dueno = [m for m in mascotas_db if m.owner_dni == dueno.dni]
    return {"dueño": dueno, "mascotas": mascotas_dueno}

@app.delete("/eliminar-dueño-y-mascotas/")
def eliminar_dueno_y_mascotas(dni_o_tel: str):
    """
    Elimina un dueño y todas sus mascotas asociadas de la base de datos.
    """
    global duenos_db, mascotas_db

    # Buscar dueño por DNI o teléfono
    dueno = next((d for d in duenos_db if d.dni == dni_o_tel or d.phone == dni_o_tel), None)
    if not dueno:
        raise HTTPException(status_code=404, detail="No se encontró un dueño con ese DNI o teléfono.")

    # Eliminar las mascotas asociadas al dueño
    mascotas_db = [m for m in mascotas_db if m.owner_dni != dueno.dni]

    # Eliminar al dueño
    duenos_db = [d for d in duenos_db if d != dueno]

    return {"mensaje": "Dueño y sus mascotas asociadas eliminados correctamente."}

@app.delete("/eliminar-mascota/")
def eliminar_mascota(data: dict):
    """
    Elimina una mascota de la base de datos asociada a un dueño.
    """
    global mascotas_db

    # Buscar la mascota
    mascota = next((m for m in mascotas_db if m.owner_dni == data["owner_dni"] and m.pet_name.lower() == data["pet_name"].lower()), None)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada.")

    # Eliminar la mascota
    mascotas_db = [m for m in mascotas_db if m != mascota]
    return {"mensaje": "Mascota eliminada correctamente."}

@app.put("/actualizar-estado-mascota/")
def actualizar_estado_mascota(data: dict):
    """
    Actualiza el estado de una mascota a 'fallecida' u otro estado especificado.
    """
    global mascotas_db

    # Buscar la mascota
    mascota = next((m for m in mascotas_db if m.owner_dni == data["owner_dni"] and m.pet_name.lower() == data["pet_name"].lower()), None)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada.")

    # Actualizar el estado de la mascota
    mascota_index = mascotas_db.index(mascota)
    updated_conditions = f"{mascota.medical_conditions}; Estado: {data['status']}"
    mascotas_db[mascota_index] = Mascota(
        owner_dni=mascota.owner_dni,
        pet_name=mascota.pet_name,
        pet_type=mascota.pet_type,
        breed=mascota.breed,
        birthdate=mascota.birthdate,
        medical_conditions=updated_conditions
    )

    return {"mensaje": f"Estado de la mascota actualizado a '{data['status']}' correctamente."}

# Endpoints: Gestión de Citas
@app.post("/citas/")
def crear_cita(cita: Cita):
    cita.id = len(citas) + 1
    citas.append(cita)
    return {"message": "Cita creada correctamente", "id": cita.id}

@app.put("/citas/{id}")
def actualizar_cita(id: int, cita: Cita):
    # Aquí buscarías la cita por id y la actualizarías
    cita_encontrada = next((c for c in citas if c.id == id), None)
    if cita_encontrada:
        cita_encontrada.animal = cita.animal
        cita_encontrada.dueno = cita.dueno
        cita_encontrada.tratamiento = cita.tratamiento
        cita_encontrada.fecha = cita.fecha
        return {"mensaje": "Cita actualizada correctamente."}
    else:
        raise HTTPException(status_code=404, detail="Cita no encontrada.")


@app.delete("/citas/{id}")
def eliminar_cita(id: int):
    # Aquí eliminarías la cita por id
    global citas
    citas = [cita for cita in citas if cita.id != id]
    return {"mensaje": "Cita eliminada correctamente."}

# Endpoints: Gestión de Facturas
@app.post("/facturas/")
def crear_factura(factura: Factura):
    facturas.append(factura)
    return {"message": "Factura creada correctamente"}

@app.get("/facturas/")
def listar_facturas():
    return facturas