#Communication with the FPGA

import serial
import datetime as dt
import ascon_pcsn
import matplotlib.pyplot as plt


FPGA_ACK = b'OK\n'
GO =    bytes.fromhex('48')
TAG =   bytes.fromhex('55')
CIPHER =bytes.fromhex('44')

class FPGA:
    def __init__(self, port, baudrate):
        """
        Initializes the FPGA class with the specified serial port and baud rate.
        
        :param port: Serial port to connect to the FPGA.
        :param baudrate: Baud rate for the serial communication.
        """
        self.port = port
        self.baudrate = baudrate
        self.log = open("log.txt", "a")

    def open_instrument(self):
        """
        Opens the connection to the FPGA.
        
        :return: 0 if successful, -1 otherwise.
        """
        try:
            self.port = serial.Serial(self.port, self.baudrate)
            self.log.write("\n" + str(dt.datetime.now()) + " - FPGA opened\n")
            return 0
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not open the FPGA\n")
            raise AssertionError("Error: Could not open the FPGA")
            return -1

    def send_key(self, key):
        """
        Sends the key to the FPGA.
        
        :param key: Key to send to the FPGA.
        :return: None
        """
        try:
            self.port.write(key)
            self.log.write(str(dt.datetime.now()) + " - Key sent\n")
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not send the key\n")
            raise AssertionError("Error: Could not send the key")
            return -1

        try:
            flag = self.port.read(3)
            if flag != FPGA_ACK:
                self.log.write(str(dt.datetime.now()) + " - Error: FPGA not ready\n")
                raise AssertionError("Error: FPGA not ready")
                return -1
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not read the FPGA\n")
            raise AssertionError("Error: Could not read the FPGA")
            return -1
        
    def send_nonce(self, nonce):
        """
        Sends the nonce to the FPGA.
        
        :param nonce: Nonce to send to the FPGA.
        :return: None
        """
        try:
            self.port.write(nonce)
            self.log.write(str(dt.datetime.now()) + " - Nonce sent\n")
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not send the nonce\n")
            raise AssertionError("Error: Could not send the nonce")
            return -1

        try:
            flag = self.port.read(3)
            if flag != FPGA_ACK:
                self.log.write(str(dt.datetime.now()) + " - Error: FPGA not ready\n")
                raise AssertionError("Error: FPGA not ready")
                return -1
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not read the FPGA\n")
            raise AssertionError("Error: Could not read the FPGA")
            return -1
        
    def send_associated_data(self, associated_data):
        """
        Sends the associated data to the FPGA.
        
        :param associated_data: Associated data to send to the FPGA.
        :return: None
        """
        try:
            self.port.write(associated_data)
            self.log.write(str(dt.datetime.now()) + " - Associated data sent\n")
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not send the associated data\n")
            raise AssertionError("Error: Could not send the associated data")
            return -1

        try:
            flag = self.port.read(3)
            if flag != FPGA_ACK:
                self.log.write(str(dt.datetime.now()) + " - Error: FPGA not ready\n")
                raise AssertionError("Error: FPGA not ready")
                return -1
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not read the FPGA\n")
            raise AssertionError("Error: Could not read the FPGA")
            return -1
        
    def send_waveform(self, wave):
        """
        Sends the waveform to the FPGA.
        
        :param wave: Waveform to send to the FPGA.
        :return: None
        """
        try:
            self.port.write(wave)
            self.log.write(str(dt.datetime.now()) + " - Waveform sent\n")
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not send the waveform\n")
            raise AssertionError("Error: Could not send the waveform")
            return -1

        try:
            flag = self.port.read(3)
            if flag != FPGA_ACK:
                self.log.write(str(dt.datetime.now()) + " - Error: FPGA not ready\n")
                raise AssertionError("Error: FPGA not ready")
                return -1
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not read the FPGA\n")
            raise AssertionError("Error: Could not read the FPGA")
            return -1
        
    def start_encryption(self):
        """
        Starts the encryption on the FPGA.
        
        :return: None
        """
        try:
            self.port.write(GO)
            self.log.write(str(dt.datetime.now()) + " - Encryption started\n")
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not start the encryption\n")
            raise AssertionError("Error: Could not start the encryption")
            return -1

        try:
            flag = self.port.read(3)
            if flag != FPGA_ACK:
                self.log.write(str(dt.datetime.now()) + " - Error: FPGA not ready\n")
                raise AssertionError("Error: FPGA not ready")
                return -1
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not read the FPGA\n")
            raise AssertionError("Error: Could not read the FPGA")
            return -1
        
    def get_cipher(self):
        """
        Gets the cipher from the FPGA.
        
        :return: Cipher received from the FPGA.
        """
        try:
            self.port.write(CIPHER)
            cipher = self.port.read(184)
            self.log.write(str(dt.datetime.now()) + " - Cipher received\n")
            self.port.read(3) # To read the FPGA_ACK
            return cipher
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not get the cipher\n")
            raise AssertionError("Error: Could not get the cipher")
            return -1
    
    def get_tag(self):
        """
        Gets the tag from the FPGA.
        
        :return: Tag received from the FPGA.
        """
        try:
            self.port.write(TAG)
            tag = self.port.read(16)
            self.log.write(str(dt.datetime.now()) + " - Tag received\n")
            self.port.read(3) # To read the FPGA_ACK
            return tag
        except:
            self.log.write(str(dt.datetime.now()) + " - Error: Could not get the tag\n")
            raise AssertionError("Error: Could not get the tag")
            return -1
    


    # def set_memory_addr(self, addr=0x00):
    #     """
    #     Sets the memory address on the FPGA.
        
    #     :param addr: Memory address to set (default is 0x00).
    #     :return: None
    #     """
    #     addr_send = bytes(f'{addr:02X}', 'utf-8')

    #     if len(addr_send) != 2:
    #         raise AssertionError("Error: address must be a 2-digit hexadecimal number")

    #     if not (addr_send[0] in b'0123456789ABCDEFabcdef' and addr_send[1] in b'0123456789ABCDEFabcdef'):
    #         raise AssertionError("Error: address must be a 2-digit hexadecimal number")

    #     try:
    #         self.port.write(b'A' + addr_send)
    #         self.log.write(str(dt.datetime.now()) + " - Memory address set to " + str(addr_send) + "\n")
    #     except:
    #         self.log.write(str(dt.datetime.now()) + " - Error: Could not set the memory address\n")
    #         raise AssertionError("Error: Could not set the memory address")
    #         return -1

    #     try:
    #         flag = self.port.read(4)
    #         if flag != FPGA_ACK:
    #             self.log.write(str(dt.datetime.now()) + " - Error: FPGA not ready\n")
    #             raise AssertionError("Error: FPGA not ready")
    #             return -1
    #     except:
    #         self.log.write(str(dt.datetime.now()) + " - Error: Could not read the FPGA\n")
    #         raise AssertionError("Error: Could not read the FPGA")
    #         return -1

    # def write_val_mem(self, val=0x00):
    #     """
    #     Writes a value to the memory at the current address.
        
    #     :param val: Value to write to memory (default is 0x00).
    #     :return: None
    #     """
    #     val_send = bytes(f'{val:02X}', 'utf-8')

    #     if len(val_send) != 2:
    #         raise AssertionError("Error: value must be a 2-digit hexadecimal number")

    #     if not (val_send[0] in b'0123456789ABCDEFabcdef' and val_send[1] in b'0123456789ABCDEFabcdef'):
    #         raise AssertionError("Error: value must be a 2-digit hexadecimal number")

    #     try:
    #         self.port.write(b'W' + val_send)
    #         self.log.write(str(dt.datetime.now()) + " - Memory value set to " + str(val_send) + "\n")
    #     except:
    #         self.log.write(str(dt.datetime.now()) + " - Error: Could not set the memory value\n")
    #         raise AssertionError("Error: Could not set the memory value")
    #         return -1

    #     try:
    #         flag = self.port.read(4)
    #         if flag != FPGA_ACK:
    #             self.log.write(str(dt.datetime.now()) + " - Error: FPGA not ready\n")
    #             raise AssertionError("Error: FPGA not ready")
    #             return -1
    #     except:
    #         self.log.write(str(dt.datetime.now()) + " - Error: Could not read the FPGA\n")
    #         raise AssertionError("Error: Could not read the FPGA")
    #         return -1

    # def display_mem_vals_leds(self):
    #     """
    #     Displays the memory values on the FPGA's LEDs.
        
    #     :return: None
    #     """
    #     try:
    #         self.port.write(b'G')
    #         self.log.write(str(dt.datetime.now()) + " - Memory values displayed on the LEDs\n")
    #     except:
    #         self.log.write(str(dt.datetime.now()) + " - Error: Could not display memory values on the LEDs\n")
    #         raise AssertionError("Error: Could not display memory values on the LEDs")
    #         return -1

    #     try:
    #         flag = self.port.read(4)
    #         if flag != FPGA_ACK:
    #             self.log.write(str(dt.datetime.now()) + " - Error: FPGA not ready\n")
    #             raise AssertionError("Error: FPGA not ready")
    #             return -1
    #     except:
    #         self.log.write(str(dt.datetime.now()) + " - Error: Could not read the FPGA\n")
    #         raise AssertionError("Error: Could not read the FPGA")
    #         return -1

    # def read_mem_val(self):
    #     """
    #     Reads the value from the memory at the current address.
        
    #     :return: Value read from memory, or -1 if an error occurs.
    #     """
    #     try:
    #         self.port.write(b'R')
    #         self.log.write(str(dt.datetime.now()) + " - Memory value asked\n")
    #     except:
    #         self.log.write(str(dt.datetime.now()) + " - Error: Could not ask the memory value\n")
    #         raise AssertionError("Error: Could not ask the memory value")
    #         return -1

    #     try:
    #         value =self.port.read(5)[1]
    #         self.log.write(str(dt.datetime.now()) + " - Memory value read: " + str(value) + "\n")
    #         return value
    #     except:
    #         self.log.write(str(dt.datetime.now()) + " - Error: Could not read the memory value\n")
    #         raise AssertionError("Error: Could not read the memory value")
    #         return -1

    def close_instrument(self):
        """
        Closes the connection to the FPGA.
        
        :return: 0 if successful, -1 otherwise.
        """
        try:
            self.port.close()
            self.log.write(str(dt.datetime.now()) + " - FPGA closed\n")
            self.log.close()
            return 0
        except:
            print("Error: Could not close the FPGA")
            self.log.write(str(dt.datetime.now()) + " - Error: Could not close the FPGA\n")
            self.log.close()
            return -1

        


    def read_csv_file(self, filename):
        """
        Opens a file containing a list of ECGs in hex format.

        :param filename: string of filename
        :return: a list of the ECGs in int format.
        """
        file = open(filename, 'r')

        waveforms = file.read().split("\n")
        waveforms = [wave.encode('utf-8') for wave in waveforms]

        file.close()

        return waveforms


    def encrypt_waveform_python(self, wave, key, nonce, associated_data):
        """
        Encrypts a ECG (called wave) in hex bytestring with ASCON128 algorythm using the key, nonce and associate_data.

        :return: a hex bytestring of the cipher text and tag at the end.
        """
        return ascon_pcsn.ascon_encrypt(key, nonce, associated_data, wave)

    def decrypt_waveform_python(self, wave, key, nonce, associated_data):
        """
        Decrypts a ECG (called wave) in hex bytestring with ASCON128 algorythm using the key, nonce and associate_data.

        :return: a hex bytestring of the plain text.
        """
        return ascon_pcsn.ascon_decrypt(key, nonce, associated_data, wave)

    def list_from_wave(self, wave):
        """
        Converts a ECG (wave) in hex bytestring into a list of int values.

        :return: a list of int corresponding to the values of the ECG (wave).
        """

        y = []
        for i in range(0, len(wave)-1, 2):
            y.append(int(wave[i:i+2], 16))
            # print(int(wave[i:i+2], 16))
        return y