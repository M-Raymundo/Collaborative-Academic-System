from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from os import path

DATA_FILE = "data.json"
app = Flask(__name__)
CORS(app)

def load_students():
    if not path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        for aluno in data:
            if "school_grades" not in aluno or not isinstance(aluno["school_grades"], dict):
                aluno["school_grades"] = {"AVA 1": 0.0, "AVA 2": 0.0, "AVA 3": 0.0}
            else:
                for n in ["AVA 1", "AVA 2", "AVA 3"]:
                    aluno["school_grades"].setdefault(n, 0.0)
        return data

def save_students(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify({"users": load_students()})

@app.route("/students/update", methods=["POST"])
def update_student():
    student_data = request.get_json()
    if not student_data or "email" not in student_data:
        return jsonify({"error": "Aluno inválido"}), 400

    students = load_students()
    updated = False
    for idx, aluno in enumerate(students):
        if aluno.get("email") == student_data["email"]:
            students[idx].update(student_data)
            updated = True
            break
    if not updated:
        students.append(student_data)

    save_students(students)
    return jsonify({"message": "Aluno atualizado com sucesso!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)