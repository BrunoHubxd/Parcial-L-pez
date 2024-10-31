import os

# Clase para representar un libro
class Libro:
    def __init__(self, titulo, autor, año, editorial, isbn, paginas):
        self.titulo = titulo
        self.autor = autor
        self.año = año
        self.editorial = editorial
        self.isbn = isbn
        self.paginas = paginas
        self.siguiente = None

# Clase para la pila de acciones
class PilaAcciones:
    def __init__(self):
        self.acciones = []

    def apilar(self, accion):
        self.acciones.append(accion)

    def desapilar(self):
        if self.acciones:
            return self.acciones.pop()
        else:
            return "La pila está vacía"

# Clase para gestionar la biblioteca
class Biblioteca:
    def __init__(self):
        self.cabeza = None
        self.pila_acciones = PilaAcciones()
        self.solicitudes = {}  # Diccionario para almacenar solicitudes de libros en préstamo

    def agregar_libro(self, titulo, autor, año, editorial, isbn, paginas):
        nuevo_libro = Libro(titulo, autor, año, editorial, isbn, paginas)
        nuevo_libro.siguiente = self.cabeza
        self.cabeza = nuevo_libro
        self.pila_acciones.apilar(f"Libro agregado: {titulo}")
        print(f"Libro agregado: {titulo}")

    def cargar_libros(self, nombre_archivo):
        if not os.path.exists(nombre_archivo):
            raise RuntimeError("No se pudo abrir el archivo")
        
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                datos = linea.strip().split(',')
                if len(datos) < 6:
                    continue

                titulo, autor, año, editorial, isbn, paginas = datos

                if "a.C." in año:
                    año = -int(año.replace(" a.C.", ""))  # Convertir a número negativo
                else:
                    año = int(año)

                self.agregar_libro(titulo, autor, año, editorial, isbn, int(paginas))

    def mostrar_libros(self):
        actual = self.cabeza
        while actual:
            print(f"Título: {actual.titulo}, Autor: {actual.autor}, Año: {actual.año}, "
                  f"Editorial: {actual.editorial}, ISBN: {actual.isbn}, Páginas: {actual.paginas}")
            actual = actual.siguiente

    def esta_disponible(self, titulo):
        """Verifica si un libro está disponible para préstamo."""
        actual = self.cabeza
        while actual:
            if actual.titulo == titulo and not any(titulo in libros for libros in self.solicitudes.values()):
                return True
            actual = actual.siguiente
        return False

    def solicitar_libro(self, nombre, dni, titulo_libro):
        if not self.esta_disponible(titulo_libro):
            raise RuntimeError("El libro solicitado no está disponible o ya fue prestado.")

        if (nombre, dni) not in self.solicitudes:
            self.solicitudes[(nombre, dni)] = []
        
        self.solicitudes[(nombre, dni)].append(titulo_libro)
        self.pila_acciones.apilar(f"Libro solicitado: {titulo_libro} por {nombre}, DNI: {dni}")
        print(f"Libro '{titulo_libro}' solicitado por {nombre}, DNI: {dni}")
        self.actualizar_archivo()  # Actualiza el archivo al solicitar el libro

    def devolver_libro(self, nombre, dni, titulo_libro):
        if (nombre, dni) in self.solicitudes and titulo_libro in self.solicitudes[(nombre, dni)]:
            self.solicitudes[(nombre, dni)].remove(titulo_libro)
            if not self.solicitudes[(nombre, dni)]:  # Eliminar entrada si ya no tiene libros prestados
                del self.solicitudes[(nombre, dni)]
            self.pila_acciones.apilar(f"Libro devuelto: {titulo_libro} por {nombre}, DNI: {dni}")
            print(f"Libro '{titulo_libro}' devuelto por {nombre}, DNI: {dni}.")
            self.agregar_libro_al_archivo(titulo_libro)  # Reagregar libro al archivo
        else:
            print(f"No hay registro de que {nombre} con DNI {dni} haya solicitado el libro '{titulo_libro}'.")

    def guardar_datos(self, nombre_archivo):
        actual = self.cabeza
        with open(nombre_archivo, 'w') as archivo:
            while actual:
                archivo.write(f"{actual.titulo},{actual.autor},{actual.año},{actual.editorial},{actual.isbn},{actual.paginas}\n")
                actual = actual.siguiente
        print("Datos guardados con éxito.")

    def actualizar_archivo(self):
        """Actualiza el archivo eliminando libros solicitados."""
        libros_disponibles = []
        actual = self.cabeza
        while actual:
            if actual.titulo not in [titulo for libros in self.solicitudes.values() for titulo in libros]:
                libros_disponibles.append(actual)
            actual = actual.siguiente
        
        with open("biblioteca.txt", 'w') as archivo:
            for libro in libros_disponibles:
                archivo.write(f"{libro.titulo},{libro.autor},{libro.año},{libro.editorial},{libro.isbn},{libro.paginas}\n")
        
        print("Archivo actualizado después de solicitar un libro.")

    def agregar_libro_al_archivo(self, titulo_libro):
        """Agrega un libro devuelto a la lista de libros disponibles en el archivo."""
        actual = self.cabeza
        while actual:
            if actual.titulo == titulo_libro:
                with open("biblioteca.txt", 'a') as archivo:
                    archivo.write(f"{actual.titulo},{actual.autor},{actual.año},{actual.editorial},{actual.isbn},{actual.paginas}\n")
                print(f"Libro '{titulo_libro}' agregado de nuevo al archivo.")
                break
            actual = actual.siguiente

# Función principal para ejecutar el sistema de gestión de biblioteca
def main():
    biblioteca = Biblioteca()

    # Cargar datos iniciales
    try:
        biblioteca.cargar_libros("biblioteca.txt")
    except RuntimeError as e:
        print(f"Error al cargar libros: {e}")

    # Interfaz de comandos simple
    while True:
        print("\nSistema de Gestión de Biblioteca")
        print("1. Mostrar todos los libros")
        print("2. Solicitar un libro")
        print("3. Devolver un libro")
        print("4. Guardar datos")
        print("5. Salir")
        opcion = input("Elige una opción: ")

        if opcion == '1':
            biblioteca.mostrar_libros()
        elif opcion == '2':
            nombre = input("Ingresa el nombre del lector: ")
            dni = input("Ingresa el DNI: ")
            titulo_libro = input("Ingresa el título del libro: ")

            try:
                biblioteca.solicitar_libro(nombre, dni, titulo_libro)
                print("Libro solicitado con éxito.")
            except RuntimeError as e:
                print(f"Error al solicitar el libro: {e}")
        elif opcion == '3':
            nombre = input("Ingresa el nombre del lector: ")
            dni = input("Ingresa el DNI: ")
            print("Libros solicitados:")
            if (nombre, dni) in biblioteca.solicitudes:
                for idx, titulo in enumerate(biblioteca.solicitudes[(nombre, dni)], start=1):
                    print(f"{idx}. {titulo}")
                titulo_libro = input("Ingresa el número del libro a devolver: ")
                try:
                    libro_a_devolver = biblioteca.solicitudes[(nombre, dni)][int(titulo_libro) - 1]
                    biblioteca.devolver_libro(nombre, dni, libro_a_devolver)
                except (IndexError, ValueError):
                    print("Número de libro inválido.")
            else:
                print("No tienes libros solicitados.")
        elif opcion == '4':
            try:
                biblioteca.guardar_datos("biblioteca.txt")
            except RuntimeError as e:
                print(f"Error al guardar datos: {e}")
        elif opcion == '5':
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
