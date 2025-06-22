import math, sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox

application = QApplication(sys.argv)

mainWindow = QWidget()
mainWindow.resize(420, 200)
mainWindow.setWindowTitle("Zerfallsrechner")
layout = QVBoxLayout()
mainWindow.setLayout(layout)

#Feld mit der Anleitung hinzufügen
anleitung = QLabel(f"Gewünschtes Isotop auswählen sowie Anfangsaktivität\n"
                   "und Dauer zur Berechnung eintragen.")
layout.addWidget(anleitung)

#Ein Dropdown Menü zum Auswählen der Isotope
isotopLabel = QLabel(f"Isotop:")
layout.addWidget(isotopLabel)
isotopAuswahl = QComboBox()
isotopAuswahl.addItems(["Tc99m", "Mo99", "I131"])
layout.addWidget(isotopAuswahl)

#Die beiden Textboxen zum Eintragen der Aktivität und Dauer (inkl. Label)
textfeldStartAktivitaet = QLineEdit()
textfeldDauer = QLineEdit()
labelStartAktivitaet = QLabel(f"Anfangsaktivität:")
labelDauer = QLabel(f"Vergangene Zeit (in Stunden):")
layout.addWidget(labelStartAktivitaet)
layout.addWidget(textfeldStartAktivitaet)
layout.addWidget(labelDauer)
layout.addWidget(textfeldDauer)

#Den Button hinzufügen, der den Vergleich startet
button = QPushButton("Berechnen")
button.setFixedSize(100, 50)
layout.addWidget(button)

#Fügt das Label mit dem Ergebnistext ein
labelErgebnis = QLabel()
layout.addWidget(labelErgebnis)

#Zeigt das Hauptfenster an
mainWindow.show()

#Legt fest, dass eine entsprechende Meldung ausgegeben wird, wenn Fehlerhafte Eingaben getätigt werden
def error():
    labelErgebnis.setText("Da ist etwas schief gelaufen. Bitte nur Zahlen eingeben und\n"
                              "zur Trennung der Nachkommastellen einen Punkt verwenden!\n\n\n\n")

#legt fest, dass beim ändern des Isotops automatisch die richtige HWZ hinterlegt wird

def berechnung_starten():
    ausgewaehlt = isotopAuswahl.currentText()
    if ausgewaehlt == "Tc99m":
        hwz = 6
    elif ausgewaehlt == "Mo99":
        hwz = 66
    elif ausgewaehlt == "I131":
        hwz = 192.48
    try:
        #Anzahl Kerne/Aktivität
        anfangsaktivitaet = float(textfeldStartAktivitaet.text())
        # Dauer (Zeitpunkt, bis zu dem man den/die Zerfall/Aktivitätsabklingung berechnen möchte
        dauer = float(textfeldDauer.text())
    except:
        error()


    # Formel

    #Zerfallsgesetz
    def zerfallsformel(anfangsaktivitaet, hwz, dauer):
        try:
            return float((anfangsaktivitaet*math.exp(-(math.log(2)/hwz*dauer))))
        except:
            error()
    #Berechnung des Ergebnisses per Zerfallsgesetz
    try:
        ergebnis = zerfallsformel(anfangsaktivitaet, hwz, dauer)
        verhaeltnis = ergebnis/anfangsaktivitaet
    except:
        error()

    #Ausgabe des Ergebnisses
    try:
        labelErgebnis.setText(f"Nach {dauer} Stunden ist noch {ergebnis} Aktivität vorhanden. \nDas entspricht {verhaeltnis*100}% der Anfangsaktivität.\n\n"
                              "Hinweis: Die Einheit der Restaktivität ist gleich der \neingegebenen Anfangsaktiviät.\n")
    except:
        error()

#Startet den Berechnungsvorgang beim Drücken eines Buttons oder der Enter Taste
button.clicked.connect(berechnung_starten)
textfeldDauer.returnPressed.connect(berechnung_starten)
textfeldStartAktivitaet.returnPressed.connect(berechnung_starten)

sys.exit(application.exec())