import sys

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)

from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
    QLabel,
    QGroupBox,
    QScrollArea
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from random_forest_model import predict_disease
# from knn_model import predict_disease


class App(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Disease Predictor")
        # self.setGeometry(100, 100, 1300, 800)
        self.showMaximized()

        self.setWindowIcon(QIcon("logo.png"))

        self.setStyleSheet("""

            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-size: 14px;
            }

            QGroupBox {
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                background-color: #3a3a3a;
                margin-top: 10px;
            }

            QCheckBox {
                padding: 8px;
                border-radius: 8px;
                background-color: #4a4a4a;
            }

            QCheckBox:hover {
                background-color: #5a5a5a;
            }

            QCheckBox:checked {
                background-color: #4CAF50;
                border: 1px solid white;
            }

            QCheckBox::indicator {
                image: none;
            }

            QPushButton {
                background-color: #4CAF50;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 15px;
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
            }

            QScrollBar::handle:vertical {
                background: #888;
                border-radius: 4px;
            }

        """)

        # MAIN LAYOUT
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # LEFT PANEL
        left_panel = QVBoxLayout()

        # TITLE
        title = QLabel("Disease Predictor")

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            padding: 10px;
        """)

        left_panel.addWidget(title)

        # SCROLL AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()

        scroll_layout = QVBoxLayout()

        scroll_content.setLayout(scroll_layout)

        scroll.setWidget(scroll_content)

        left_panel.addWidget(scroll)

        #SYMPTOM GROUPS
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

            for symptom in symptoms:

                cb = QCheckBox(symptom)

                group_layout.addWidget(cb)

                self.checkboxes.append(cb)

            scroll_layout.addWidget(group_box)

        scroll_layout.addStretch()

        # ANALYZE BUTTON
        self.predict_button = QPushButton(
            "Analyse Symptoms"
        )

        self.clear_button = QPushButton(
            "Clear Selection"
        )

        self.clear_button.clicked.connect(
            self.clear_selection
        )

        self.predict_button.clicked.connect(
            self.get_selected
        )

        left_panel.addWidget(self.predict_button)
        left_panel.addWidget(self.clear_button)

        # RIGHT PANEL
        right_panel = QVBoxLayout()

        # RESULT LABEL
        self.result_label = QLabel(
            "Select symptoms and click Analyse"
        )

        self.result_label.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
        """)

        right_panel.addWidget(self.result_label)

        # GRAPH
        self.figure = Figure(
            facecolor="#2b2b2b"
        )

        self.canvas = FigureCanvas(self.figure)

        # TOOLBAR
        self.toolbar = NavigationToolbar(
            self.canvas,
            self
        )

        right_panel.addWidget(self.toolbar)
        right_panel.addWidget(self.canvas)

        # HIDE INITIALLY
        self.canvas.hide()
        self.toolbar.hide()

        # ADD PANELS
        self.layout.addLayout(left_panel, 2)
        self.layout.addLayout(right_panel, 3)

    def get_selected(self):

        selected = []

        for cb in self.checkboxes:

            if cb.isChecked():

                selected.append(cb.text())

        if len(selected) < 3:

            self.result_label.setText(
                "Please select at least 3 symptoms."
            )

            return

        # SHOW GRAPH AREA
        self.canvas.show()
        self.toolbar.show()

        # GET MODEL RESULTS
        results = predict_disease(selected)

        # UPDATE RESULT TEXT
        text = ""

        for disease, prob in results:

            text += f"{disease} : {prob}%\n"

        self.result_label.setText(text)

        # CLEAR OLD GRAPH
        self.figure.clear()

        # CREATE AXIS
        ax = self.figure.add_subplot(111)

        diseases = [x[0] for x in results]
        probs = [x[1] for x in results]

        # DRAW GRAPH
        ax.barh(diseases, probs)

        # GRAPH STYLING
        ax.set_facecolor("#2b2b2b")

        self.figure.patch.set_facecolor("#2b2b2b")

        ax.tick_params(colors="white")

        ax.set_xlabel(
            "Probability (%)",
            color="white"
        )

        ax.set_title(
            "Predicted Diseases",
            color="white"
        )

        ax.set_xlim(0, 100)

        # REDRAW
        self.figure.tight_layout()
        self.canvas.draw()

    def clear_selection(self):

        for cb in self.checkboxes:

            cb.setChecked(False)

        self.result_label.setText(
            "Selections cleared."
        )

        self.figure.clear()

        self.canvas.draw()

        self.canvas.hide()

        self.toolbar.hide()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = App()

    window.show()

    sys.exit(app.exec())