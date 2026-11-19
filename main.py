# main.py
from modelos import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada, Reserva
from excepciones import ErrorSistemaFJ
from logger import LoggerSistema

def ejecutar_simulacion():
    log = LoggerSistema()
    clientes = []
    servicios = []
    reservas = []

    print("=== INICIANDO SISTEMA INTEGRAL SOFTWARE FJ ===\n")

    # Operación 1: Registro válido de cliente
    try:
        c1 = Cliente("C01", "Laura Gómez", "laura@correo.com")
        clientes.append(c1)
        log.registrar("INFO", f"Cliente registrado: {c1.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 1 fallida: {e}")

    # Operación 2: Registro inválido de cliente (correo malo)
    try:
        c_bad = Cliente("C02", "Carlos Ruiz", "carloscorreo.com")
        clientes.append(c_bad)
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 2 (Cliente inválido) controlada: {e}")
        print(f"[Controlado] Error en Op 2: {e}")

    # Operación 3: Creación válida de Sala
    try:
        s1 = ReservaSala("S01", "Sala Juntas Norte", 50000, 10)
        servicios.append(s1)
        log.registrar("INFO", f"Servicio creado: {s1.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 3 fallida: {e}")

    # Operación 4: Creación válida de Equipo
    try:
        s2 = AlquilerEquipo("E01", "MacBook Pro M3", 35000, "Alta")
        servicios.append(s2)
        log.registrar("INFO", f"Servicio creado: {s2.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 4 fallida: {e}")

    # Operación 5: Creación inválida de Servicio (tarifa negativa)
    try:
        s_bad = AsesoriaEspecializada("A99", "Arquitectura Cloud", -10000, "DevOps")
        servicios.append(s_bad)
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 5 (Servicio inválido) controlada: {e}")
        print(f"[Controlado] Error en Op 5: {e}")

    # Operación 6: Creación válida de Asesoría
    try:
        s3 = AsesoriaEspecializada("A01", "Seguridad Informática", 80000, "Ciberseguridad")
        servicios.append(s3)
        log.registrar("INFO", f"Servicio creado: {s3.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 6 fallida: {e}")

    # Operación 7: Reserva exitosa con descuento (uso de try/except/else)
    try:
        r1 = Reserva("R01", clientes[0], servicios[0], 4)
        r1.procesar_y_confirmar(descuento=0.10)
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 7 fallida: {e}")
    else:
        reservas.append(r1)
        log.registrar("INFO", f"Reserva confirmada: {r1.obtener_resumen()}")
        print(f"[Éxito] {r1.obtener_resumen()}")

    # Operación 8: Intento de reservar un servicio ya ocupado
    try:
        r2 = Reserva("R02", clientes[0], servicios[0], 2)
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 8 (Servicio ocupado) controlada: {e}")
        print(f"[Controlado] Error en Op 8: {e}")

    # Operación 9: Reserva fallida por horas inválidas (prueba encadenamiento)
    try:
        r3 = Reserva("R03", clientes[0], servicios[1], 1) # Equipo exige mínimo 2 horas
        r3.procesar_y_confirmar()
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 9 (Encadenamiento) controlada: {e} | Causa: {e.__cause__}")
        print(f"[Controlado] Error en Op 9: {e} -> Causa original: {e.__cause__}")

    # Operación 10: Cancelación exitosa y liberación de servicio
    try:
        reservas[0].cancelar()
        log.registrar("INFO", f"Reserva cancelada: {reservas[0].id}")
        print(f"[Éxito] Reserva {reservas[0].id} cancelada. Sala disponible nuevamente.")
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 10 fallida: {e}")

    # Operación 11: Intento de cancelar una reserva ya cancelada
    try:
        reservas[0].cancelar()
    except ErrorSistemaFJ as e:
        log.registrar("ERROR", f"Op 11 (Doble cancelación) controlada: {e}")
        print(f"[Controlado] Error en Op 11: {e}")

    print("\n=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES (Revisa sistema_fj.log) ===")

if __name__ == "__main__":
    ejecutar_simulacion()