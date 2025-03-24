from FPGA import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from collections import deque
import neurokit2 as nk
import numpy as np
from time import sleep

KEY =   bytes.fromhex('4B8A55114D1CB6A9A2BE263D4D7AECAAFF')
NONCE = bytes.fromhex('4E4ED0EC0B98C529B7C8CDDF37BCD0284A')
DA =    bytes.fromhex('444120746F20428000')

W = b'57'
PADDING = b'800000'

# Variable globale pour choisir le nombre d'ECGs affichés
NUM_ECGS_DISPLAYED = 10
# Variable globale pour choisir le nombre d'ECGs utilisés pour le calcul du BPM
NUM_ECGS_FOR_BPM = 20

class PlotWindow(QMainWindow):
    def __init__(self, waves, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.waves = waves
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ECG Plotter')
        self.setGeometry(0, 0, 1500, 400)
        
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        layout = QVBoxLayout(self.main_widget)
        
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        
        self.plot_widget.addLegend()
        self.plot_widget.showGrid(x=True, y=True)
        
        self.curve_decrypted = self.plot_widget.plot(pen='g', name='Decrypted')
        self.curve_filtered = self.plot_widget.plot(pen='w', name='Filtered')
        self.curve_peaks = self.plot_widget.plot(pen=None, symbol='o', symbolBrush='r', name='R-peaks')
        
        self.ptr_wave = 0
        self.ptr_sample = 0
        self.current_wave_decrypted = []
        
        # File circulaire assez grande pour NUM_ECGS_DISPLAYED ECGs
        self.decrypted_data = deque(maxlen=max(NUM_ECGS_DISPLAYED, NUM_ECGS_FOR_BPM) * 2000)
        self.filtered_data = []
        self.peaks_x = []
        self.peaks_y = []
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1)  # Affichage fluide

        # Timer BPM
        self.bpm_timer = QtCore.QTimer()
        self.bpm_timer.timeout.connect(self.detect_peaks_and_bpm)
        self.bpm_timer.start(500)

    def update_plot(self):
        if self.ptr_wave < len(self.waves):
            if self.ptr_sample == 0:
                # Nouveau bloc -> chiffrement/déchiffrement
                wave = self.waves[self.ptr_wave] # bytes
                wave = W + wave + PADDING
                wave = bytes(wave).decode('utf-8') #str
                wave = bytes.fromhex(wave)
                print(wave)
                
                fpga.send_waveform(wave)
                fpga.start_encryption()
                
                cipher = fpga.get_cipher()
                tag = fpga.get_tag()


                # wave_encrypted = fpga.encrypt_waveform_python(wave, KEY, NONCE, DA)
                wave_decrypted = fpga.decrypt_waveform_python(cipher[:-3]+tag, KEY[1:], NONCE[1:], DA[1:-2])
                self.current_wave_decrypted = fpga.list_from_wave(wave_decrypted.hex())
            
            # Ajout d'un échantillon
            if self.ptr_sample < len(self.current_wave_decrypted):
                sample = self.current_wave_decrypted[self.ptr_sample]
                self.decrypted_data.append(sample)
                self.ptr_sample += 1
            else:
                self.ptr_wave += 1
                self.ptr_sample = 0
            
            # Mise à jour graphique
            self.curve_decrypted.setData(list(self.decrypted_data))
            self.curve_peaks.setData(self.peaks_x, self.peaks_y)
            self.curve_filtered.setData(self.filtered_data)

            # Afficher NUM_ECGS_DISPLAYED ECGs
            wave_length = len(self.current_wave_decrypted)
            start = max(0, len(self.decrypted_data) - NUM_ECGS_DISPLAYED * wave_length)
            end = len(self.decrypted_data)
            self.plot_widget.setXRange(start, end)

    def detect_peaks_and_bpm(self):
        MIN_LENGTH = 3000  # Minimum pour éviter les erreurs avec le filtre
        if len(self.decrypted_data) < MIN_LENGTH:
            self.setWindowTitle('Waveform Plotter - BPM: --')
            return

        ecg_signal = np.array(self.decrypted_data)[-NUM_ECGS_FOR_BPM * 2000:]  # Plus de données pour BPM
        try:
            # Application du filtre ECG spécifique de NeuroKit2
            filtered_ecg = nk.ecg_clean(ecg_signal, sampling_rate=1000, method="neurokit")
            self.filtered_data = filtered_ecg.tolist()
            
            _, rpeaks = nk.ecg_peaks(filtered_ecg, sampling_rate=1000)
            peaks = rpeaks['ECG_R_Peaks']

            if len(peaks) < 2:
                self.setWindowTitle('Waveform Plotter - BPM: --')
                return

            offset = len(self.decrypted_data) - len(filtered_ecg)
            self.peaks_x = (peaks + offset).tolist()
            self.peaks_y = filtered_ecg[peaks].tolist()

            bpm = nk.ecg_rate(peaks, sampling_rate=1000)
            avg_bpm = np.mean(bpm)
            if np.isnan(avg_bpm):
                self.setWindowTitle('Waveform Plotter - BPM: --')
                return

            self.setWindowTitle(f'Waveform Plotter - BPM: {int(avg_bpm)}')

        except Exception as e:
            print(f"Peak detection error: {e}")

if __name__ == '__main__':
    print("Starting application...")

    fpga = FPGA('COM6', 115200)
    fpga.open_instrument()
    fpga.send_key(KEY)
    fpga.send_nonce(NONCE)
    fpga.send_associated_data(DA)

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