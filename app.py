from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)

# Datos geopolíticos completos de Ecuador
PROVINCIAS_DATA = {
    "Azuay": {
        "region": "Sierra",
        "capital": "Cuenca",
        "superficie": "8,189 km²",
        "poblacion": "881,394 hab.",
        "cantones": 15,
        "parroquias": 60,
        "geografia": "Región montañosa con valles interandinos",
        "economia": "Agricultura, turismo, artesanías, minería"
    },
    "Bolívar": {
        "region": "Sierra",
        "capital": "Guaranda",
        "superficie": "3,254 km²",
        "poblacion": "209,933 hab.",
        "cantones": 7,
        "parroquias": 29,
        "geografia": "Altiplano andino con páramos",
        "economia": "Agricultura, ganadería, turismo ecológico"
    },
    "Cañar": {
        "region": "Sierra",
        "capital": "Azogues",
        "superficie": "3,908 km²",
        "poblacion": "281,396 hab.",
        "cantones": 7,
        "parroquias": 28,
        "geografia": "Zona montañosa con laguna de Culebrillas",
        "economia": "Agricultura, ganadería, migración"
    },
    "Carchi": {
        "region": "Sierra",
        "capital": "Tulcán",
        "superficie": "3,699 km²",
        "poblacion": "186,869 hab.",
        "cantones": 6,
        "parroquias": 27,
        "geografia": "Frontera con Colombia, páramos",
        "economia": "Comercio fronterizo, agricultura, floricultura"
    },
    "Chimborazo": {
        "region": "Sierra",
        "capital": "Riobamba",
        "superficie": "5,287 km²",
        "poblacion": "524,004 hab.",
        "cantones": 10,
        "parroquias": 45,
        "geografia": "Nevado Chimborazo (6,268 m), páramos",
        "economia": "Agricultura, turismo, industria textil"
    },
    "Cotopaxi": {
        "region": "Sierra",
        "capital": "Latacunga",
        "superficie": "6,569 km²",
        "poblacion": "488,716 hab.",
        "cantones": 7,
        "parroquias": 33,
        "geografia": "Volcán Cotopaxi, valle interandino",
        "economia": "Agricultura, floricultura, industria"
    },
    "Imbabura": {
        "region": "Sierra",
        "capital": "Ibarra",
        "superficie": "4,599 km²",
        "poblacion": "476,257 hab.",
        "cantones": 6,
        "parroquias": 36,
        "geografia": "Lagos, volcanes, valle del Chota",
        "economia": "Turismo, agricultura, artesanías, comercio"
    },
    "Loja": {
        "region": "Sierra",
        "capital": "Loja",
        "superficie": "11,027 km²",
        "poblacion": "521,154 hab.",
        "cantones": 16,
        "parroquias": 78,
        "geografia": "Frontera con Perú, valles secos",
        "economia": "Minería, agricultura, ganadería, educación"
    },
    "Pichincha": {
        "region": "Sierra",
        "capital": "Quito",
        "superficie": "9,494 km²",
        "poblacion": "3,228,233 hab.",
        "cantones": 8,
        "parroquias": 65,
        "geografia": "Capital nacional, volcanes, equinoccial",
        "economia": "Servicios, gobierno, industria, turismo"
    },
    "Tungurahua": {
        "region": "Sierra",
        "capital": "Ambato",
        "superficie": "3,334 km²",
        "poblacion": "590,600 hab.",
        "cantones": 9,
        "parroquias": 44,
        "geografia": "Volcán Tungurahua activo, valle central",
        "economia": "Industria, comercio, agricultura, turismo"
    },
    "El Oro": {
        "region": "Costa",
        "capital": "Machala",
        "superficie": "5,988 km²",
        "poblacion": "715,751 hab.",
        "cantones": 14,
        "parroquias": 47,
        "geografia": "Costa sur, manglares, frontera con Perú",
        "economia": "Banano, camarón, cacao, minería"
    },
    "Esmeraldas": {
        "region": "Costa",
        "capital": "Esmeraldas",
        "superficie": "15,216 km²",
        "poblacion": "643,654 hab.",
        "cantones": 8,
        "parroquias": 42,
        "geografia": "Costa norte, selva tropical, playas",
        "economia": "Petróleo, turismo, pesca, agricultura tropical"
    },
    "Guayas": {
        "region": "Costa",
        "capital": "Guayaquil",
        "superficie": "17,139 km²",
        "poblacion": "4,387,434 hab.",
        "cantones": 25,
        "parroquias": 60,
        "geografia": "Puerto principal, río Guayas, isla Puná",
        "economia": "Puerto, industria, comercio, banca"
    },
    "Los Ríos": {
        "region": "Costa",
        "capital": "Babahoyo",
        "superficie": "7,205 km²",
        "poblacion": "921,763 hab.",
        "cantones": 13,
        "parroquias": 49,
        "geografia": "Cuenca baja del Guayas, llanura aluvial",
        "economia": "Agricultura (arroz, banano, cacao), ganadería"
    },
    "Manabí": {
        "region": "Costa",
        "capital": "Portoviejo",
        "superficie": "18,893 km²",
        "poblacion": "1,562,079 hab.",
        "cantones": 22,
        "parroquias": 74,
        "geografia": "Costa central, cordillera Chongón-Colonche",
        "economia": "Agricultura, pesca, turismo, petroquímica"
    },
    "Santa Elena": {
        "region": "Costa",
        "capital": "Santa Elena",
        "superficie": "3,690 km²",
        "poblacion": "401,178 hab.",
        "cantones": 3,
        "parroquias": 12,
        "geografia": "Península, playas, zona seca",
        "economia": "Turismo, pesca, petróleo, sal"
    },
    "Morona Santiago": {
        "region": "Amazonía",
        "capital": "Macas",
        "superficie": "25,690 km²",
        "poblacion": "196,535 hab.",
        "cantones": 12,
        "parroquias": 43,
        "geografia": "Selva amazónica, cordillera del Cóndor",
        "economia": "Minería, agricultura, ganadería, ecoturismo"
    },
    "Napo": {
        "region": "Amazonía",
        "capital": "Tena",
        "superficie": "12,476 km²",
        "poblacion": "133,705 hab.",
        "cantones": 5,
        "parroquias": 26,
        "geografia": "Selva amazónica, río Napo",
        "economia": "Petróleo, turismo ecológico, agricultura"
    },
    "Orellana": {
        "region": "Amazonía",
        "capital": "Puerto Francisco de Orellana",
        "superficie": "21,675 km²",
        "poblacion": "161,338 hab.",
        "cantones": 4,
        "parroquias": 30,
        "geografia": "Selva amazónica, río Napo",
        "economia": "Petróleo, agricultura, ganadería"
    },
    "Pastaza": {
        "region": "Amazonía",
        "capital": "Puyo",
        "superficie": "29,520 km²",
        "poblacion": "114,202 hab.",
        "cantones": 4,
        "parroquias": 19,
        "geografia": "Selva amazónica, transición sierra-oriente",
        "economia": "Turismo ecológico, agricultura, ganadería"
    },
    "Sucumbíos": {
        "region": "Amazonía",
        "capital": "Nueva Loja",
        "superficie": "18,327 km²",
        "poblacion": "230,503 hab.",
        "cantones": 7,
        "parroquias": 30,
        "geografia": "Frontera con Colombia, selva amazónica",
        "economia": "Petróleo, agricultura, comercio fronterizo"
    },
    "Zamora Chinchipe": {
        "region": "Amazonía",
        "capital": "Zamora",
        "superficie": "23,111 km²",
        "poblacion": "120,416 hab.",
        "cantones": 9,
        "parroquias": 28,
        "geografia": "Frontera con Perú, cordillera del Cóndor",
        "economia": "Minería (oro, cobre), agricultura, ganadería"
    },
    "Galápagos": {
        "region": "Insular",
        "capital": "Puerto Baquerizo Moreno",
        "superficie": "8,010 km²",
        "poblacion": "33,042 hab.",
        "cantones": 3,
        "parroquias": 6,
        "geografia": "Archipiélago volcánico, patrimonio mundial",
        "economia": "Turismo, conservación, pesca controlada"
    },
    "Santo Domingo": {
        "region": "Sierra",
        "capital": "Santo Domingo",
        "superficie": "3,857 km²",
        "poblacion": "458,580 hab.",
        "cantones": 1,
        "parroquias": 7,
        "geografia": "Transición sierra-costa, subtropical",
        "economia": "Agricultura, ganadería, comercio, industria"
    }
}

# Colores por región
REGION_COLORS = {
    "Costa": "#3b82f6",
    "Sierra": "#22c55e", 
    "Amazonía": "#ef4444",
    "Insular": "#f59e0b"
}

def create_directories():
    """Función para crear directorios necesarios"""
    directories = ['templates', 'data', 'static']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Directorio creado: {directory}")

@app.route("/")
def index():
    return render_template("mapa.html")

@app.route("/api/provincias")
def get_provincias():
    """API endpoint para obtener datos de provincias"""
    return jsonify(PROVINCIAS_DATA)

@app.route("/api/provincia/<nombre>")
def get_provincia(nombre):
    """API endpoint para obtener datos de una provincia específica"""
    if nombre in PROVINCIAS_DATA:
        return jsonify(PROVINCIAS_DATA[nombre])
    return jsonify({"error": "Provincia no encontrada"}), 404

@app.route("/data/<path:filename>")
def serve_data(filename):
    """Servir archivos de datos (GeoJSON)"""
    return send_from_directory("data", filename)

if __name__ == "__main__":
    # Crear directorios necesarios al inicio
    create_directories()
    
    print("🗺️  Servidor del Mapa Geopolítico de Ecuador iniciado")
    print("📍 Accede a: http://localhost:5000")
    print("🏛️  24 provincias con información completa")
    app.run(debug=True, host='0.0.0.0', port=5000)