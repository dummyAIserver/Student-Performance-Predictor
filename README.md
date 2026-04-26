# Student-Performance-Predictor

Project Setup & Running Instructions
This project is a Flask-based web application that predicts students’ final marks using a trained machine-learning model.
compatible with python3.10 version.

Follow the steps below to correctly set up and run the project.

1. Clone the Repository
git clone https://github.com/dummyAIserver/Student-Performance-Predictor.git
cd Student-Performance-Predictor

2. Download pretrained ml model(model.pkl file) from this link https://drive.google.com/file/d/1547GJ1Wum9L7v9sp8zRSKW37GJeRdMjT/view?usp=drive_link
   
4. Create a Virtual Environment
On Windows:
python310 -m venv venv
venv\Scripts\activate

On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

4. Install Dependencies
All required packages are listed in requirements.txt
pip install -r requirements.txt

5. (Optional) Retrain the Model
If you want to retrain the model, edit the file path in train_model.py (currently uses an absolute path) and run:
python train_model.py

6. Run the Streamlit Application
python app.py

The server will start, automatically open(if need permission click on 'yes' or 'run') you browser or click(ctrl+left mouse button) the localhost address in terminal.

7. Using the Application

Enter student name, attendance, assignment score, and internal marks.
The application will predict the final marks using the pre-trained ML model.
