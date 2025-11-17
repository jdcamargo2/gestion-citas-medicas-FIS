# Sistema de Gestión de Citas Médicas – Tarea Semana 07

Este repositorio contiene la implementación de la **Tarea Semana 07: Casos de uso, clases, relaciones y secuencia** del curso de Fundamentos de Ingeniería de Software.

El sistema modela la **Gestión de Citas Médicas** para una clínica, a partir de los requisitos planteados por el docente:

- Pacientes que se registran en el sistema.
- Doctores asociados a una especialidad.
- Citas con fecha, hora y estado (PENDIENTE, CONFIRMADA, CANCELADA).
- Envío de notificaciones de confirmación/cancelación por correo (simulado).

---

## Objetivo de la actividad

- Identificar los **escenarios**, clases, atributos, métodos y relaciones a partir de una descripción de problema.
- Elaborar:
  - **Diagramas de casos de uso** (general y específicos).
  - **Diagrama de clases UML** con una interface.
  - **Diagrama de secuencia** basado en un escenario del caso de uso.
- Llevar el diseño a **programación**, implementando el modelo de clases y el flujo del diagrama de secuencia.

---

## Tecnologías y enfoque

- **Lenguaje:** Python 3.x  
- **Tipo de aplicación:** Cliente enriquecido sencillo de consola  
- **Arquitectura utilizada:** Inspirada en el patrón **MVC**:
  - **Modelo (Model):**
    - `Paciente`
    - `Doctor`
    - `Cita`
    - `EstadoCita` (Enum)
  - **Controlador (Controller):**
    - `GestorCitas` – coordina la lógica para agendar, cancelar y listar citas.
  - **Vista / Boundary (View):**
    - `PantallaAgendarCita` – muestra mensajes y simula una pantalla de agendamiento.
    - Menú interactivo por consola para el usuario.
  - **Notificación (Interface):**
    - `Notificador` (interface)
    - `NotificadorCorreo` (implementación concreta que simula el envío de correos).

---

## Relación con los diagramas UML

El código implementa el diseño realizado en Enterprise Architect:

- **Casos de uso:**
  - General del sistema de Gestión de Citas Médicas.
  - Específicos:
    - Registrar Paciente
    - Agendar Cita
    - Cancelar Cita
- **Diagrama de clases:**
  - Clases `Paciente`, `Doctor`, `Cita`, `Notificador`, `NotificadorCorreo`.
  - Relaciones:
    - Un `Paciente` puede tener muchas `Cita`.
    - Un `Doctor` puede tener muchas `Cita`.
    - `NotificadorCorreo` implementa la interface `Notificador`.
- **Diagrama de secuencia (Agendar Cita):**
  - Actor: `Paciente`
  - Objetos: `PantallaAgendarCita`, `GestorCitas`, `Cita`, `NotificadorCorreo`
  - El flujo de mensajes del diagrama se refleja en las llamadas del código:
    - Solicitud de agendar
    - Creación de la cita
    - Cambio de estado
    - Envío de la notificación
    - Confirmación al usuario

---

## Estructura del archivo principal

El proyecto se concentra en un solo archivo:

- `gestion_citas.py`

Dentro de este archivo se definen todas las clases (modelo, controlador, vista y notificador) y el **menú interactivo**.

---

## Cómo ejecutar el programa

1. Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/gestion-citas-medicas-semana07.git
cd gestion-citas-medicas-semana07
