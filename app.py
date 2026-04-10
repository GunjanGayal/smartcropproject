from flask import Flask, render_template, request, redirect, session
import sqlite3, os
import tensorflow as tf
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
import math
import cv2

app = Flask(__name__)
app.secret_key = "smartcropsecret"

DATABASE = "smartcrop.db"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png","jpg","jpeg"}

# ---------------- DATABASE ----------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS uploads(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            filename TEXT,
            crop TEXT,
            disease TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

create_tables()

# ---------------- MODEL ----------------
MODEL_PATH = "plant_disease_model.h5"
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
else:
    model = None

class_names = [
"Apple___Apple_scab","Apple___Black_rot","Apple___Cedar_apple_rust","Apple___healthy",
"Blueberry___healthy",
"Cherry_(including_sour)___Powdery_mildew","Cherry_(including_sour)___healthy",
"Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot","Corn_(maize)___Common_rust_",
"Corn_(maize)___Northern_Leaf_Blight","Corn_(maize)___healthy",
"Grape___Black_rot","Grape___Esca_(Black_Measles)","Grape___Leaf_blight_(Isariopsis_Leaf_Spot)","Grape___healthy",
"Orange___Haunglongbing_(Citrus_greening)",
"Peach___Bacterial_spot","Peach___healthy",
"Pepper,_bell___Bacterial_spot","Pepper,_bell___healthy",
"Potato___Early_blight","Potato___Late_blight","Potato___healthy",
"Raspberry___healthy","Soybean___healthy","Squash___Powdery_mildew",
"Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___Late_blight",
"Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot",
"Tomato___Spider_mites Two-spotted_spider_mite","Tomato___Target_Spot",
"Tomato___Tomato_Yellow_Leaf_Curl_Virus","Tomato___Tomato_mosaic_virus",
"Tomato___healthy"
]

# ---------------- IMAGE PREPROCESS ----------------
def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(128,128))
    img = img.astype("float32")/255.0
    img = np.expand_dims(img,axis=0)
    return img

# ---------------- BASIC LEAF-LIKE FILTER ----------------
def is_leaf_like(path):

    img = cv2.imread(path)
    img = cv2.resize(img,(128,128))

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([25,40,40])
    upper_green = np.array([90,255,255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    green_ratio = np.sum(mask > 0) / mask.size

    # agar green bahut kam hai to leaf nahi
    if green_ratio < 0.15:
        return False

    return True

# ---------------- ENTROPY CHECK ----------------
def  is_valid_prediction(probs, threshold=0.6):
    probs = np.array(probs)
    probs = probs / np.sum(probs)
    entropy = -np.sum(probs * np.log(probs + 1e-10))
    max_entropy = math.log(len(probs))
    return (entropy / max_entropy) < threshold

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# -------- User Registration --------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
            conn.commit()
        except:
            conn.close()
            return "Username already exists"
        conn.close()
        session["user"] = username
        return redirect("/upload")
    return render_template("register.html")

# Admin Login



# Main Admin Login (works with /admin)
@app.route("/admin", methods=["GET","POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if (username == "admin" and password == "admin123") or(username == "Mamta" and password == "mamta123") or (username == "Sivali" and password == "sivali123")    :
            session["admin"] = True
            return redirect("/admin/users")  # Dashboard
        else:
            error = "Invalid admin credentials"
    return render_template("admin_login.html", error=error)

# Optional alias route: /admin_login
@app.route("/admin_login", methods=["GET","POST"])
def admin_login_alias():
    return admin_login()  # Calls the same login function

# Dashboard showing all users
@app.route("/admin/users")
def admin_users():
    if not session.get("admin"):
        return redirect("/admin")  # Redirect if not logged in
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    uploads = conn.execute("SELECT * FROM uploads ORDER BY timestamp DESC").fetchall()
    conn.close()
    return render_template("admin_dashboard.html", users=users, uploads=uploads)


# Edit user
@app.route("/admin/edit_user/<int:user_id>", methods=["GET","POST"])
def edit_user(user_id):
    if not session.get("admin"):
        return redirect("/admin")
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        conn.execute("UPDATE users SET username=?, password=? WHERE id=?", (username,password,user_id))
        conn.commit()
        conn.close()
        return redirect("/admin/users")
    conn.close()
    return render_template("admin_edit_user.html", user=user)

# Delete user
@app.route("/admin/delete_user/<int:user_id>")
def delete_user(user_id):
    if not session.get("admin"):
        return redirect("/admin")
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return redirect("/admin/users")
# Multiple delete users
@app.route("/admin/delete_multiple_users", methods=["POST"])
def delete_multiple_users():
    if not session.get("admin"):
        return redirect("/admin")

    user_ids = request.form.getlist("user_ids")

    if user_ids:
        conn = get_db_connection()
        conn.executemany("DELETE FROM users WHERE id=?", [(uid,) for uid in user_ids])
        conn.commit()
        conn.close()

    return redirect("/admin/users")
@app.route("/admin/delete_upload/<int:id>")
def delete_upload(id):
    if not session.get("admin"):
        return redirect("/admin")

    conn = get_db_connection()

    file = conn.execute("SELECT filename FROM uploads WHERE id=?", (id,)).fetchone()

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file["filename"])
        if os.path.exists(filepath):
            os.remove(filepath)

    conn.execute("DELETE FROM uploads WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin/users")


# ✅ YAHAN PASTE KARO (function ke bahar)
@app.route("/admin/delete_multiple_uploads", methods=["POST"])
def delete_multiple_uploads():
    if not session.get("admin"):
        return redirect("/admin")

    upload_ids = request.form.getlist("upload_ids")

    if upload_ids:
        conn = get_db_connection()

        for uid in upload_ids:
            file = conn.execute("SELECT filename FROM uploads WHERE id=?", (uid,)).fetchone()

            if file:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file["filename"])
                if os.path.exists(filepath):
                    os.remove(filepath)

            conn.execute("DELETE FROM uploads WHERE id=?", (uid,))

        conn.commit()
        conn.close()

    return redirect("/admin/users")
@app.route("/upload",methods=["GET","POST"])
def upload():


    if "user" not in session:
        return redirect("/register")

    if request.method=="POST":

        file=request.files["image"]

        if file.filename=="":
            return "No file selected"

        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(file.filename)}"

        if "." not in filename or filename.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:
            return "Invalid file type"

        path=os.path.join(app.config["UPLOAD_FOLDER"],filename)
        file.save(path)

        crop = "Invalid Image"
        disease = "Not a Crop Leaf"
        confidence = 0

        # Leaf check
        if is_leaf_like(path) and model:

            img = preprocess_image(path)
            probs = model.predict(img)[0]

            if is_valid_prediction(probs, threshold=0.45):

                index = np.argmax(probs)
                confidence = float(probs[index]) * 100

                # confidence validation
                if confidence >= 80:

                    predicted_class = class_names[index]

                    if "___" in predicted_class:
                        crop, disease = predicted_class.split("___",1)
                    else:
                        crop = predicted_class
                        disease = "Unknown"

        # Save upload record
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO uploads (username,filename,crop,disease,confidence,timestamp) VALUES (?,?,?,?,?,?)",
            (session["user"],filename,crop,disease,round(confidence,2),str(datetime.now()))
        )
        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            crop=crop,
            disease=disease,
            prevention="Check crop health regularly",
            treatment="Follow recommended practices",
            confidence=round(confidence,2),
            image_file=filename
        )

    return render_template("upload.html")
# ---------------- RUN ----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)