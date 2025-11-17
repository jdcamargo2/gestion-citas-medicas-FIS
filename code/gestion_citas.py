from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


# ===========================
#  MODELO DE DOMINIO (Model)
# ===========================


class EstadoCita(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


@dataclass
class Paciente:
    id_paciente: int
    nombre: str
    edad: int
    correo: str

    def registrar(self) -> None:
        print(f"[Paciente] Registrando paciente: {self.nombre} ({self.correo})")

    def agendar_cita(
        self, gestor: "GestorCitas", doctor: "Doctor", fecha: str, hora: str
    ) -> "Cita":
        print(f"[Paciente] {self.nombre} solicita agendar cita con {doctor.nombre}")
        return gestor.agendar_cita(self, doctor, fecha, hora)

    def cancelar_cita(self, gestor: "GestorCitas", cita: "Cita") -> None:
        print(f"[Paciente] {self.nombre} solicita cancelar la cita {cita.id_cita}")
        gestor.cancelar_cita(cita)


@dataclass
class Doctor:
    id_doctor: int
    nombre: str
    especialidad: str

    def confirmar_cita(self, cita: "Cita") -> None:
        print(f"[Doctor] {self.nombre} confirma la cita {cita.id_cita}")
        cita.cambiar_estado(EstadoCita.CONFIRMADA)


@dataclass
class Cita:
    id_cita: int
    paciente: Paciente
    doctor: Doctor
    fecha: str
    hora: str
    estado: EstadoCita = EstadoCita.PENDIENTE

    def agendar(self) -> None:
        print(
            f"[Cita] Agendando cita {self.id_cita} para "
            f"{self.paciente.nombre} con {self.doctor.nombre} "
            f"el {self.fecha} a las {self.hora}"
        )
        self.estado = EstadoCita.PENDIENTE

    def cancelar(self) -> None:
        print(f"[Cita] Cancelando cita {self.id_cita}")
        self.estado = EstadoCita.CANCELADA

    def cambiar_estado(self, nuevo_estado: EstadoCita) -> None:
        print(
            f"[Cita] Cambiando estado de {self.estado.value} "
            f"a {nuevo_estado.value} para cita {self.id_cita}"
        )
        self.estado = nuevo_estado


# ===========================
#  NOTIFICACION (Interface)
# ===========================


class Notificador:
    def enviar_correo(self, destinatario: str, mensaje: str) -> None:
        raise NotImplementedError


class NotificadorCorreo(Notificador):
    def __init__(
        self, servidor_smtp: str = "smtp.ejemplo.com", puerto: int = 587
    ) -> None:
        self.servidor_smtp = servidor_smtp
        self.puerto = puerto

    def enviar_correo(self, destinatario: str, mensaje: str) -> None:
        print(f"[NotificadorCorreo] Enviando correo a {destinatario}")
        print(f"[NotificadorCorreo] Contenido: {mensaje}\n")


# ===========================
#  CONTROLADOR (Controller)
# ===========================


class GestorCitas:
    def __init__(self, notificador: Notificador) -> None:
        self.notificador = notificador
        self._citas: List[Cita] = []
        self._contador_citas: int = 1

    def _generar_id_cita(self) -> int:
        nuevo_id = self._contador_citas
        self._contador_citas += 1
        return nuevo_id

    def agendar_cita(
        self, paciente: Paciente, doctor: Doctor, fecha: str, hora: str
    ) -> Cita:
        print("[GestorCitas] Recibida solicitud para agendar cita")

        id_cita = self._generar_id_cita()
        cita = Cita(
            id_cita=id_cita, paciente=paciente, doctor=doctor, fecha=fecha, hora=hora
        )

        cita.agendar()
        self._citas.append(cita)

        mensaje = (
            f"Estimado {paciente.nombre}, su cita con el Dr. {doctor.nombre} "
            f"ha sido agendada para el {fecha} a las {hora}. "
            f"ID de cita: {id_cita}."
        )
        self.notificador.enviar_correo(paciente.correo, mensaje)

        print("[GestorCitas] Cita agendada exitosamente\n")
        return cita

    def cancelar_cita(self, cita: Cita) -> None:
        print(f"[GestorCitas] Solicitud para cancelar cita {cita.id_cita}")
        cita.cancelar()

        mensaje = (
            f"Estimado {cita.paciente.nombre}, su cita con el Dr. {cita.doctor.nombre} "
            f"programada para el {cita.fecha} a las {cita.hora} ha sido CANCELADA."
        )
        self.notificador.enviar_correo(cita.paciente.correo, mensaje)

    def buscar_cita_por_id(self, id_cita: int) -> Optional[Cita]:
        for c in self._citas:
            if c.id_cita == id_cita:
                return c
        return None

    def listar_citas(self) -> List[Cita]:
        return list(self._citas)


# ===========================
#  VISTA / BOUNDARY (View)
# ===========================


class PantallaAgendarCita:
    def __init__(self, gestor: GestorCitas) -> None:
        self.gestor = gestor

    def solicitar_agendar_cita(
        self, paciente: Paciente, doctor: Doctor, fecha: str, hora: str
    ) -> Cita:
        print("[PantallaAgendarCita] El paciente solicita agendar una cita")
        print(
            f"[PantallaAgendarCita] Datos ingresados: doctor={doctor.nombre}, "
            f"fecha={fecha}, hora={hora}"
        )
        cita = self.gestor.agendar_cita(paciente, doctor, fecha, hora)
        self.mostrar_mensaje("Cita agendada con exito")
        return cita

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"[PantallaAgendarCita] {mensaje}\n")


# ===========================
#  MENU INTERACTIVO
# ===========================


def mostrar_menu() -> None:
    print("==========================================")
    print("   Sistema de Gestion de Citas Medicas   ")
    print("==========================================")
    print("1. Registrar paciente")
    print("2. Agendar cita")
    print("3. Cancelar cita")
    print("4. Listar citas")
    print("0. Salir")
    print("==========================================")


def registrar_paciente_interactivo() -> Paciente:
    print("\n--- Registro de paciente ---")
    nombre = input("Nombre del paciente: ").strip()
    edad_str = input("Edad: ").strip()
    correo = input("Correo: ").strip()

    try:
        edad = int(edad_str)
    except ValueError:
        print("Edad invalida, se usara 0.")
        edad = 0

    # Para este ejemplo, usamos siempre id_paciente = 1
    paciente = Paciente(
        id_paciente=1,
        nombre=nombre or "Paciente Sin Nombre",
        edad=edad,
        correo=correo or "sin.correo@example.com",
    )
    paciente.registrar()
    print()
    return paciente


def crear_doctor_por_defecto() -> Doctor:
    # En un caso real se registrarian varios doctores.
    # Aqui usamos uno fijo para simplificar.
    return Doctor(id_doctor=1, nombre="Doctor General", especialidad="Medicina General")


# ===========================
#  SCRIPT PRINCIPAL
# ===========================


def main() -> None:
    print("========== INICIO DEL PROGRAMA ==========\n")

    notificador = NotificadorCorreo()
    gestor = GestorCitas(notificador)

    doctor = crear_doctor_por_defecto()
    print(f"[Sistema] Doctor disponible: {doctor.nombre} ({doctor.especialidad})\n")

    paciente: Optional[Paciente] = None
    pantalla = PantallaAgendarCita(gestor)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            paciente = registrar_paciente_interactivo()

        elif opcion == "2":
            if paciente is None:
                print("Debe registrar primero un paciente (opcion 1).\n")
                continue

            print("\n--- Agendar cita ---")
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            hora = input("Hora (HH:MM): ").strip()

            pantalla.solicitar_agendar_cita(
                paciente=paciente,
                doctor=doctor,
                fecha=fecha or "2025-01-01",
                hora=hora or "09:00",
            )

        elif opcion == "3":
            if not gestor.listar_citas():
                print("No hay citas para cancelar.\n")
                continue

            print("\n--- Cancelar cita ---")
            try:
                id_cita = int(input("Ingrese el ID de la cita: ").strip())
            except ValueError:
                print("ID invalido.\n")
                continue

            cita = gestor.buscar_cita_por_id(id_cita)
            if cita is None:
                print(f"No se encontro la cita con ID {id_cita}.\n")
            else:
                if paciente is None:
                    # Por simplicidad, usamos el paciente asociado a la cita
                    paciente = cita.paciente
                paciente.cancelar_cita(gestor, cita)
                print()

        elif opcion == "4":
            print("\n--- Listado de citas ---")
            citas = gestor.listar_citas()
            if not citas:
                print("No hay citas registradas.\n")
            else:
                for c in citas:
                    print(
                        f"ID: {c.id_cita} | Paciente: {c.paciente.nombre} | "
                        f"Doctor: {c.doctor.nombre} | Fecha: {c.fecha} "
                        f"{c.hora} | Estado: {c.estado.value}"
                    )
                print()

        elif opcion == "0":
            print("\nSaliendo del sistema...")
            break

        else:
            print("Opcion no valida.\n")

    print("\n========== FIN DEL PROGRAMA ==========\n")


if __name__ == "__main__":
    main()
