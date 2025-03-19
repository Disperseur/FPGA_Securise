# # Affichage ecg avec ascon python
# from FPGA import *
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# import pyqtgraph as pg
# from pyqtgraph.Qt import QtCore

# KEY     = bytes.fromhex("8A55114D1CB6A9A2BE263D4D7AECAAFF")
# NONCE   = bytes.fromhex("4ED0EC0B98C529B7C8CDDF37BCD0284A")
# DA      = b"A to B"

# class PlotWindow(QMainWindow):
#     def __init__(self, waves, parent=None):
#         super(PlotWindow, self).__init__(parent)
#         self.waves = waves
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle('Waveform Plotter')
#         self.setGeometry(100, 100, 800, 600)
        
#         self.main_widget = QWidget(self)
#         self.setCentralWidget(self.main_widget)
        
#         layout = QVBoxLayout(self.main_widget)
        
#         self.plot_widget = pg.PlotWidget()
#         layout.addWidget(self.plot_widget)
        
#         self.plot_widget.addLegend()
#         self.plot_widget.showGrid(x=True, y=True)
        
#         self.curve_decrypted = self.plot_widget.plot(pen='g', name='Decrypted')
        
#         self.ptr = 0
#         self.decrypted_data = []
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.update_plot)
#         self.timer.start(100)  # Update every 100 ms

#     def update_plot(self):
#         if self.ptr < len(self.waves):
#             wave = self.waves[self.ptr]
#             wave_encrypted = fpga.encrypt_waveform_python(wave, KEY, NONCE, DA)
#             wave_decrypted = fpga.decrypt_waveform_python(wave_encrypted, KEY, NONCE, DA)
            
#             self.decrypted_data.extend(fpga.list_from_wave(wave_decrypted))
#             self.curve_decrypted.setData(self.decrypted_data)
            
#             # Set x-axis range to keep 4 waves on the screen
#             wave_length = len(wave)
#             self.plot_widget.setXRange(max(0, len(self.decrypted_data) - 1 * wave_length), len(self.decrypted_data))
            
#             self.ptr += 1

# if __name__ == '__main__':
#     print("Starting application...")
#     fpga = FPGA('COM11', 115200)
#     print("FPGA initialized.")
#     waves = fpga.read_csv_file("waveform_example_ecg.csv")
#     print("Waves loaded.")

#     app = QApplication(sys.argv)
#     print("QApplication created.")
#     mainWin = PlotWindow(waves)
#     print("PlotWindow created.")
#     mainWin.show()
#     print("PlotWindow shown.")
#     sys.exit(app.exec_())



# affichage ecg avec ascon fpga
from FPGA import *

KEY =   bytes.fromhex('4C8A55114D1CB6A9A2BE263D4D7AECAAFF')
NONCE = bytes.fromhex('4F4ED0EC0B98C529B7C8CDDF37BCD0284A')
DA =    bytes.fromhex('424120746F20428000')
WAVE =  bytes.fromhex('585A5B5B5A5A5A5A5A59554E4A4C4F545553515354565758575A5A595756595B5A5554545252504F4F4C4C4D4D4A49444447474644424341403B36383E4449494747464644434243454745444546474A494745484F58697C92AECEEDFFFFE3B47C471600041729363C3F3E40414141403F3F403F3E3B3A3B3E3D3E3C393C41464646454447464A4C4F4C505555524F5155595C5A595A5C5C5B5959575351504F4F53575A5C5A5B5D5E6060615F605F5E5A5857545252800000')


fpga = FPGA('COM4', 115200)
fpga.open_instrument()
fpga.send_key(KEY)
fpga.send_nonce(NONCE)
fpga.send_associated_data(DA)
fpga.send_waveform(WAVE)
fpga.start_encryption()
cipher = fpga.get_cipher()
tag = fpga.get_tag()
fpga.close_instrument()

plain = fpga.decrypt_waveform_python(cipher[:-3]+tag, KEY[1:], NONCE[1:], DA[1:-2])
print(plain == WAVE[1:-3])
