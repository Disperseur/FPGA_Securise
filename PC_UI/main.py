from FPGA import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from collections import deque

KEY     = bytes.fromhex("8A55114D1CB6A9A2BE263D4D7AECAAFF")
NONCE   = bytes.fromhex("4ED0EC0B98C529B7C8CDDF37BCD0284A")
DA      = b"A to B"

class PlotWindow(QMainWindow):
    def __init__(self, waves, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.waves = waves
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Waveform Plotter')
        self.setGeometry(100, 100, 800, 600)
        
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        layout = QVBoxLayout(self.main_widget)
        
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        
        self.plot_widget.addLegend()
        self.plot_widget.showGrid(x=True, y=True)
        
        self.curve_decrypted = self.plot_widget.plot(pen='g', name='Decrypted')
        
        self.ptr_wave = 0
        self.ptr_sample = 0
        self.current_wave_decrypted = []
        
        # File circulaire avec une taille maximale pour scrolling
        self.decrypted_data = deque(maxlen=200)  # Ajuste à ta convenance
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(10)  # Affichage plus fluide, 10 ms

    def update_plot(self):
        if self.ptr_wave < len(self.waves):
            if self.ptr_sample == 0:
                # Nouveau bloc -> chiffrement/déchiffrement
                wave = self.waves[self.ptr_wave]
                wave_encrypted = fpga.encrypt_waveform_python(wave, KEY, NONCE, DA)
                wave_decrypted = fpga.decrypt_waveform_python(wave_encrypted, KEY, NONCE, DA)
                self.current_wave_decrypted = fpga.list_from_wave(wave_decrypted)
            
            # Ajout d'un échantillon à la file
            if self.ptr_sample < len(self.current_wave_decrypted):
                sample = self.current_wave_decrypted[self.ptr_sample]
                self.decrypted_data.append(sample)
                self.ptr_sample += 1
            else:
                # Passe au bloc suivant
                self.ptr_wave += 1
                self.ptr_sample = 0
            
            # Mise à jour du graphique
            self.curve_decrypted.setData(list(self.decrypted_data))

            # Limiter l'affichage aux deux derniers ECGs
            wave_length = len(self.current_wave_decrypted)
            start = max(0, len(self.decrypted_data) - 2 * wave_length)
            end = len(self.decrypted_data)
            self.plot_widget.setXRange(start, end)
        else:
            # Fin des données
            pass


if __name__ == '__main__':
    print("Starting application...")
    fpga = FPGA('COM11', 115200)
    print("FPGA initialized.")
    waves = fpga.read_csv_file("PC_UI/waveform_example_ecg.csv")
    print("Waves loaded.")

    app = QApplication(sys.argv)
    print("QApplication created.")
    mainWin = PlotWindow(waves)
    print("PlotWindow created.")
    mainWin.show()
    print("PlotWindow shown.")
    sys.exit(app.exec_())
