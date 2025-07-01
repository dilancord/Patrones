import datetime
import locale # Para el formato AM/PM

class WelcomeScreen:
    def __init__(self):
        from configuration_manager import ConfigurationManager
        self.config_manager = ConfigurationManager()

    def display(self):
        language = self.config_manager.get_property("language")
        time_format = self.config_manager.get_property("timeFormat")
        theme = self.config_manager.get_property("theme")

        welcome_message = ""
        if language and language.upper() == "ES":
            welcome_message = "¡Bienvenido a la aplicación de configuración!"
        elif language and language.upper() == "EN":
            welcome_message = "Welcome to the configuration application!"
        else:
            welcome_message = "Welcome!" # Default

        now = datetime.datetime.now()
        formatted_time = ""

        if time_format and time_format.upper() == "24H":
            formatted_time = now.strftime("%H:%M:%S")
        else:
            try:
                locale.setlocale(locale.LC_TIME, 'en_US.UTF-8') # O 'es_ES.UTF-8' si prefieres AM/PM en español
            except locale.Error:
                pass
            formatted_time = now.strftime("%I:%M:%S %p") # %I para 12 horas, %p para AM/PM

        print("\n--- Panel de Bienvenida ---")
        print(f"Idioma: {language}")
        print(f"Formato de Hora: {time_format}")
        print(f"Tema: {theme}")
        print("---------------------------\n")

        reset_color = "\033[0m" # resetear color

        if theme and theme.lower() == "dark":
            text_color = "\033[97m"
            background_color = "\033[40m" # Fondo negro
        else:
            text_color = "\033[30m" # Negro
            background_color = "\033[47m" # Fondo blanco

        print(f"{background_color}{text_color}{welcome_message}")
        print(f"{text_color}La hora actual es: {formatted_time}{reset_color}")
        print("---------------------------\n")