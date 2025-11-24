# ⚓ PUERTO COSECHA

Plataforma web para conectar **productores agrícolas** con **empresas importadoras/exportadoras**, facilitando la creación de operaciones comerciales, gestión de documentos aduaneros y generación de reportes.

---

## 1. 🌟 Descripción del Proyecto

PUERTO COSECHA es una solución integral diseñada para optimizar y trazar el flujo de comercio de productos agrícolas.

### Funcionalidades Clave

* **Catálogo Público:** Visualización de productos agrícolas sin necesidad de autenticación.
* **Gestión de Productos:** Registro, edición y administración de productos por parte de los productores.
* **Gestión de Operaciones:** Creación, seguimiento y gestión de operaciones de importación/exportación.
* **Documentación Aduanera:** Subida y asociación de documentos (facturas, *packing lists*, certificados) a cada operación.
* **Normativa y Trazabilidad:** Asociación de **Incoterms** y normativas aplicables para una trazabilidad completa.

### Actores Principales

| Actor | Rol Principal |
| :--- | :--- |
| **Visitante** | Navega el catálogo de productos. |
| **Productor** | Registra y gestiona sus productos y el stock. |
| **Empresa** | Genera operaciones comerciales y sube documentos aduaneros. |
| **Administrador** | Supervisa y gestiona todas las entidades del sistema. |

---

## 2. ⚙️ Requisitos del Sistema

| Requisito | Versión |
| :--- | :--- |
| Python | 3.12+ |
| Django | 5.x |
| Base de Datos | PostgreSQL |
| Adaptador DB | `psycopg2-binary` |

> **Requisito Opcional:** Se recomienda usar un entorno virtual (`venv` o `conda`) para aislar las dependencias del proyecto.

---

## 3. 🚀 Instalación y Configuración

Sigue estos pasos para levantar el entorno de desarrollo:

1.  **Clonar el repositorio:**

    ```bash
    git clone <url_del_repositorio>
    cd Puerto-Cosecha
    ```

2.  **Crear y activar entorno virtual:**

    * **Linux / macOS:**
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```
    * **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Base de Datos:**

    * Configura tu base de datos **PostgreSQL**.
    * Edita el archivo `settings.py` de Django con las credenciales de tu DB.

5.  **Ejecutar Migraciones:**

    ```bash
    python manage.py migrate
    ```

6.  **Crear Superusuario (Administrador):**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Cargar datos de ejemplo (Opcional):**

    ```bash
    python manage.py loaddata fixtures_demo.json
    ```

8.  **Ejecutar Servidor:**

    ```bash
    python manage.py runserver
    ```

    Accede a la plataforma a través de `http://127.0.0.1:8000/`.

---

## 4. 🧩 Estructura de Módulos (Apps de Django)

| Módulo | Función Principal |
| :--- | :--- |
| `usuarios` | Gestión de perfiles, roles (productor, empresa, admin) y autenticación. |
| `productos` | Catálogo de productos agrícolas, registro y edición por productor. |
| `operaciones` | Creación y gestión del ciclo de vida de las operaciones comerciales y documentos aduaneros. |
| `reportes` | Vistas y lógica para la generación de reportes y analíticas. |

---

## 5. 🗺️ Uso Básico (Workflows)

### 5.1. Flujo del Productor

1.  **Registro y Perfil:** Se registra con el rol `productor`.
2.  **Creación de Productos:** Carga nuevos productos especificando:
    * Nombre, Descripción, Precio, Stock.
    * País de Origen, Unidad de Medida.
    * Categoría y normativa (Incoterms, etc.).
3.  **Monitoreo:** Visualiza sus productos y las operaciones generadas sobre ellos.

### 5.2. Flujo de la Empresa

1.  **Registro y Perfil:** Se registra con el rol `empresa`.
2.  **Búsqueda:** Navega el catálogo público de productos.
3.  **Creación de Operación:** Genera una nueva operación comercial sobre un producto seleccionado.
4.  **Seguimiento y Documentación:**
    * Cambia el estado de la operación:
        > `pendiente` → `en_proceso` → `en_transito` → `finalizado/cancelado`
    * Sube los documentos aduaneros asociados (Factura, *Packing List*, Certificado de Origen).

---

## 6. 📊 Reportes Disponibles

El módulo `reportes` ofrece diversas vistas para la analítica del negocio:

| Tipo de Reporte | Descripción | Filtros Disponibles |
| :--- | :--- | :--- |
| **Por Estado** | Conteo de operaciones según su estado actual. | Estados |
| **Por País** | Conteo de operaciones según el país de destino. | Paises |
| **Por Producto** | Filtrado de operaciones para obtener la cantidad total negociada por producto. | Productos |
| **Reporte Completo** | Vista detallada con todos los datos de la operación. | Producto, Estado, País |

### Datos del Reporte Completo

* ID de operación
* Empresa y Productor involucrados
* Producto y cantidad
* Precio unitario y total
* Estado de la operación
* País de destino
* Fecha de creación
* Documentos asociados (enlace o listado)

---

## 7. 📁 Fixtures (Datos de Ejemplo)

Para una prueba rápida del sistema, se utiliza el archivo `fixtures_demo.json`.

> **Para cargar:** `python manage.py loaddata fixtures_demo.json`

### Estructura Mínima de Ejemplo

```json
[
    {
        "model": "usuarios.usuario",
        "pk": 1,
        "fields": {
            "username": "productor_demo",
            "rol": "productor",
            "password": "pbkdf2_sha256$..." // Hash de una contraseña segura (e.g., "12345678")
        }
    },
    {
        "model": "productos.producto",
        "pk": 1,
        "fields": {
            "productor": 1,
            "nombre": "Tomate",
            "descripcion": "Tomate rojo fresco de la mejor calidad.",
            "precio_unitario": "1.50",
            "stock": 100,
            "pais_origen": "Perú",
            "unidad": "kg",
            "categoria": "Hortalizas"
        }
    }
]