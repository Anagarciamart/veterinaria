import json
import re


class Dueño:
    def __init__(self, nombre, dni, direccion, telefono, correo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.mascotas = []

    def agregar_mascota(self, mascota):
        self.mascotas.append(mascota)

    def eliminar_mascota(self, nombre_mascota):
        for mascota in self.mascotas:
            if mascota.nombre == nombre_mascota:
                self.mascotas.remove(mascota)
                return True
        return False


class Mascota:
    def __init__(self, nombre, especie, raza, fecha_nacimiento, patologias, dueño):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.fecha_nacimiento = fecha_nacimiento
        self.patologias = patologias
        self.dueño = dueño
        self.historia_clinica = []
        self.estado = 'vivo'

    def agregar_tratamiento(self, tratamiento):
        self.historia_clinica.append(tratamiento)


class ClinicaVeterinaria:
    def __init__(self):
        self.dueños = []

    def validar_dni(self, dni):
        return re.fullmatch(r'\d{8}[A-Za-z]', dni) is not None

    def validar_telefono(self, telefono):
        return telefono.isdigit() and 9 <= len(telefono) <= 15

    def validar_correo(self, correo):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", correo) is not None

    def buscar_dueño(self, dni=None, telefono=None):
        for dueño in self.dueños:
            if (dni and dueño.dni == dni) or (telefono and dueño.telefono == telefono):
                return dueño
        return None

    def agregar_dueño(self):
        nombre = input("Ingrese el nombre del dueño: ")

        while True:
            dni = input("Ingrese el DNI del dueño (8 dígitos y una letra): ")
            if self.validar_dni(dni):
                break
            else:
                print("DNI inválido. Debe contener 8 dígitos seguidos de una letra.")

        direccion = input("Ingrese la dirección del dueño: ")

        while True:
            telefono = input("Ingrese el teléfono del dueño: ")
            if self.validar_telefono(telefono):
                break
            else:
                print("Teléfono inválido. Debe contener solo números y tener entre 9 y 15 dígitos.")

        while True:
            correo = input("Ingrese el correo del dueño: ")
            if self.validar_correo(correo):
                break
            else:
                print("Correo inválido. Ingrese un correo con formato válido (ejemplo@dominio.com).")

        nuevo_dueño = Dueño(nombre, dni, direccion, telefono, correo)
        self.dueños.append(nuevo_dueño)
        print("Dueño agregado con éxito.")
        return nuevo_dueño

    def agregar_mascota(self):
        dueño = None
        dni_o_telefono = input("Ingrese DNI o teléfono del dueño (o presione Enter para registrar uno nuevo): ")

        if dni_o_telefono:
            dueño = self.buscar_dueño(dni_o_telefono)
            if not dueño:
                print("Dueño no encontrado.")
                return
        else:
            dueño = self.agregar_dueño()

        nombre = input("Ingrese el nombre de la mascota: ")
        especie = input("Ingrese la especie de la mascota: ")
        raza = input("Ingrese la raza de la mascota: ")

        while True:
            fecha_nacimiento = input("Ingrese la fecha de nacimiento de la mascota (AAAA-MM-DD): ")
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha_nacimiento):
                break
            else:
                print("Fecha de nacimiento inválida. Use el formato AAAA-MM-DD.")

        patologias = input("Ingrese patologías previas (si conocidas): ")

        mascota = Mascota(nombre, especie, raza, fecha_nacimiento, patologias, dueño)
        dueño.agregar_mascota(mascota)
        print("Mascota agregada con éxito.")

    def eliminar_dueño(self):
        dni = input("Ingrese el DNI del dueño que desea eliminar: ")
        dueño = self.buscar_dueño(dni=dni)
        if dueño:
            confirmacion = input(
                f"¿Está seguro que desea eliminar al dueño {dueño.nombre} y todas sus mascotas? (s/n): ")
            if confirmacion.lower() == 's':
                self.dueños.remove(dueño)
                print("Dueño eliminado con éxito.")
            else:
                print("Eliminación cancelada.")
        else:
            print("Dueño no encontrado.")

    def eliminar_mascota(self):
        dni = input("Ingrese el DNI del dueño de la mascota a eliminar: ")
        dueño = self.buscar_dueño(dni=dni)
        if dueño:
            nombre_mascota = input("Ingrese el nombre de la mascota que desea eliminar: ")
            if dueño.eliminar_mascota(nombre_mascota):
                print("Mascota eliminada con éxito.")
            else:
                print("Mascota no encontrada.")
        else:
            print("Dueño no encontrado.")

    def mostrar_mascotas(self):
        for dueño in self.dueños:
            print(f"Dueño: {dueño.nombre}, DNI: {dueño.dni}")
            for mascota in dueño.mascotas:
                print(" - Nombre:", mascota.nombre)
                print("   Especie:", mascota.especie)
                print("   Raza:", mascota.raza)
                print("   Fecha de Nacimiento:", mascota.fecha_nacimiento)
                print("   Estado:", mascota.estado)
                print("   Historia Clínica:", mascota.historia_clinica)
                print("")


def menu():
    print("------ Menú ------")
    print("1. Agregar dueño")
    print("2. Agregar mascota")
    print("3. Mostrar mascotas")
    print("4. Eliminar dueño")
    print("5. Eliminar mascota")
    print("6. Salir")


clinica = ClinicaVeterinaria()

while True:
    menu()
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        clinica.agregar_dueño()
    elif opcion == '2':
        clinica.agregar_mascota()
    elif opcion == '3':
        clinica.mostrar_mascotas()
    elif opcion == '4':
        clinica.eliminar_dueño()
    elif opcion == '5':
        clinica.eliminar_mascota()
    elif opcion == '6':
        print("Saliendo del programa...")
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")



