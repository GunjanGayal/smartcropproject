import sqlite3

conn = sqlite3.connect("smartcrop.db")
cursor = conn.cursor()

diseases = [
    ("Apple___Apple_scab", "Maintain clean orchard", "Apply fungicide"),
    ("Apple___Black_rot", "Remove infected leaves", "Use copper fungicide"),
    ("Apple___Cedar_apple_rust", "Remove nearby cedar", "Apply fungicide"),
    ("Apple___healthy", "Maintain healthy practices", "No treatment required"),
    ("Blueberry___healthy", "Regular monitoring", "No treatment required"),
    ("Cherry_(including_sour)___Powdery_mildew", "Avoid overcrowding", "Apply sulfur fungicide"),
    ("Cherry_(including_sour)___healthy", "Keep clean orchard", "No treatment required"),
    ("Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Rotate crops", "Fungicide spray"),
    ("Corn_(maize)___Common_rust_", "Resistant varieties", "Fungicide spray"),
    ("Corn_(maize)___Northern_Leaf_Blight", "Good drainage", "Apply fungicide"),
    ("Corn_(maize)___healthy", "Maintain healthy practices", "No treatment required"),
    ("Grape___Black_rot", "Prune infected areas", "Fungicide spray"),
    ("Grape___Esca_(Black_Measles)", "Remove diseased vines", "Fungicide application"),
    ("Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Avoid wet leaves", "Apply fungicide"),
    ("Grape___healthy", "Regular monitoring", "No treatment required"),
    ("Orange___Haunglongbing_(Citrus_greening)", "Remove infected trees", "No chemical cure"),
    ("Peach___Bacterial_spot", "Sanitize tools", "Copper spray"),
    ("Peach___healthy", "Maintain good care", "No treatment required"),
    ("Pepper,_bell___Bacterial_spot", "Crop rotation", "Copper-based treatment"),
    ("Pepper,_bell___healthy", "Healthy practices", "No treatment required"),
    ("Potato___Early_blight", "Use certified seed", "Apply fungicide"),
    ("Potato___Late_blight", "Good drainage", "Fungicide spray"),
    ("Potato___healthy", "Regular care", "No treatment required"),
    ("Raspberry___healthy", "Prune regularly", "No treatment required"),
    ("Soybean___healthy", "Rotate crops", "No treatment required"),
    ("Squash___Powdery_mildew", "Avoid wet foliage", "Apply sulfur spray")
]


for d in diseases:
    try:
        cursor.execute("INSERT INTO diseases (disease_name, prevention, treatment) VALUES (?,?,?)", d)
    except sqlite3.IntegrityError:
        pass  # agar duplicate ho to ignore

conn.commit()
conn.close()
print("✅ Diseases data inserted successfully")