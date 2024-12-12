from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
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
    owner_dni: str
    pet_name: str
    treatment: str
    start_time: datetime
    end_time: datetime
    status: str = "Pendiente"

class Factura(BaseModel):
    id: int
    cita_id: int
    treatments: List[str]
    total_cost: float
    payment_method: str
    is_paid: bool
    issue_date: datetime = datetime.now()

# Base de datos en memoria
duenos_db: List[Dueno] = []
mascotas_db: List[Mascota] = []
citas_db: List[Cita] = []
facturas_db: List[Factura] = []

# Endpoints
@app.post("/registrar-dueño/")
def registrar_dueno(dueno: Dueno):
    for d in duenos_db:
        if d.dni == dueno.dni:
            raise HTTPException(status_code=400, detail="El DNI ya está registrado.")
    duenos_db.append(dueno)
    return {"mensaje": "Dueño registrado con éxito."}

# Endpoints de gestión
@app.post("/registrar-dueño/")
def registrar_dueno(dueno: Dueno):
    if any(d.dni == dueno.dni for d in duenos_db):
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

# Endpoints de Gestión de Citas

@app.post("/crear-cita/")
def crear_cita(cita: Cita):
    if cita.end_time <= cita.start_time:
        raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la de inicio.")
    if not any(m.owner_dni == cita.owner_dni and m.pet_name.lower() == cita.pet_name.lower() for m in mascotas_db):
        raise HTTPException(status_code=404, detail="Mascota no encontrada o no pertenece al dueño.")
    if any((c.start_time <= cita.start_time < c.end_time or c.start_time < cita.end_time <= c.end_time) for c in citas_db):
        raise HTTPException(status_code=400, detail="Ya existe una cita en el mismo horario.")
    citas_db.append(cita)
    return {"mensaje": "Cita creada exitosamente.", "cita": cita}

@app.post("/finalizar-cita/{cita_id}")
def finalizar_cita(cita_id: int, treatments: List[str], total_cost: float, payment_method: str):
    cita = next((c for c in citas_db if c.id == cita_id), None)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada.")
    cita.status = "Finalizada"
    factura = Factura(
        id=len(facturas_db) + 1,
        cita_id=cita.id,
        treatments=treatments,
        total_cost=total_cost,
        payment_method=payment_method,
        is_paid=False
    )
    facturas_db.append(factura)
    return {"mensaje": "Cita finalizada y factura generada.", "factura": factura}

@app.put("/pagar-factura/{factura_id}")
def pagar_factura(factura_id: int):
    factura = next((f for f in facturas_db if f.id == factura_id), None)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada.")
    factura.is_paid = True
    return {"mensaje": "Factura marcada como pagada."}

@app.put("/modificar-cita/{cita_id}")
def modificar_cita(cita_id: int, nueva_fecha: dict):
    cita = next((c for c in citas_db if c.id == cita_id), None)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada.")
    cita.start_time = nueva_fecha["nueva_fecha"]
    return cita

@app.delete("/cancelar-cita/{cita_id}")
def cancelar_cita(cita_id: int):
    global citas_db
    cita = next((c for c in citas_db if c.id == cita_id), None)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada.")
    citas_db = [c for c in citas_db if c.id != cita_id]
    return {"mensaje": "Cita cancelada correctamente."}
