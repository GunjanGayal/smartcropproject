import sqlite3

DATABASE = "smartcrop.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_name TEXT UNIQUE,
            prevention TEXT,
            treatment TEXT
        )
    """)
    conn.commit()
    conn.close()
def insert_all_diseases():
    conn = get_db_connection()
    cursor = conn.cursor()

    diseases = [
        # Apple
        ("Apple___Apple_scab", "Remove fallen leaves, prune properly, ensure good air circulation", "Spray fungicide like Mancozeb or Captan"),
        ("Apple___Black_rot", "Remove infected fruit, prune trees", "Apply Copper-based fungicide"),
        ("Apple___Cedar_apple_rust", "Remove nearby cedar trees, prune infected branches", "Use fungicide if necessary"),
        ("Apple___healthy", "Maintain proper care", "No treatment needed"),
        # Blueberry
        ("Blueberry___healthy", "Maintain proper care", "No treatment needed"),
        # Cherry
        ("Cherry_(including_sour)___Powdery_mildew", "Ensure good air circulation, prune infected parts", "Use fungicide"),
        ("Cherry_(including_sour)___healthy", "Maintain proper care", "No treatment needed"),
        # Corn
        ("Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Rotate crops, avoid overhead watering", "Fungicide application if severe"),
        ("Corn_(maize)___Common_rust_", "Plant resistant varieties", "Use fungicide if needed"),
        ("Corn_(maize)___Northern_Leaf_Blight", "Rotate crops, remove debris", "Fungicide application if severe"),
        ("Corn_(maize)___healthy", "Maintain proper care", "No treatment needed"),
        # Grape
        ("Grape___Black_rot", "Remove infected parts", "Use fungicide"),
        ("Grape___Esca_(Black_Measles)", "Remove infected vines", "No chemical treatment"),
        ("Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Prune, remove infected leaves", "Fungicide if needed"),
        ("Grape___healthy", "Maintain proper care", "No treatment needed"),
        # Orange
        ("Orange___Haunglongbing_(Citrus_greening)", "Remove infected trees", "No cure"),
        # Peach
        ("Peach___Bacterial_spot", "Remove infected parts", "Copper-based spray"),
        ("Peach___healthy", "Maintain proper care", "No treatment needed"),
        # Pepper
        ("Pepper,_bell___Bacterial_spot", "Remove infected parts", "Use bactericide"),
        ("Pepper,_bell___healthy", "Maintain proper care", "No treatment needed"),
        # Potato
        ("Potato___Early_blight", "Remove infected plants", "Fungicide"),
        ("Potato___Late_blight", "Remove infected plants", "Fungicide"),
        ("Potato___healthy", "Maintain proper care", "No treatment needed"),
        # Raspberry
        ("Raspberry___healthy", "Maintain proper care", "No treatment needed"),
        # Soybean
        ("Soybean___healthy", "Maintain proper care", "No treatment needed"),
        # Squash
        ("Squash___Powdery_mildew", "Ensure good air circulation", "Use fungicide"),
        # Tomato (all major diseases from PlantVillage)
        ("Tomato___Bacterial_spot", "Remove infected leaves, avoid overhead watering", "Copper-based bactericide"),
        ("Tomato___Early_blight", "Remove infected plants, rotate crops", "Fungicide like Chlorothalonil"),
        ("Tomato___Late_blight", "Remove infected plants, ensure good airflow", "Fungicide like Mancozeb"),
        ("Tomato___Leaf_Mold", "Provide good air circulation, avoid wetting leaves", "Fungicide if needed"),
        ("Tomato___Septoria_leaf_spot", "Remove infected leaves, rotate crops", "Apply fungicide"),
        ("Tomato___Spider_mites Two-spotted_spider_mite", "Ensure proper watering, remove infested leaves", "Miticide if severe"),
        ("Tomato___Target_Spot", "Remove infected leaves, improve spacing", "Fungicide application"),
        ("Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Remove infected plants, control whiteflies", "No chemical cure"),
        ("Tomato___Tomato_mosaic_virus", "Remove infected plants, disinfect tools", "No chemical cure"),
        ("Tomato___healthy", "Maintain proper care", "No treatment needed")
    ]

    for d in diseases:
        cursor.execute(
            "INSERT OR IGNORE INTO diseases (disease_name, prevention, treatment) VALUES (?,?,?)",
            d
        )

    conn.commit()
    conn.close()

# Run once
create_tables()
insert_all_diseases()
print("✅ Database ready with all diseases")