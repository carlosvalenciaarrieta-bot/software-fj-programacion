from datetime import datetime

class LoggerSistema:
    def __init__(self, archivo="sistema_fj.log"):
        self.archivo = archivo

    def registrar(self, nivel: str, mensaje: str):
        f = None
        try:
            f = open(self.archivo, "a", encoding="utf-8")
            marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n")
        except IOError as e:
            print(f"Error crítico escribiendo en el log: {e}")
        finally:
            if f:
                f.close()