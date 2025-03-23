from FPGA import *
import sys
import neurokit2 as nk
import matplotlib.pyplot as plt

KEY     = bytes.fromhex("8A55114D1CB6A9A2BE263D4D7AECAAFF")
NONCE   = bytes.fromhex("4ED0EC0B98C529B7C8CDDF37BCD0284A")
DA      = b"A to B"

if __name__ == '__main__':
    print("Starting application...")
    fpga = FPGA('COM11', 115200)
    print("FPGA initialized.")
    waves = fpga.read_csv_file("waveform_example_ecg.csv")
    print("Waves loaded.")

    wave = waves[20]
    wave_encrypted = fpga.encrypt_waveform_python(wave, KEY, NONCE, DA)
    wave_decrypted = fpga.list_from_wave(fpga.decrypt_waveform_python(wave_encrypted, KEY, NONCE, DA))
    print(wave_decrypted)

    # Ensure the signal is long enough
    if len(wave_decrypted) < 10:
        print("Error: The signal is too short for processing.")
        sys.exit(1)

    try:
        # Identify PQRST parts of the ECG
        ecg_signals, info = nk.ecg_process(wave_decrypted, sampling_rate=360)
        r_peaks = info["ECG_R_Peaks"]
        p_waves = info["ECG_P_Peaks"]
        q_waves = info["ECG_Q_Peaks"]
        s_waves = info["ECG_S_Peaks"]
        t_waves = info["ECG_T_Peaks"]

        # Plot the ECG signal with PQRST points
        plt.figure(figsize=(10, 6))
        plt.plot(wave_decrypted, label='Decrypted ECG')
        plt.scatter(r_peaks, [wave_decrypted[i] for i in r_peaks], color='red', label='R-peaks')
        plt.scatter(p_waves, [wave_decrypted[i] for i in p_waves], color='blue', label='P-peaks')
        plt.scatter(q_waves, [wave_decrypted[i] for i in q_waves], color='green', label='Q-peaks')
        plt.scatter(s_waves, [wave_decrypted[i] for i in s_waves], color='yellow', label='S-peaks')
        plt.scatter(t_waves, [wave_decrypted[i] for i in t_waves], color='magenta', label='T-peaks')
        plt.legend()
        plt.title('ECG Signal with PQRST Points')
        plt.xlabel('Samples')
        plt.ylabel('Amplitude')
        plt.show()
    except Exception as e:
        print(f"Error processing ECG signal: {e}")
        sys.exit(1)