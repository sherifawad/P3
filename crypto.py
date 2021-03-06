import os
import shutil
import tempfile
import zipfile
import random
import time
import aes
import hashlib
import curves
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.factory import Factory
from kivy.core.window import Window

temp_ =  tempfile.mkdtemp()
cv = curves.Curve.get_curve('secp160r1')
p = curves.Point(0x4a96b5688ef573284664698968c38bb913cbfc82, 0x23a628553168947d59dcc912042351377ac5fb32, cv)
q = 0x100000000000000000001f4c8f927aed3ca752257
iv_c = "9B7D2C34A366BF89"
d_KGC = 773182302672421767750165305491852205951657281488
r_KGC = 1354751385705862203270732046669540660812388894970
d_c1 = 682751145430528733998785385796475295296378616137
Bank_x = "5dc45f399f852ac96b279ef7f269642edc29164e"
Bank_y = "9575c1d5c4ac6327cc06580c86c20097db357a52"
My_ID = "id_c"
d_b1 = 636094978034945902382888945383118957293951948210
client_x = "587127a78a1022e5b6ae512825dbc56aba2499bf"
client_y =  "e3b68f415f942a86d0d31e99a2d856194bc57d5c"
Receiver_ID = "id_b"

class Var_():
    def VEntry(self, Secret, X_C, Y_C, Y_ID, R_ID):
        global d_c1, Bank_x, Bank_y, My_ID, client_x, client_y, Receiver_ID, d_b1
        d_c1 = Secret.text or 682751145430528733998785385796475295296378616137
        Bank_x = X_C.text or "5dc45f399f852ac96b279ef7f269642edc29164e"
        Bank_y = Y_C.text or "9575c1d5c4ac6327cc06580c86c20097db357a52"
        My_ID = Y_ID.text or "id_c"
        d_b1 = Secret.text or 636094978034945902382888945383118957293951948210
        client_x = X_C.text or "587127a78a1022e5b6ae512825dbc56aba2499bf"
        client_y = Y_C.text or "e3b68f415f942a86d0d31e99a2d856194bc57d5c"
        Receiver_ID = R_ID.text or "id_b"

class ListView_(Screen):
    def Load(self, path):
        global a
        a = path
    def Save(self, path, text_input):
        global output_file_path
        output_file_path = os.path.join(path, text_input)
    def Image_(self, path):
        file_path = shutil.copy2(path[0], temp_)
        global image_file_path
        image_file_path = str(file_path)
    def RImage_(self, path):
        global  R_path
        R_path = os.path.join(path[0])

class SManagement(ScreenManager):
    pass

class Home_(Screen):
    pass

class Send_(Screen):
    def send_all(self):
        global d_c1, Bank_x, Bank_y, My_ID, d_c, P_c, P_b
        if type(d_c1) is int:
            d_c1 = d_c1
        else: d_c1 = int(d_c1, base=16)
        if type(Bank_x) is int:
            Bank_x = Bank_x
        else: Bank_x = int(Bank_x, base=16)
        if type(Bank_y) is int:
            Bank_y = Bank_y
        else: Bank_y = int(Bank_y, base=16)
        Bank_R = curves.Point(Bank_x, Bank_y, cv)
        P_b = Bank_R
        if type(My_ID) is bytes:
            My_ID = My_ID
        else:
            My_ID = (bytes(My_ID, 'utf-8'))
        d_c2 = (r_KGC + d_KGC * int(hashlib.sha256(My_ID).hexdigest(), 16))%q
        d_c = d_c1 * d_c2
        P_c = d_c * p
    def Exsend_(self):
        Send_().send_all()
        r_sc = 406572794028345823020817876817526759659544524999
        r_sc = (bytes(str(r_sc), 'utf-8'))
        localtime = time.asctime( time.localtime(time.time()) )
        localtime = (bytes(str(localtime), 'utf-8'))

        z_sc = hashlib.sha256()
        z_sc.update(r_sc)
        z_sc.update(localtime)
        z_sc.update(bytes(str(My_ID), 'utf-8'))
        z_sc = int(z_sc.hexdigest(), 16)
        K_2c = z_sc * p
        K_1c = (K_2c.x * d_c) * P_b
        X_K1c = (bytes(str(K_1c.x), 'utf-8'))
        Y_K2c = (bytes(str(K_2c.y), 'utf-8'))

                                                  #encryption
        key_c = X_K1c[:16] # Symmetric Key
        aese_c = aes.AESModeOfOperationOFB(key_c, iv_c)
        text = zipfile.ZipFile(temp_ + "source.zip", mode="w")
        n = len(a)
        i = 0
        while True:
            if i < len(a):
                text.write(a[i])
                i += 1
            else:
                break
        text.close()
        text = open(temp_ + "source.zip", "rb")
        text = text.read()
        h_c = hashlib.sha256()
        h_c.update(text)
        h_c.update(Y_K2c)
        h_c = int(h_c.hexdigest(), 16)
        C = aese_c.encrypt(text)

        S = (z_sc - (h_c * d_c))%q
        R = h_c * P_c

        Dict = {'s':S, 'r':str(R), 'c':C}

        f = open(output_file_path + ".txt", "w")
        f.write(str(Dict))
        f.close()
        print(temp_)
        shutil.rmtree(temp_, ignore_errors=True)

class Receive_(Screen):
    def receive_all(self):
        global d_b1, client_x, client_y, Receiver_ID, d_b, P_c, P_b
        if type(d_b1) is int:
            d_b1 = d_b1
        else: d_b1 = int(d_b1, base=16)
        if type(client_x) is int:
            client_x = client_x
        else: client_x = int(client_x, base=16)
        if type(client_y) is int:
            client_y = client_y
        else: client_y = int(client_y, base=16)
        Client_R = curves.Point(client_x, client_y, cv)
        P_c = Client_R
        if type(Receiver_ID) is bytes:
            Receiver_ID = Receiver_ID
        else:
            Receiver_ID = (bytes(Receiver_ID, 'utf-8'))
        d_b2 = (r_KGC + d_KGC * int(hashlib.sha256(Receiver_ID).hexdigest(), 16))%q
        d_b = d_b1 * d_b2
        P_b = d_b * p
    def Exreceive_(self):

        Receive_().receive_all()

        f = open(R_path, "r")
        my_dict = eval(f.read())

        R = my_dict['r']
        S = my_dict['s']
        Cr = my_dict['c']
        f.close()
        print(temp_)
        shutil.rmtree(temp_, ignore_errors=True)
        R = R.split()
        r_x = int(R[1], base=16)
        r_y = int(R[3], base=16)
        R = curves.Point(r_x, r_y, cv)
                                                    # Bank
        K_2b = (S * p) + R
        Y_K2b = (bytes(str(K_2b.y), 'utf-8'))

        K_1b = (K_2b.x * d_b) * P_c
        X_K1b = (bytes(str(K_1b.x), 'utf-8'))
        key_b = X_K1b[:16] # Symmetric Key
        iv_b = "9B7D2C34A366BF89"
        aesd_b = aes.AESModeOfOperationOFB(key_b, iv_b)
        decrypted_b = aesd_b.decrypt(Cr)
        plaintext = open(output_file_path + ".zip", "wb")
        plaintext.write(decrypted_b)
        plaintext.close()
        plaintext = open(output_file_path + ".zip", "rb")
        plaintext = plaintext.read()

        h_b =hashlib.sha256()
        h_b.update(plaintext)
        h_b.update(Y_K2b)
        h_b = int(h_b.hexdigest(), 16)
        R_b = h_b * P_c

        if R == R_b :
            Factory.RWin().open()
        else:
            Factory.RDefeat().open()

class output():
    def CustKey(self):
        return P_c

presentation = Builder.load_file("crypto.kv")

class MainApp(App):
    ListView_ = ListView_()
    Var_ = Var_()
    Send_ = Send_()
    output =output()
    def build(self):
        Window.clearcolor = (0.8823529411764706, 0.8470588235294118, 0.7254901960784313, 1)
        return presentation

if __name__ == '__main__':
    MainApp().run()
