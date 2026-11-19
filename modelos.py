from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError, ServicioNoDisponibleError, OperacionNoPermitidaError

# 1. Clase abstracta general del sistema
class EntidadSistema(ABC):
    def __init__(self, id_entidad: str):
        if not id_entidad or not id_entidad.strip():
            raise DatoInvalidoError("El ID de la entidad no puede estar vacío.")
        self._id = id_entidad.strip()

    @property
    def id(self):
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        pass

# 2. Clase Cliente con encapsulación y validaciones
class Cliente(EntidadSistema):
    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise DatoInvalidoError(f"Correo electrónico inválido: {valor}")
        self._correo = valor.strip()

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id}]: {self.nombre} ({self.correo})"

# 3. Clase abstracta Servicio
class Servicio(EntidadSistema):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float):
        super().__init__(id_servicio)
        if tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor a cero.")
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self.disponible = True

    @abstractmethod
    def validar_parametros(self, horas: int):
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    # Método con sobrecarga simulada (parámetros opcionales para impuestos y descuentos)
    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self.validar_parametros(horas)
        if not (0 <= descuento < 1):
            raise DatoInvalidoError("El descuento debe estar entre 0 y 0.99 (0% a 99%).")
        
        subtotal = self._tarifa_base * horas
        con_descuento = subtotal * (1 - descuento)
        total = con_descuento * (1 + impuesto)
        return round(total, 2)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"{self.describir_servicio()} - Estado: {estado}"

# 3.1 Servicio Especializado: Sala
class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser positiva.")
        self.capacidad = capacidad

    def validar_parametros(self, horas: int):
        if horas < 1 or horas > 12:
            raise DatoInvalidoError("Las salas se reservan entre 1 y 12 horas.")

    def describir_servicio(self) -> str:
        return f"Sala '{self._nombre}' (Capacidad: {self.capacidad} personas)"

# 3.2 Servicio Especializado: Alquiler de Equipos
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, gama: str):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not gama:
            raise DatoInvalidoError("Debe especificar la gama del equipo.")
        self.gama = gama

    def validar_parametros(self, horas: int):
        if horas < 2:
            raise DatoInvalidoError("El alquiler de equipos requiere mínimo 2 horas.")

    def describir_servicio(self) -> str:
        return f"Equipo '{self._nombre}' (Gama: {self.gama})"

# 3.3 Servicio Especializado: Asesoría Especializada
class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str):
        super().__init__(id_servicio, nombre, tarifa_hora)
        self.especialidad = especialidad

    def validar_parametros(self, horas: int):
        if horas <= 0:
            raise DatoInvalidoError("La duración de la asesoría debe ser mayor a 0 horas.")

    def describir_servicio(self) -> str:
        return f"Asesoría '{self._nombre}' (Área: {self.especialidad})"

# 4. Clase Reserva
class Reserva(EntidadSistema):
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int):
        super().__init__(id_reserva)
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio {servicio.id} no está disponible.")
        
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def procesar_y_confirmar(self, descuento: float = 0.0):
        try:
            if self.estado != "PENDIENTE":
                raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado {self.estado}.")
            # Encadenamiento de excepciones si falla el cálculo
            self.costo_total = self.servicio.calcular_costo(self.horas, descuento=descuento)
        except DatoInvalidoError as e:
            raise OperacionNoPermitidaError("Fallo al procesar los costos de la reserva.") from e
        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")
        self.estado = "CANCELADA"
        self.servicio.disponible = True

    def obtener_resumen(self) -> str:
        return f"Reserva [{self.id}] | {self.cliente.nombre} | {self.servicio.describir_servicio()} | Estado: {self.estado} | Total: ${self.costo_total}"