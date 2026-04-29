import pickle
import numpy as np
import streamlit as st
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from export_utils import create_excel_export, create_pdf_export, generate_filename
import io

# Check if model exists, if not train it
if not os.path.exists("model.pkl"):
    st.info("Training model... (this runs only once)")
    
    # Load dataset and train
    df = pd.read_csv("student_performance_dataset.csv")
    X = df[["attendance", "assignment_score", "internal_marks"]]
    y = df["final_marks"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = RandomForestRegressor(n_estimators=400, max_depth=14, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
else:
    # Load the trained model
    model = pickle.load(open("model.pkl", "rb"))

# Streamlit page setup
st.set_page_config(page_title="Student Performance Predictor", layout="wide")

# History file
HISTORY_FILE = "history.csv"

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Predict", "History", "Export"])

if page == "Predict":
    st.title("Student Final Marks Prediction")
    st.write("Enter attendance, assignment score, and internal marks to predict final marks.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        student_name = st.text_input("Student Name", placeholder="Enter student name")
    
    with col2:
        attendance = st.number_input("Attendance", min_value=0.0, max_value=100.0, step=0.1)
    
    with col3:
        assignment = st.number_input("Assignment Score", min_value=0.0, max_value=20.0, step=0.1)
    
    internal = st.number_input("Internal Marks", min_value=0.0, max_value=30.0, step=0.1)
    
    if st.button("Predict Final Marks", use_container_width=True):
        # Prepare input data
        input_data = np.array([[attendance, assignment, internal]])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        rounded_pred = round(prediction, 2)
        
        # Save to history
        row = pd.DataFrame([{
            "student_name": student_name if student_name else "Unknown",
            "attendance": attendance,
            "assignment": assignment,
            "internal": internal,
            "prediction": rounded_pred
        }])
        
        if os.path.exists(HISTORY_FILE):
            row.to_csv(HISTORY_FILE, mode="a", header=False, index=False)
        else:
            row.to_csv(HISTORY_FILE, index=False)
        
        st.success(f"Predicted Final Marks: **{rounded_pred}**")

elif page == "History":
    st.title("Prediction History")
    
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        st.dataframe(df, use_container_width=True)
        
        if st.button("Clear History"):
            os.remove(HISTORY_FILE)
            st.success("History cleared!")
            st.rerun()
    else:
        st.info("No prediction history yet.")

elif page == "Export":
    st.title("Export History")
    
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        history_data = df.to_dict(orient="records")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export as Excel", use_container_width=True):
                try:
                    excel_file = create_excel_export(history_data)
                    filename = generate_filename("xlsx")
                    
                    st.download_button(
                        label="Download Excel File",
                        data=excel_file.getvalue(),
                        file_name=filename,
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    st.success("Excel file ready for download!")
                except Exception as e:
                    st.error(f"Excel export failed: {str(e)}")
        
        with col2:
            if st.button("📄 Export as PDF", use_container_width=True):
                try:
                    pdf_file = create_pdf_export(history_data)
                    filename = generate_filename("pdf")
                    
                    st.download_button(
                        label="Download PDF File",
                        data=pdf_file.getvalue(),
                        file_name=filename,
                        mime='application/pdf'
                    )
                    st.success("PDF file ready for download!")
                except Exception as e:
                    st.error(f"PDF export failed: {str(e)}")
    else:
        st.info("No prediction history to export.")