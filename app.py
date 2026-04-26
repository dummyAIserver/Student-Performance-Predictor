<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pickle
import numpy as np
import pandas as pd
import os
from export_utils import create_excel_export, create_pdf_export, generate_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Load Model
model = pickle.load(open("model.pkl", "rb"))

HISTORY_FILE = "history.csv"


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    result = session.pop('result', None)
    return render_template("index.html", result=result)


# ---------------- PREDICTION ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        student_name = request.form.get("student_name", "Unknown").strip()
        attendance = float(request.form["attendance"])
        assignment = float(request.form["assignment"])
        internal = float(request.form["internal"])
    except:
        session['result'] = "Invalid input!"
        return redirect(url_for('home'))

    # Prediction
    x = np.array([[attendance, assignment, internal]])
    prediction = float(model.predict(x)[0])
    rounded_pred = round(prediction, 2)

    # Save to history.csv
    row = pd.DataFrame([{
        "student_name": student_name,
        "attendance": attendance,
        "assignment": assignment,
        "internal": internal,
        "prediction": rounded_pred
    }])

    if os.path.exists(HISTORY_FILE):
        row.to_csv(HISTORY_FILE, mode="a", header=False, index=False)
    else:
        row.to_csv(HISTORY_FILE, index=False)

    session['result'] = rounded_pred
    return redirect(url_for('home'))


# ---------------- HISTORY PAGE ----------------
@app.route("/history")
def history():
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        data = df.to_dict(orient="records")
    else:
        data = []

    return render_template("history.html", history=data)

# ---------------- CLEAR HISTORY ROUTE ----------------
@app.route("/clear-history", methods=["POST"])
def clear_history():
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            return {"success": True, "message": "History cleared successfully"}
        else:
            return {"success": True, "message": "No history to clear"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------------- EXPORT ROUTES ----------------
@app.route("/export/excel")
def export_excel():
    """Export history as Excel file"""
    try:
        # Get history data
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            history_data = df.to_dict(orient="records")
        else:
            history_data = []
        
        if not history_data:
            return {"success": False, "message": "No data to export"}
        
        # Create Excel file
        excel_file = create_excel_export(history_data)
        filename = generate_filename("xlsx")
        
        return send_file(
            excel_file,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return {"success": False, "message": f"Excel export failed: {str(e)}"}


@app.route("/export/pdf")
def export_pdf():
    """Export history as PDF file"""
    try:
        # Get history data
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            history_data = df.to_dict(orient="records")
        else:
            history_data = []
        
        if not history_data:
            return {"success": False, "message": "No data to export"}
        
        # Create PDF file
        pdf_file = create_pdf_export(history_data)
        filename = generate_filename("pdf")
        
        return send_file(
            pdf_file,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return {"success": False, "message": f"PDF export failed: {str(e)}"}

if __name__ == "__main__":
    app.run(debug=True)
=======
import pickle
import numpy as np
import streamlit as st

# Load the trained model
model = pickle.load(open("model.pkl", "rb"))

st.title("Student Final Marks Prediction")

st.write("Enter attendance, assignment score, and internal marks to predict final marks.")

# Input fields
attendance = st.number_input("Attendance", placeholder="Enter attendance (0-100)", step=0.1)
assignment = st.number_input("Assignment Score", placeholder="Enter assignment marks (0-20)", step=0.1)
internal = st.number_input("Internal Marks", placeholder="Enter internal marks (0-30)", step=0.1)

if st.button("Predict Final Marks"):
    # Prepare input data
    input_data = np.array([[attendance, assignment, internal]])
    
    # Make prediction
    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Final Marks: {prediction:.2f}")
>>>>>>> 875acd2202eb07739648d213d3b501ad3825ee3c
