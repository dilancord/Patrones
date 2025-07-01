import random
import time

class ConnectionSimulator:
    def __init__(self):
        from configuration_manager import ConfigurationManager
        self.config_manager = ConfigurationManager()

    def simulate(self):
        max_connections = self.config_manager.get_property("maxConnections")
        enable_logs = self.config_manager.get_property("enableLogs")
        default_currency = self.config_manager.get_property("defaultCurrency")

        # para que las connections sea un entero
        try:
            max_connections = int(max_connections)
        except (ValueError, TypeError):
            print("Error: 'maxConnections' no es un número válido. Usando 5 por defecto.")
            max_connections = 5

        # para que enable_logs sea un booleano
        enable_logs = str(enable_logs).lower() == 'true'

        print("\n--- Simulador de Conexiones ---")
        print(f"Máximo de Conexiones: {max_connections}")
        print(f"Logs Habilitados: {enable_logs}")
        print(f"Moneda por Defecto: {default_currency}")
        print("-------------------------------\n")

        for i in range(1, max_connections + 1):
            success = random.choice([True, False]) # Simula éxito o fracaso
            if success:
                if enable_logs:
                    print(f"Log: Conexión {i} establecida con éxito.")
            else:
                if enable_logs:
                    print(f"Log: Fallo al establecer la conexión {i}.")
            time.sleep(0.2) # Simula el tiempo de conexión

        print("\nResumen de Conexiones:")
        print(f"Se intentaron {max_connections} conexiones.")
        print(f"Los valores de configuración se manejan en {default_currency}.")
        print("-------------------------------\n")