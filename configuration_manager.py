import json
import os

class ConfigurationManager:
    _instance = None
    _config = {}
    _config_file = "config.json"

    def __new__(cls):
        """
        Sobrescribe new para que solo se cree una instancia.
        """
        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(cls)
            cls._instance._load_configuration()
        return cls._instance

    def _load_configuration(self):
        """
        Carga la configuración desde el archivo valores por defecto.
        """
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                print(f"Configuración cargada desde {self._config_file}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar la configuración desde {self._config_file}: {e}. Cargando valores por defecto.")
                self._load_default_configuration()
                self.save_configuration() # Guarda los valores por defecto
        else:
            print(f"El archivo {self._config_file} no existe. Cargando valores por defecto.")
            self._load_default_configuration()
            self.save_configuration() # Crea y guarda

    def _load_default_configuration(self):
        """
        Carga valores por defecto de configuración .
        """
        self._config = {
            "defaultCurrency": "CRC",
            "timeFormat": "24H",
            "maxConnections": 5,
            "language": "ES",
            "autoSaveInterval": 10,
            "enableLogs": True,
            "theme": "light",
            "region": "LATAM",
            "backupEnabled": True,
            "backupDirectory": "/tmp/backups"
        }

    def get_property(self, key):
        """
        Es para dar acceso.
        """
        return self._config.get(key)

    def set_property(self, key, value):
        """
        Para actualizar.
        """
        self._config[key] = value

    def save_configuration(self):
        """
        Guarda los cambios
        """
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
            print(f"Configuración guardada en {self._config_file}")
        except IOError as e:
            print(f"Error al guardar la configuración en {self._config_file}: {e}")

    def print_configuration(self):
        """
        enseña los valores de configuración .
        """
        print("\n--- Configuración Actual ---")
        for key, value in self._config.items():
            print(f"{key}: {value}")
        print("---------------------------\n")

