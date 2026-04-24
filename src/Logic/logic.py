class ApartadoLogic:
    """Clase encargada de todos los cálculos y reglas de negocio de los apartados."""
    
    @staticmethod
    def calcular_anticipo_minimo(total_texto: str) -> float:
        """Calcula el 20% obligatorio basado en el total del carrito."""
        try:
            # Limpiamos el texto "$150.00" -> 150.0
            total = float(total_texto.replace("$", "").replace(",", ""))
            return round(total * 0.20, 2)
        except ValueError:
            return 0.0

    @staticmethod
    def calcular_monto_restante(total_texto: str, anticipo_texto: str) -> float:
        """Calcula cuánto queda por pagar."""
        try:
            total = float(total_texto.replace("$", "").replace(",", ""))
            # Si el anticipo está vacío o no es número, asumimos 0
            anticipo = float(anticipo_texto) if anticipo_texto else 0.0
            return round(max(0, total - anticipo), 2)
        except ValueError:
            return 0.0
        
    
class VentaLogic:
    @staticmethod
    def preparar_detalle_venta(carrito: dict) -> list:
        """Convierte el diccionario del carrito al formato JSON que espera el SP."""
        # Formato esperado por el SP: [{"productos_id": id, "cantidad": cant}, ...]
        detalle = []
        for nombre, info in carrito.items():
            detalle.append({
                "productos_id": info["id"],
                "cantidad": info["cantidad"]
            })
        return detalle

    @staticmethod
    def limpiar_monto(monto_texto: str) -> float:
        """Limpia el texto de moneda ($15.00 -> 15.0)."""
        return float(monto_texto.replace("$", "").replace(",", ""))