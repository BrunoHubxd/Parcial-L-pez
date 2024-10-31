#include <iostream>
#include <fstream>
#include <string>
#include <stack>
#include <unordered_map>

using namespace std;

// Clase para representar un libro
class Libro {
public:
    string titulo;
    string autor;
    int anio;
    string editorial;
    string isbn;
    int paginas;
    Libro* siguiente;

    Libro(string titulo, string autor, int anio, string editorial, string isbn, int paginas)
        : titulo(titulo), autor(autor), anio(anio), editorial(editorial), isbn(isbn), paginas(paginas), siguiente(nullptr) {}
};

// Clase para la biblioteca
class Biblioteca {
private:
    Libro* cabeza;
    stack<string> pilaAcciones;
    unordered_map<string, unordered_map<string, bool>> solicitudes;

public:
    Biblioteca() : cabeza(nullptr) {}

    // Método para agregar un libro a la biblioteca
    void agregar_libro(const string& titulo, const string& autor, int anio, const string& editorial, const string& isbn, int paginas) {
        Libro* nuevoLibro = new Libro(titulo, autor, anio, editorial, isbn, paginas);
        nuevoLibro->siguiente = cabeza;
        cabeza = nuevoLibro;
        pilaAcciones.push("Libro agregado: " + titulo);
    }

    // Método para cargar libros desde un archivo
    void cargar_libros(const string& nombreArchivo) {
        ifstream archivo(nombreArchivo);
        if (!archivo.is_open()) {
            cerr << "No se pudo abrir el archivo." << endl;
            return;
        }

        string titulo, autor, editorial, isbn;
        int anio, paginas;
        while (getline(archivo, titulo, ',')) {
            getline(archivo, autor, ',');
            archivo >> anio;
            archivo.ignore();
            getline(archivo, editorial, ',');
            getline(archivo, isbn, ',');
            archivo >> paginas;
            archivo.ignore();
            agregar_libro(titulo, autor, anio, editorial, isbn, paginas);
        }
        archivo.close();
    }

    // Método para mostrar todos los libros
    void mostrar_libros() {
        Libro* actual = cabeza;
        int indice = 1;
        while (actual != nullptr) {
            cout << indice++ << ". " << actual->titulo << " de " << actual->autor << ", " << actual->anio << " (" << actual->editorial << "), ISBN: " << actual->isbn << ", " << actual->paginas << " páginas\n";
            actual = actual->siguiente;
        }
    }

    // Método para verificar si un libro está disponible
    bool esta_disponible(const string& titulo) {
        return solicitudes[titulo].empty();
    }

    // Método para solicitar un libro
    void solicitar_libro(const string& titulo, const string& lector, const string& dni) {
        if (esta_disponible(titulo)) {
            solicitudes[titulo][dni] = true;
            pilaAcciones.push("Libro solicitado: " + titulo + " por " + lector);
            cout << "El libro '" << titulo << "' ha sido solicitado por " << lector << ".\n";
        } else {
            cout << "El libro '" << titulo << "' no está disponible.\n";
        }
    }

    // Método para devolver un libro
    void devolver_libro(const string& titulo, const string& dni) {
        if (solicitudes[titulo].count(dni) > 0) {
            solicitudes[titulo].erase(dni);
            pilaAcciones.push("Libro devuelto: " + titulo);
            cout << "El libro '" << titulo << "' ha sido devuelto.\n";
        } else {
            cout << "No se encontro la solicitud del libro '" << titulo << "' para este usuario.\n";
        }
    }

    // Método para guardar el estado de la biblioteca en un archivo
    void guardar_datos(const string& nombreArchivo) {
        ofstream archivo(nombreArchivo);
        if (!archivo.is_open()) {
            cerr << "No se pudo abrir el archivo para guardar." << endl;
            return;
        }

        Libro* actual = cabeza;
        while (actual != nullptr) {
            archivo << actual->titulo << "," << actual->autor << "," << actual->anio << "," << actual->editorial << "," << actual->isbn << "," << actual->paginas << "\n";
            actual = actual->siguiente;
        }
        archivo.close();
    }

    // Método para limpiar la memoria de los libros
    ~Biblioteca() {
        while (cabeza != nullptr) {
            Libro* temp = cabeza;
            cabeza = cabeza->siguiente;
            delete temp;
        }
    }
};

// Función principal
int main() {
    Biblioteca biblioteca;
    biblioteca.cargar_libros("biblioteca.txt");

    int opcion;
    string titulo, autor, editorial, isbn, lector, dni;
    int anio, paginas;

    do {
        cout << "\nOpciones:\n";
        cout << "1. Mostrar todos los libros\n";
        cout << "2. Solicitar un libro\n";
        cout << "3. Devolver un libro\n";
        cout << "4. Guardar datos\n";
        cout << "5. Salir\n";
        cout << "Ingrese una opcion: ";
        cin >> opcion;
        cin.ignore();

        switch (opcion) {
            case 1:
                biblioteca.mostrar_libros();
                break;
            case 2:
                cout << "Ingrese el titulo del libro: ";
                getline(cin, titulo);
                cout << "Ingrese el nombre del lector: ";
                getline(cin, lector);
                cout << "Ingrese el DNI del lector: ";
                getline(cin, dni);
                biblioteca.solicitar_libro(titulo, lector, dni);
                break;
            case 3:
                cout << "Ingrese el titulo del libro: ";
                getline(cin, titulo);
                cout << "Ingrese el DNI del lector: ";
                getline(cin, dni);
                biblioteca.devolver_libro(titulo, dni);
                break;
            case 4:
                biblioteca.guardar_datos("biblioteca.txt");
                cout << "Datos guardados exitosamente.\n";
                break;
            case 5:
                cout << "Saliendo...\n";
                break;
            default:
                cout << "Opcion no válida.\n";
                break;
        }
    } while (opcion != 5);

    return 0;
}
