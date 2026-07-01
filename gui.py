import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox,
    QPushButton, QLabel, QGroupBox, QScrollArea, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# from random_forest_model import predict_disease
from knn_model import predict_disease

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Disease Predictor")
        self.setGeometry(100, 100, 400, 500)
        self.setWindowIcon(QIcon("logo2.png"))

        title = QLabel("Disease Predictor")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 5px;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(title)

        # left_panel = QVBoxLayout()

        #Adding Scroll Feature
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)

        self.layout.addWidget(scroll)
        
        #SYMPTOMS LIST
        self.symptom_groups = {

            "General Symptoms": [
                "fatigue",
                "lethargy",
                "malaise",
                "high_fever",
                "mild_fever",
                "shivering",
                "chills",
                "sweating",
                "dehydration",
                "weight_gain",
                "weight_loss",
                "restlessness",
                "anxiety",
                "mood_swings",
                "irritability",
                "depression",
                "loss_of_appetite",
                "increased_appetite",
                "excessive_hunger"
            ],

            "Neurological Symptoms": [
                "headache",
                "dizziness",
                "loss_of_balance",
                "unsteadiness",
                "spinning_movements",
                "slurred_speech",
                "altered_sensorium",
                "lack_of_concentration",
                "visual_disturbances",
                "coma",
                "weakness_of_one_body_side",
                "loss_of_smell"
            ],

            "Respiratory Symptoms": [
                "continuous_sneezing",
                "cough",
                "breathlessness",
                "phlegm",
                "throat_irritation",
                "sinus_pressure",
                "runny_nose",
                "congestion",
                "mucoid_sputum",
                "rusty_sputum",
                "blood_in_sputum",
                "chest_pain",
                "patches_in_throat"
            ],

            "Digestive Symptoms": [
                "stomach_pain",
                "acidity",
                "ulcers_on_tongue",
                "vomiting",
                "indigestion",
                "nausea",
                "constipation",
                "abdominal_pain",
                "diarrhoea",
                "belly_pain",
                "passage_of_gases",
                "stomach_bleeding",
                "distention_of_abdomen",
                "swelling_of_stomach"
            ],

            "Skin & Allergy Symptoms": [
                "skin_rash",
                "nodal_skin_eruptions",
                "dischromic_patches",
                "red_spots_over_body",
                "pus_filled_pimples",
                "blackheads",
                "scurring",
                "skin_peeling",
                "silver_like_dusting",
                "blister",
                "red_sore_around_nose",
                "yellow_crust_ooze",
                "inflammatory_nails",
                "small_dents_in_nails"
            ],

            "Muscle & Joint Symptoms": [
                "joint_pain",
                "muscle_wasting",
                "muscle_pain",
                "muscle_weakness",
                "back_pain",
                "neck_pain",
                "knee_pain",
                "hip_joint_pain",
                "stiff_neck",
                "swelling_joints",
                "movement_stiffness",
                "cramps",
                "painful_walking",
                "weakness_in_limbs"
            ],

            "Cardiovascular Symptoms": [
                "fast_heart_rate",
                "palpitations",
                "prominent_veins_on_calf",
                "swollen_blood_vessels",
                "cold_hands_and_feets"
            ],

            "Liver & Jaundice Symptoms": [
                "yellowish_skin",
                "yellow_urine",
                "yellowing_of_eyes",
                "dark_urine",
                "acute_liver_failure",
                "toxic_look_(typhos)"
            ],

            "Urinary Symptoms": [
                "burning_micturition",
                "spotting_ urination",
                "bladder_discomfort",
                "foul_smell_of urine",
                "continuous_feel_of_urine",
                "polyuria"
            ],

            "Eye & ENT Symptoms": [
                "sunken_eyes",
                "blurred_and_distorted_vision",
                "redness_of_eyes",
                "watering_from_eyes",
                "pain_behind_the_eyes"
            ],

            "Hormonal & Metabolic Symptoms": [
                "irregular_sugar_level",
                "obesity",
                "enlarged_thyroid",
                "brittle_nails",
                "swollen_extremeties",
                "puffy_face_and_eyes"
            ],

            "Swelling & Inflammation": [
                "swollen_legs",
                "swelled_lymph_nodes",
                "fluid_overload"
            ],

            "Bowel & Anal Symptoms": [
                "pain_during_bowel_movements",
                "pain_in_anal_region",
                "bloody_stool",
                "irritation_in_anus"
            ],

            "Reproductive & Women's Health": [
                "abnormal_menstruation"
            ],

            "Risk Factors & Lifestyle": [
                "family_history",
                "history_of_alcohol_consumption",
                "extra_marital_contacts",
                "receiving_blood_transfusion",
                "receiving_unsterile_injections"
            ]
            }
        
        self.checkboxes = []        
        for group, symptoms in self.symptom_groups.items():
            group_box = QGroupBox(group)
            group_layout = QVBoxLayout()
            group_box.setLayout(group_layout)
            scroll_layout.addWidget(group_box)

            for symptom in symptoms:
                cb = QCheckBox(symptom)
                group_layout.addWidget(cb)
                self.checkboxes.append(cb)
        
        scroll_layout.addStretch() #This makes the unused space to be occupied by empty

        
        self.predict_button = QPushButton("Analyse Symptoms")
        self.predict_button.clicked.connect(self.get_selected)
        self.layout.addWidget(self.predict_button)

        self.setStyleSheet("""
            QWidget {
                background-color: #3d3d3d;
                font-size: 14px;
            }

            QGroupBox {
                font-weight: bold;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px 0 0 0;
                background-color: white;
            }

            QCheckBox {
                padding: 5px;
                border-radius: 8px;
                background-color: white;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
            
            QScrollArea {
                border: none;
            }

            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #999;
                border-radius: 4px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: #777;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
                           
            QCheckBox {
                border: none;
                padding: 8px 12px;
                border-radius: 10px;
                background-color: #f0f0f0;
            }

            QCheckBox::indicator {
                image: none;
            }

            QCheckBox:hover {
                background-color: #e0e0e0;
            }

            QCheckBox:checked {
                border: 1px solid #4CAF50;
                background-color: #dff5e1;
            }
            
        """)

        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)

        self.figure = Figure(facecolor="#1e1e1e")

        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)

    def get_selected(self):
        selected = []

        for cb in self.checkboxes:
            if cb.isChecked():
                selected.append(cb.text())

        if len(selected) < 3:
            print("Select at least 3 symptoms")
            return

        results = predict_disease(selected)

        print(results)

        # Clear old graph
        self.figure.clear()

        # Create graph area
        ax = self.figure.add_subplot(111)

        # Extract disease names and probabilities
        diseases = [x[0] for x in results]
        probs = [x[1] for x in results]

        # Create horizontal bar graph
        ax.barh(diseases, probs)

        # Dark theme styling
        ax.set_facecolor("#1e1e1e")
        self.figure.patch.set_facecolor("#1e1e1e")

        ax.tick_params(colors="white")

        ax.set_xlabel("Probability (%)", color="white")
        ax.set_title("Predicted Diseases", color="white")

        # Refresh canvas
        self.canvas.draw()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())