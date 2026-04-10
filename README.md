# prueba-tecnica-taller-rapido-juarez

Un sistema de gestion integral (MVP) desarrollado en Django para la administracion de tickets de servicio, control de inventario y analisis de metricas de un taller mecanico.

Este proyecto fue diseñado con una filosofia Mobile-First y arquitectura PWA (Progressive Web App), priorizando la agilidad de uso en el entorno real del taller y manteniendo un codigo bloat-free (libre de dependencias pesadas innecesarias).

---

## Contexto: El Por Que y Donde se hizo

Este proyecto nace como una prueba tecnica / MVP para resolver la digitalizacion de un entorno de trabajo rapido. En un taller, los mecanicos operan con tiempos ajustados, a menudo usando el celular con una sola mano y con conectividad intermitente.

El objetivo principal fue construir una herramienta que sea robusta en el backend (Django) pero que se sienta como una aplicacion nativa, rapida y tactil en el frontend, sin requerir hardware costoso ni curvas de aprendizaje largas.

---

## Desafios y Soluciones Implementadas

### 1. Usabilidad en el Entorno de Trabajo (UX)
Desafio: Las tablas de datos estandar y las barras de navegacion colapsables son dificiles de operar en pantallas chicas o con prisas.
Solucion: Implementacion de un diseño hibrido. En resoluciones de escritorio, el sistema muestra vistas gerenciales detalladas (tablas clasicas). En moviles, la interfaz muta automaticamente a Tarjetas Touch-Friendly y un Menu Inferior (Launchpad) basado en Memory Muscle UX, garantizando objetivos de pulsacion amplios y comodos.

### 2. Rendimiento y Busquedas en Inventario
Desafio: Un taller real maneja cientos de repuestos. Hacer consultas al servidor (backend) por cada letra que el usuario tipea en el buscador generaria cuellos de botella y demoras.
Solucion: Desarrollo de un motor de busqueda y filtrado dinamico utilizando Vanilla JavaScript puro en el frontend. Esto permite filtrar inventarios y metricas en tiempo real manipulando el DOM, manteniendo el proyecto bloat-free sin necesidad de integrar frameworks pesados solo para esta tarea.

### 3. Inteligencia de Negocio (Metricas Reales)
Desafio: Los totales de facturacion incluian el IVA, lo cual distorsionaba la metrica de productividad real del mecanico y la rentabilidad del taller.
Solucion: Refactorizacion de la logica de negocio en views.py. Las metricas ahora filtran dinamicamente por el mes en curso y separan los montos estrictamente Netos (Mano de obra vs. Costo de repuestos), aislando el ruido impositivo.

### 4. Integridad Historica y Escalabilidad Impositiva
Desafio: Las tasas de impuestos (como el IVA) pueden cambiar en el futuro o variar segun la region. Una actualizacion de estos valores no debe alterar los registros contables de meses o anos anteriores.
Solucion: Diseno de base de datos basado en "Snapshots" (Instantaneas). Los impuestos se configuran como variables iniciales, pero al procesar un servicio, el sistema guarda el valor absoluto y el porcentaje vigente en ese momento exacto. Esto blinda los registros historicos y establece una arquitectura escalable, facilitando la futura incorporacion de multiples impuestos locales o regionales a nivel de codigo sin romper la integridad contable.

### 5. Accesibilidad y Resiliencia
Desafio: El sistema debia estar accesible como un icono mas en el telefono del usuario, sin depender de abrir el navegador constantemente.
Solucion: Integracion de arquitectura PWA, configurando un manifest.json dinamico y un Service Worker para habilitar la instalacion de la aplicacion en dispositivos moviles (Android/iOS) y de escritorio (Standalone).

### Rutas y Endpoints
Al tratarse de una arquitectura MVT (Model-View-Template) renderizada desde el servidor, las siguientes rutas representan los puntos de acceso principales del sistema:

GET / : Dashboard o panel principal. Lista los servicios activos.

GET, POST /nuevo/ : Formulario de creacion de un nuevo ticket de servicio.

GET /inventario/ : Listado del inventario de refacciones y estado de stock.

GET, POST /inventario/nueva/ : Alta de nueva refaccion.

GET, POST /inventario/editar/<id>/ : Modificacion de una refaccion existente.

GET, POST /servicio/<id>/ : Detalle del ticket. Permite agregar refacciones consumidas y modificar el estado del servicio mediante una maquina de estados.

GET /metricas/ : Panel gerencial con el calculo de rendimiento por mecanico (filtrado por mes actual).

---

## Stack Tecnologico

* Backend: Python 3, Django 5.x
* Frontend: HTML5, Bootstrap 5.3, Vanilla JS, CSS3
* Base de Datos: SQLite3 (Desarrollo)
* Funcionalidades Extra: PWA, ReportLab (Generacion de PDF)

---

## Como levantar el entorno (Instalacion)

Paso 1: Clonar el repositorio usando git clone y la URL de tu repositorio.
Paso 2: Acceder a la carpeta del proyecto desde la terminal.
Paso 3: Crear un entorno virtual utilizando el comando: python -m venv env
Paso 4: Activar el entorno virtual (en Windows: env\Scripts\activate, en Linux/Mac: source env/bin/activate).
Paso 5: Instalar las dependencias necesarias ejecutando: pip install -r requirements.txt
Paso 6: IMPORTANTE. Crear un archivo llamado .env en la raiz del proyecto (al mismo nivel que manage.py) para alojar las variables de entorno requeridas, como credenciales de correo electronico y claves secretas.
Paso 7: Ejecutar las migraciones de la base de datos con los comandos: python manage.py makemigrations seguido de python manage.py migrate.
Paso 8: Crear un usuario administrador ejecutando: python manage.py createsuperuser.
Paso 9: Iniciar el servidor local de desarrollo con: python manage.py runserver.
Paso 10: Acceder al proyecto desde el navegador web en la direccion http://127.0.0.1:8000/