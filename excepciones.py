class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores de Software FJ."""
    pass

class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un parámetro está vacío, es negativo o tiene formato incorrecto."""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio ocupado o inactivo."""
    pass

class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar confirmar/cancelar una reserva en un estado inválido."""
    pass