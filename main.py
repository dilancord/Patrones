from configuration_manager import ConfigurationManager
from welcome_screen import WelcomeScreen
from connection_simulator import ConnectionSimulator
import os

def clear_console():
    """Limpia la consola """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Tira el menú principal en la consola"""
    print("\n--- Menú Principal ---")
    print("1. Ver configuración actual")
    print("2. Cambiar configuración")
    print("3. Ir al panel de bienvenida")
    print("4. Ejecutar el simulador de conexiones")
    print("5. Salir del sistema")
    print("----------------------")

def change_configuration(config_manager):
    """
    Permite cambiar algo de la configuración.
    """
    print("\n--- Cambiar Configuración ---")
    print("Parámetros disponibles para cambiar:")
    current_config_keys = config_manager._config.keys()
    for key in sorted(current_config_keys):
        print(f"- {key}")

    print("\nIngrese el nombre del parámetro a cambiar (o 'cancelar' para salir): ")
    key = input().strip()

    if key.lower() == "cancelar":
        print("Cambio de configuración cancelado.")
        return

    if key not in current_config_keys:
        print(f"Error: El parámetro '{key}' no existe en la configuración.")
        return

    print(f"Ingrese el nuevo valor para '{key}': ")
    value = input().strip()

    original_value = config_manager.get_property(key)
    converted_value = value

    if isinstance(original_value, bool):
        if value.lower() == 'true':
            converted_value = True
        elif value.lower() == 'false':
            converted_value = False
        else:
            print(f"Error: Valor inválido para '{key}'. Use 'true' o 'false'.")
            return
    elif isinstance(original_value, int):
        try:
            converted_value = int(value)
        except ValueError:
            print(f"Error: Valor inválido para '{key}'. Debe ser un número entero.")
            return
    elif isinstance(original_value, float):
        try:
            converted_value = float(value)
        except ValueError:
            print(f"Error: Valor inválido para '{key}'. Debe ser un número decimal.")
            return

    # Validaciones específicas por nombre de parámetro si se necesita más control
    if key == "timeFormat" and converted_value not in ["24H", "AM/PM"]:
        print("Error: Valor inválido para 'timeFormat'. Use '24H' o 'AM/PM'.")
        return
    elif key == "theme" and converted_value not in ["light", "dark"]:
        print("Error: Valor inválido para 'theme'. Use 'light' o 'dark'.")
        return
    elif key == "maxConnections" and converted_value <= 0:
        print("Error: El número de conexiones debe ser positivo.")
        return

    config_manager.set_property(key, converted_value)
    config_manager.save_configuration()
    print(f"Parámetro '{key}' actualizado a '{converted_value}' y guardado.")

def main():
    config_manager = ConfigurationManager()
    welcome_screen = WelcomeScreen()
    connection_simulator = ConnectionSimulator()

    while True:
        clear_console()
        print_menu()
        try:
            option = int(input("Seleccione una opción: "))
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")
            input("Presione Enter para continuar...")
            continue

        if option == 1:
            config_manager.print_configuration()
        elif option == 2:
            change_configuration(config_manager)
        elif option == 3:
            welcome_screen.display()
        elif option == 4:
            connection_simulator.simulate()
        elif option == 5:
            print("Saliendo del sistema. ¡Adiós!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

        input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()