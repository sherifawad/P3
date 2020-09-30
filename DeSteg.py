import binascii

HEADER_SIZE = 54
DELIMITER = "$"

class LSBDecrypter:
    def __init__(self):
        self.StegImageFile = ''
        # self.fh = open(StegImageFile, 'rb')
        self.number_of_chars_in_text = 0
        self.original_text = ''

    def read_header(self):
        self.fh = open(StegImageFile, 'rb')
        for i in range(0, HEADER_SIZE):
            byte = self.fh.read(1)

    def get_char(self):
        new_byte = ''

        for bit in range(0, 8):
            byte = self.fh.read(1)

            new_byte += str(ord(byte) & 0x01)

        n = int(new_byte, 2)
        desteg_char = binascii.unhexlify('%x' % n)
        desteg_char = ''.join(map(chr, desteg_char))
        return desteg_char

    def get_text_size(self):
        curr_ch = self.get_char()

        s_sz = ''

        while curr_ch != DELIMITER:
            s_sz += curr_ch
            curr_ch = self.get_char()

        if (s_sz != ''):
            self.number_of_chars_in_text = int(s_sz)

    def read_stega_text(self):
        decoded_chars = 0;
        while decoded_chars < self.number_of_chars_in_text:
            self.original_text += self.get_char()
            decoded_chars += 1

    def close_file(self):
        self.fh.close();

    def get_text(self):
        self.read_header()
        self.get_text_size()
        self.read_stega_text()
        self.close_file()
        return self.original_text

    def reveal_(self, stego):
        global StegImageFile
        StegImageFile = stego
        destag_insta = LSBDecrypter()
        text = destag_insta.get_text()
        # text = open("C:/Users/Sherif/OneDrive/P3/teto.txt", "w").write(text)
        return text

# ImageFile = "C:/Users/Sherif/OneDrive/P3/steg.bmp"
# LSBDecrypter().reveal_(ImageFile)
