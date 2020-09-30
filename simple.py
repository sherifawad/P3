import sys
marker = 'iddqd'
# marker = marker.encode("utf-8")
import os

class HideException(Exception):
    """Базовый класс для ошибок в модуле «скрыватель»."""
    pass


class UsageException(HideException):
    """Класс для ошибок использования утилиты."""

    def __str__(self):
        return self.message + '\nUsage: hide.py [bmp image] [any file]'


def bin(s):
    """Переводит число в двоичную систему счисления.
    Результат в виде битовой строки.
    """
    return str(s) if s <= 1 else bin(s >> 1) + str(s & 1)


def byte2bin(bytes):
    """Поставляет байты в виде битовых строк.
    Преобразует символ в число.
    Переводит число в двоичную систему с дополнением нулей.
    """
    for b in bytes:
        yield bin(ord(b)).zfill(8)


def hide(bmp_filename, src_filename):
    """Помещает в BMP изображение любой файл, включая его название.
    У пикселей (байтов) в изображении меняет младшие биты на те,
    что содержатся в потоке бит скрываемого файла.
    Для определения в BMP секретных данных ставятся метки.
    """
    src = open(src_filename, 'rb')
    # src_filename = src_filename.encode("utf-8")

    text =''.join(map(chr, open(src_filename, 'rb').read()))
    secret = marker + src_filename + marker + text + marker
    src.close()

    bmp = open("steg.bmp", 'rb+')
    bmp.seek(55)
    # print(bmp.read())
    container = ''.join(map(chr, bmp.read()))
    # container = bmp.read()

    need = 8 * len(secret) - len(container)
    if need > 0:
        raise HideException('BMP size is not sufficient for confidential file.'
                            '\nNeed another %s byte.' % need)
    cbits = byte2bin(container)
    encrypted = []
    # print(secret)
    for sbits in byte2bin(secret):
        for bit in sbits:
            bits = cbits.__next__()
            # Замена младшего бита в контейнерном байте
            bits = bits[:-1] + bit
            b = chr(int(bits, 2))
            # Замена байта в контейнере
            encrypted.append(b)

    bmp.seek(55)
    # print(encrypted)
    # encrypted = bytearray(map(ord, encrypted))
    # print(encrypted)
    # encrypted = bytearray(h.decode("hex") for h in encrypted)
    # encrypted = bytearray(map(int(encrypted, 16) ))
    # bmp.write(''.join(encrypted))
    bmp.write(bytearray(map(ord, encrypted)))
    bmp.close()



bmp_filename = "C:/Users/Sherif/OneDrive/Pyhton_Projects/P3/target.png"
src_filename = "C:/Users/Sherif/OneDrive/Pyhton_Projects/P3/long.txt"

hide(bmp_filename, src_filename)











































# from binascii import hexlify
# def char_to_bin(string):
#     bin_string = [bin(ord(char))[2:].zfill(8) for char in string]
#     # Qty of bits for removal purposes pos:1
#     bin_string.insert(0, bin((len(bin_string)) * 8)[2:].zfill(8))
#
#     # length of bits length number
#     fill = len(bin_string[0])
#     length = len(bin_string[0][2:].zfill(fill))
#     bin_string.insert(0, bin(length)[2:].zfill(8))
#     return bin_string
#
#
# # Only works for the image being inserted
# def ascii_to_bin(data):
#     bin_data = []
#     width = bin(int(data[0]))[2:].zfill(16)
#     height = bin(int(data[1]))[2:].zfill(16)
#
#     for elem in range(2, len(data)):
#         bin_data.append(bin(int(data[elem]))[2:].zfill(8))
#
#     # Number of bits to be inserted for removal purposes
#     bin_data.insert(0, bin((len(bin_data) * 8))[2:].zfill(22))
#     print((len(bin_data) * 8))
#
#     # Insert dimensions
#     bin_data.insert(0, height)
#     bin_data.insert(0, width)
#
#     return bin_data
#
#
# def hide_message(message, image):
#     bin_msg = char_to_bin(message)
#
#     # Number of bits to be inserted
#     bits = int(bin_msg[1], 2)
#
#     try:
#         with open(image, 'r') as f:
#             header = f.readlines()[0:3]
#             f.seek(0)
#             data = [y for x in f.readlines()[3:] for y in x.replace("\n", "").split(" ") if y != ""]
#         with open(image, 'rb') as f:
#             header = f.readlines()[0:3]
#             f.seek(0)
#     except FileNotFoundError as e:
#         print(e.strerror)
#     else:
#         # f = open(image, 'rb')
#         # f = bytearray(map(ord, x))
#
#         bin_data = [bin(int(x))[2:].zfill(8) for x in data]
#
#         # bin_data = [bin(int(x, 16))[2:].zfill(8) for x in data]
#
#         if len(bin_data) < bits:
#             raise ValueError()
#
#         # Inserting Message with LSB technique
#         y = 0
#         for x in "".join(bin_msg):
#             while y < (len(bin_data)):
#                 bin_data[y] = bin_data[y][0:len(bin_data[y])-1] + x
#                 y += 1
#                 break
#
#         # binary to ascii
#         for x in range(len(bin_data)):
#             data[x] = str(int(bin_data[x], 2)) + "\n"
#
#         with open("stego_" + image, 'w') as f:
#             f.write(''.join(header) + ''.join(data))
#
#
# def retrieve_message(image):
#
#     try:
#         with open(image, 'r') as f:
#             header = f.readlines()[0:3]
#             f.seek(0)
#             data = [y for x in f.readlines()[3:] for y in x.replace("\n", "").split(" ") if y != ""]
#     except FileNotFoundError as e:
#         print(e.strerror)
#     else:
#
#         # ascii to binary
#         bin_data = [bin(int(x))[2:].zfill(8) for x in data]
#
#         # Retrieve length of ??Qty of bits??
#         bit_length = ""
#         for x in range(8):
#             bit_length += bin_data[x][-1]
#
#         message_length = ""
#         # Retrieve Message Length (Bits Qty)
#         for x in range(8, 8 + int(bit_length, 2)):
#             message_length += bin_data[x][-1]
#
#         bin_msg = []
#         # Retrieve Message
#         ctr = 0
#         acc = ""
#         x = 8 + int(bit_length, 2)
#         y = x + int(message_length, 2)
#
#         while x < y:
#             if ctr < 8:
#                 acc += bin_data[x][-1]
#                 ctr += 1
#                 x += 1
#             else:
#                 bin_msg.append(acc)
#                 acc = ""
#                 ctr = 0
#         bin_msg.append(acc)
#
#         message = ""
#         for x in bin_msg:
#             message += chr(int(x, 2))
#
#         return message
#
#
# def hide_image(secret, carrier):
#
#     try:
#         with open(secret, "r") as a, open(carrier, "r") as b:
#
#             secret_data = [y for x in a.readlines()[1:] for y in x.replace("\n", "").split(" ") if y != ""]
#
#             carrier_header = b.readlines()[0:3]
#             b.seek(0)
#             carrier_data = [y for x in b.readlines()[3:] for y in x.replace("\n", "").split(" ") if y != ""]
#
#     except FileNotFoundError:
#         print(FileNotFoundError.strerror)
#     else:
#
#         bin_carrier_data = [bin(int(x))[2:].zfill(8) for x in carrier_data]
#         bin_secret_data = "".join(ascii_to_bin(secret_data))
#
#         if len(bin_secret_data) > len(bin_carrier_data):
#             raise ValueError()
#
#         # Insert image into carrier
#         y = 0
#         bit_pos = 1
#         for x in bin_secret_data:
#             if y < len(bin_carrier_data):
#                 if bit_pos > 1:
#                     bin_carrier_data[y] = bin_carrier_data[y][0:len(bin_carrier_data[y]) - bit_pos] + \
#                                           x + \
#                                           bin_carrier_data[y][-bit_pos + 1:]
#                     y += 1
#                 else:
#                     bin_carrier_data[y] = bin_carrier_data[y][0:len(bin_carrier_data[y]) - bit_pos] + x
#                     y += 1
#             else:
#                 y = 0
#                 bit_pos += 1
#                 bin_carrier_data[y] = bin_carrier_data[y][0:len(bin_carrier_data[y]) - bit_pos] + x + bin_carrier_data[y][-bit_pos + 1:]
#                 y += 1
#
#         for x in range(len(bin_carrier_data)):
#             carrier_data[x] = str(int(bin_carrier_data[x], 2))
#
#         with open('steg_' + carrier, 'w') as f:
#             f.write("".join(carrier_header) + "\n".join(carrier_data))
#
#
# def retrieve_image(image):
#
#     try:
#         with open(image, 'r') as f:
#
#             header_bin = [bin(int(y))[2:].zfill(16) for x in f.readlines()[3:35] for y in x.replace("\n", "").split(" ") if y != ""]
#             f.seek(0)
#             l = [bin(int(y))[2:].zfill(16) for x in f.readlines()[35:57] for y in x.replace("\n", "").split(" ") if y != ""]
#             f.seek(0)
#             data_bin = [bin(int(y))[2:].zfill(16) for x in f.readlines()[57:] for y in x.replace("\n", "").split(" ") if y != ""]
#
#     except FileNotFoundError:
#         print(FileNotFoundError.strerror)
#     else:
#
#         # Extract header
#         h = ''
#         for x in range(32):
#             h += header_bin[x][-1]
#
#         header = _magic_number + "\n" + str(int(h[0:16], 2)) + " " + str(int(h[16:33], 2)) + "\n"
#
#         #Extract data
#         message_length = ''
#         for x in range(len(l)):
#             message_length += l[x][-1]
#
#         message_length = int(message_length, 2)
#
#         d = ''
#         y = 0
#         bit_pos = -1
#         for x in range(message_length):
#             if y < len(data_bin):
#                 d += data_bin[y][bit_pos]
#                 y += 1
#             else:
#                 y = 0
#                 bit_pos -= 1
#                 d += data_bin[y][bit_pos]
#                 y += 1
#
#         data = []
#         acc = ''
#         y = 0
#         for x in d:
#             if y < 8:
#                 acc += x
#                 y += 1
#             else:
#                 data.append(str(int(acc, 2)))
#                 y = 0
#                 acc = ''
#                 acc += x
#                 y += 1
#
#         data.append(str(int(acc, 2)))
#         data.append("")
#
#         with open("ret_image.ppm", 'w') as f:
#             f.write("".join(header) + "\n".join(data))
#
# secret = ("sec.txt")
# carrier = ("chris.png")
# hide_message(secret, carrier)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # import png
# # import stepic
# # from PIL import Image
# # import cv2
# # data = open("C:/Users/Sherif/OneDrive/P3/sec.txt", "rb").read()
# # image = "C:/target.png"
# # StegImageFile = "C:/Users/Sherif/OneDrive/P3/zozo.bmp"
# # import Cimp
# #
# # png_Reader = png.Reader(image)
# # # png_reader = png.reader(image)
# # png_width, png_height, png_pixels, png_meta = png_Reader.read_flat()
# # png_size = png_width * png_height
# # # im = stepic.encode(im, TextToHide)
# # # print (png_size)
# # im = Image.open(image)
# # # print(list(im.getdata()))
# # print(png_Reader.asRGB8())
# # # get = list(png_pixels)
# # def encode_imdata(imdata, data):
# #     '''given a sequence of pixels, returns an iterator of pixels with
# #     encoded data'''
# #
# #     datalen = len(data)
# #     if datalen == 0:
# #         raise ValueError('data is empty')
# #     if datalen * 3 > len(imdata):
# #         raise ValueError('data is too large for image')
# #
# #     imdata = iter(imdata)
# #
# #     for i in range(datalen):
# #         pixels = [value & ~1 for value in
# #                   next(imdata)[:3] + next(imdata)[:3] + next(imdata)[:3]]
# #         byte = ord(data[i])
# #         for j in range(7, -1, -1):
# #             pixels[j] |= byte & 1
# #             byte >>= 1
# #         if i == datalen - 1:
# #             pixels[-1] |= 1
# #         pixels = tuple(pixels)
# #         yield pixels[0:3]
# #         yield pixels[3:6]
# #         yield pixels[6:9]
# #
# #
# # def encode_inplace(image, data):
# #     '''hides data in an image'''
# #
# #     w = png_pixels[0]
# #     (x, y) = (0, 0)
# #     for pixel in encode_imdata(get, data):
# #         image.putpixel((x, y), pixel)
# #         if x == w - 1:
# #             x = 0
# #             y += 1
# #         else:
# #             x += 1
# #
# #
# # def encode(image, data):
# #     '''generates an image with hidden data, starting with an existing
# #     image and arbitrary data'''
# #
# #     # image = image.copy()
# #     encode_inplace(image, data)
# #     return image
#
# # encode(image, data)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#  # Consts
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # HEADER_SIZE = 900
# # DELIMITER = "$"
# #
# # class LSBEncrypter(object):
# #     def __init__(self):
# #         self.image_byte_counter = 0
# #         self.new_image_data = ''
# #         self.original_image = ''
# #         self.text_to_hide = ''
# #
# #     def open_image(self):
# #         with open(ImageFile, "rb") as f:
# #             self.original_image = ''.join(map(chr, f.read()))
# #     def read_header(self):
# #         for x in range(0, HEADER_SIZE):
# #             self.new_image_data += self.original_image[x]
# #             self.image_byte_counter += 1
# #     def hide_text_size(self):
# #         sz = len(self.text_to_hide)
# #         s_sz = str(sz)
# #         s_sz += DELIMITER
# #         self.do_steg(s_sz)
# #
# #     def do_steg(self, steg_text):
# #
# #         for ch in range(0, len(steg_text)):
# #
# #             current_char = steg_text[ch]
# #             current_char_binary = '{0:08b}'.format(ord(current_char))
# #
# #             for bit in range(0, len(current_char_binary)):
# #                 new_byte_binary = ''
# #
# #                 current_image_binary = '{0:08b}'.format(ord(self.original_image[self.image_byte_counter]))
# #
# #                 new_byte_binary = current_image_binary[:7]
# #
# #                 new_byte_binary += current_char_binary[bit]
# #
# #                 new_byte = chr(int(new_byte_binary, 2))
# #
# #                 self.new_image_data += new_byte
# #                 self.image_byte_counter += 1
# #     def copy_rest(self):
# #
# #         self.new_image_data += self.original_image[self.image_byte_counter:]
# #         # print(self.new_image_data)
# #     def close_file(self):
# #         with open(StegImageFile, "wb") as out:
# #             out.write(bytearray(map(ord, self.new_image_data)))
# #
# #     def run(self, stega_text):
# #         self.text_to_hide = stega_text
# #         self.open_image()
# #         self.read_header()
# #         self.hide_text_size()
# #         self.do_steg(self.text_to_hide)
# #         self.copy_rest()
# #         self.close_file()
# #
# #     def hide_(self, Texte, image, steg):
# #         global TextToHide, ImageFile, StegImageFile
# #         TextToHide = Texte
# #         ImageFile = image
# #         StegImageFile = steg
# #         stega_instance = LSBEncrypter()
# #         stega_instance.run(TextToHide)
# #
# # TextToHide = open("C:/Users/Sherif/OneDrive/P3/sec.txt", "r").read()
# # ImageFile = "C:/Users/Sherif/OneDrive/P3/FW.bmp"
# # StegImageFile = "C:/Users/Sherif/OneDrive/P3/zozo.bmp"
# #
# # LSBEncrypter().hide_(TextToHide, ImageFile, StegImageFile)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # ImageFile = "C:/Users/Sherif/OneDrive/P3/FW.bmp"
# # TextToHide = open("C:/Users/Sherif/OneDrive/P3/sec.txt", "r").read()
# # StegImageFile = "C:/Users/Sherif/OneDrive/P3/hidden_cat.bmp"
# #
# #
# # import EnSteg
# # EnSteg.main()
#
#
#
# # x = 5
# # b = 6
# # class addition():
# #    def process(self):
# #       c = x + b
# #       print (c)
# # # def main():
# # #
# # #     addition().process()
# # #     print (c)
# # #
# # # if __name__ == '__main__':
# # #     main()
# #
# # addition().process()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # __author__ = 'omrih'
# # import binascii
# #
# # # Consts
# # HEADER_SIZE = 54 # Header size of BMP
# # DELIMITER = "$" # Separator between number of characters and text
# #
# # # User Configurations
# # StegImageFile = "C:/Users/Sherif/OneDrive/P3/hidden_cat.bmp"
# #
# # class LSBDecrypter:
# #     def __init__(self):
# #         self.fh = open(StegImageFile, 'rb')
# #         self.number_of_chars_in_text = 0
# #         self.original_text = ''
# #
# #     def read_header(self):
# #         # Reading Header - text is not encoded in it
# #         for i in range(0, HEADER_SIZE):
# #             byte = self.fh.read(1)
# #
# #     # Takes the LSB of the next 8 bytes and assemble a byte from them,
# #     # Returns the ASCII representation of the byte created
# #     def get_char(self):
# #         new_byte = ''
# #
# #         # get lsb of next 8 bytes
# #         for bit in range(0, 8):
# #             byte = self.fh.read(1)
# #
# #             # Taking only the LSB
# #             new_byte += str(ord(byte) & 0x01)
# #
# #         # Converting binary value to ASCII
# #         n = int(new_byte, 2)
# #         desteg_char = binascii.unhexlify('%x' % n)
# #         desteg_char = ''.join(map(chr, desteg_char))
# #         return desteg_char
# #
# #     # Gets the length of the hidden text,
# #     # It was inserted before the delimiter
# #     def get_text_size(self):
# #         curr_ch = self.get_char()
# #
# #         s_sz = ''
# #
# #         # loop while we haven't reached the separator
# #         while curr_ch != DELIMITER:
# #             s_sz += curr_ch
# #             curr_ch = self.get_char()
# #
# #         if (s_sz != ''):
# #             self.number_of_chars_in_text = int(s_sz)
# #
# #     # Reads the entire text hidden in the image
# #     def read_stega_text(self):
# #         decoded_chars = 0;
# #         while decoded_chars < self.number_of_chars_in_text:
# #             self.original_text += self.get_char()
# #             decoded_chars += 1
# #
# #     def close_file(self):
# #         self.fh.close();
# #
# #     def get_text(self):
# #         self.read_header()
# #         self.get_text_size()
# #         self.read_stega_text()
# #         self.close_file()
# #         return self.original_text
# #
# # def main():
# #     destag_insta = LSBDecrypter()
# #     text = destag_insta.get_text()
# #     text = open("C:/Users/Sherif/OneDrive/P3/teto.txt", "w").write(text)
# #     print ("Successfully decoded")
# #
# # if __name__ == '__main__':
# #     main()
# #
# # main()
#
#
#
#
#
#
#
#
#
#
#
#
#
# #  # Consts
# # HEADER_SIZE = 54 # Header size of BMP
# # DELIMITER = "$" # Separator between number of characters and text
# #
# # # User Configurations
# # TextToHide = open("C:/Users/Sherif/OneDrive/P3/sec.txt", "r").read()
# #
# # # TextToHide = "I Am Secret Information!"
# # ImageFile = "C:/Users/Sherif/OneDrive/P3/FW.bmp"
# # StegImageFile = "C:/Users/Sherif/OneDrive/P3/hidden_cat.bmp"
# #
# # class LSBEncrypter(object):
# #
# #     def __init__(self):
# #         self.image_byte_counter = 0
# #         self.new_image_data = ''
# #         self.original_image = ''
# #         self.text_to_hide = ''
# #
# #     def open_image(self):
# #          # Open the image file
# #         with open(ImageFile, "rb") as f:
# #             # self.original_image = f.read()
# #             self.original_image = ''.join(map(chr, f.read()))
# #         # print(type(self.original_image))
# #      # Reading first chunk of the file - we don't want to overwrite the header
# #     def read_header(self):
# #         for x in range(0, HEADER_SIZE):
# #             self.new_image_data += self.original_image[x]
# #             self.image_byte_counter += 1
# #         # print(self.new_image_data)
# #     def hide_text_size(self):
# #         sz = len(self.text_to_hide)
# #         s_sz = str(sz)
# #         s_sz += DELIMITER # s_sz now equal to size of text to hide + Delimiter
# #         self.do_steg(s_sz)
# #
# #      # Hides the text in the image.
# #      # Does that by replacing the bytes LSB (Least significant bit) to be our bit
# #     def do_steg(self, steg_text):
# #
# #          # Goes through the text we want to hide, char by char
# #         for ch in range(0, len(steg_text)):
# #
# #             current_char = steg_text[ch] # Gets current Char
# #             current_char_binary = '{0:08b}'.format(ord(current_char)) # Gets the binary value of current character
# #
# #              # Goes through current char binary - bit by bit
# #             for bit in range(0, len(current_char_binary)):
# #                 new_byte_binary = ''
# #
# #                  ### Overwriting the image's byte LSB with our current Bit
# #
# #                  # Gets the binary value of original image byte
# #                 current_image_binary = '{0:08b}'.format(ord(self.original_image[self.image_byte_counter]))
# #
# #                  # Copies the first 7 bits (we want them to be the same)
# #                 new_byte_binary = current_image_binary[:7]
# #
# #                  # Set the last bit to be our bit
# #                 new_byte_binary += current_char_binary[bit]
# #
# #                  # Gets the new char value by it's binary
# #                 new_byte = chr(int(new_byte_binary, 2))
# #
# #                  # Adds new byte to output
# #                 self.new_image_data += new_byte
# #                 self.image_byte_counter += 1
# #
# #     def copy_rest(self):
# #          # Copies the what's left of the file
# #         self.new_image_data += self.original_image[self.image_byte_counter:]
# #
# #     def close_file(self):
# #         with open(StegImageFile, "wb") as out:
# #             out.write(bytearray(map(ord, self.new_image_data)))
# #             # out.write(self.new_image_data)
# #
# #     def run(self, stega_text):
# #         self.text_to_hide = stega_text
# #         self.open_image()
# #         self.read_header()
# #         self.hide_text_size()
# #         self.do_steg(self.text_to_hide)
# #         self.copy_rest()
# #         self.close_file()
# #
# # def main():
# #     pass
# #     global TextToHide
# #     stega_instance = LSBEncrypter()
# #     stega_instance.run(TextToHide)
# #     print("Successfully finished hiding text")
# #
# # if __name__ == '__main__':
# #     main()
# #
# # main()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # from PIL import Image
# # import png
# # im = Image.open("C:/Users/Sherif/OneDrive/P3/chris.png")
# # print (im)
# #
# # im1 = png.Reader.re
#
# # import Image
# #
# # im = Image.open("C:/Users/Sherif/OneDrive/P3/chris.png")
# #
# # print (im)
#
#
# # from PIL import Image
# #
# # import png, sys, os
# # import stepic
# # png_path = "C:/Users/Sherif/OneDrive/P3/chris.png"
# # print(Image.getdata())
# # im = png.Reader(png_path)
# # # png_width, png_height, png_pixels, png_meta = png_reader.read_flat()
# #
# # text = ''.join( map(chr,open("C:/Users/Sherif/OneDrive/P3/sec.txt", mode="rb").read()))
# # # im = Image.open(image_file_path)
# # im = stepic.encode(im, text)
# # # im.save(output_file_path + ".png", 'PNG')
# # # print(png_reader.read_flat())
#
#
#
#
#
# # for i in range(file_width * file_height):
# #     if file_pixels[i] == 0:
# #         if png_pixels[i*3] % 2 != 0:
# #             if png_pixels[i*3] == 255:
# #                 png_pixels[i*3] = 254
# #             else:
# #                 png_pixels[i*3] = png_pixels[i*3] + 1
# #     else:
# #         if png_pixels[i*3] % 2 == 0:
# #             png_pixels[i*3] = png_pixels[i*3] + 1
#
#
# # import getopt
# #
# # COLOR_GREEN = '\033[0;32m'
# # COLOR_YELLOW = '\033[0;33m'
# # COLOR_NONE = '\033[1;m'
# #
# # def hide_data(file_path, png_path, output_path):
# #     if not png_path or not os.path.isfile(png_path):
# #         raise Exception('Invalid PNG file')
# #
# #     if not file_path or not os.path.isfile(file_path):
# #         raise Exception('Invalid data file')
# #
# #     if not output_path:
# #         raise Exception('Invalid output path')
# #
# #     print (COLOR_YELLOW + ' ⚫ Injecting hidden image' + COLOR_NONE)
# #
# #     png_reader = png.Reader(png_path)
# #     png_width, png_height, png_pixels, png_meta = png_reader.read_flat()
# #
# #     file_reader = png.Reader(file_path)
# #     file_width, file_height, file_pixels, file_meta = file_reader.read_flat()
# #
# #     for i in xrange(file_width * file_height):
# #         if file_pixels[i] == 0:
# #             if png_pixels[i*3] % 2 != 0:
# #                 if png_pixels[i*3] == 255:
# #                     png_pixels[i*3] = 254
# #                 else:
# #                     png_pixels[i*3] = png_pixels[i*3] + 1
# #         else:
# #             if png_pixels[i*3] % 2 == 0:
# #                 png_pixels[i*3] = png_pixels[i*3] + 1
# #
# #     output_file = open(output_path, 'wb')
# #     output_writer = png.Writer(png_width, png_height)
# #     output_writer.write_array(output_file, png_pixels)
# #     output_file.close()
# #
# #     print (COLOR_GREEN + ' ✔ Hidden image was injected successfully' + COLOR_NONE)
# #
# #
# # def recover_data(png_path, output_path):
# #     if not png_path or not os.path.isfile(png_path):
# #         raise Exception('Invalid PNG file')
# #
# #     if not output_path:
# #         raise Exception('Invalid output path')
# #
# #     print (COLOR_YELLOW + ' ⚫ Extracting hidden image' + COLOR_NONE)
# #
# #     png_reader = png.Reader(png_path)
# #     width, height, pixels, meta = png_reader.asRGB8()
# #
# #     recoverd_data = []
# #     for row in pixels:
# #       for i in xrange(width):
# #           pixel = row[i*3]
# #           pixel = pixel % 2 != 0
# #           recoverd_data.append(int(pixel))
# #
# #     output_file = open(output_path, 'wb')
# #     output_writer = png.Writer(width, height, greyscale=True, bitdepth=1)
# #     output_writer.write_array(output_file, recoverd_data)
# #     output_file.close()
# #
# #     print( COLOR_GREEN + ' ✔ Hidden image was extracted successfully' + COLOR_NONE)
# #
# #
# # def print_usage():
# #     print( "\nUsage:\n" + \
# #           "  ./lsb.py --hide --file [PATH] --png [PATH] --output [PATH]\n" + \
# #           "  ./lsb.py --recover --png [PATH] --output [PATH]\n" + \
# #           "\nArguments:\n" + \
# #           "  -h, --hide        To hide data in a png file\n" + \
# #           "  -r, --recover     To recover data from a png file\n" + \
# #           "  -p, --png=        Path to a .png file\n" + \
# #           "  -f, --file=       Path to a file to hide in the png file\n" + \
# #           "  -o, --output=     Path to an output file\n" + \
# #           "  --help            Display this message\n")
# #
# #
# # hide_data("C:/Users/Sherif/OneDrive/P3/sec.txt", "C:/Users/Sherif/OneDrive/P3/chris.png", "C:/Users/Sherif/OneDrive/P3/output_path.png")
# #
# # try:
# #     opts, args = getopt.getopt(sys.argv[1:], 'hrp:f:o:',
# #         ['hide', 'recover', 'png=', 'file=', 'output=', 'help'])
# #
# # except getopt.GetoptError as e:
# #     print (e)
# #     print_usage()
# #     sys.exit(1)
# #
# # hiding_data = False
# # recovering_data = False
# # png_path = None
# # file_path = None
# # output_path = None
# #
# # for opt, arg in opts:
# #     if opt in ("-h", "--hide"):
# #         hiding_data = True
# #     elif opt in ("-r", "--recover"):
# #         recovering_data = True
# #     elif opt in ("-p", "--png"):
# #         png_path = arg
# #     elif opt in ("-f", "--file"):
# #         file_path = arg
# #     elif opt in ("-o", "--output"):
# #         output_path = arg
# #     elif opt in ("--help"):
# #         print_usage()
# #         sys.exit(1)
# #     else:
# #         print("Invalid argument {}".format(opt))
# #
# # if (not hiding_data and not recovering_data):
# #     print_usage()
# #     sys.exit(0)
# #
# # try:
# #     if (hiding_data):
# #         hide_data(file_path, png_path, output_path)
# #     if (recovering_data):
# #         recover_data(png_path, output_path)
# #
# # except Exception as e:
# #     print (e)
# #     print_usage()
# # sys.exit(1)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # class LSBEncrypter(object):
# #
# #     def __init__(self):
# #         self.image_byte_counter = 0
# #         self.new_image_data = ''
# #         self.original_image = ''
# #         self.text_to_hide = ''
# #
# #     def open_image(self):
# #         # Open the image file
# #         with open(ImageFile, "rb") as f:
# #             self.original_image = f.read()
# #
# #     # Reading first chunk of the file - we don't want to overwrite the header
# #     def read_header(self):
# #         for x in range(0, HEADER_SIZE):
# #             self.new_image_data += self.original_image[x]
# #             self.image_byte_counter += 1
# #
# #     def hide_text_size(self):
# #         sz = len(self.text_to_hide)
# #         s_sz = str(sz)
# #         s_sz += DELIMITER # s_sz now equal to size of text to hide + Delimiter
# #         self.do_steg(s_sz)
# #
# #     # Hides the text in the image.
# #     # Does that by replacing the bytes LSB (Least significant bit) to be our bit
# #     def do_steg(self, steg_text):
# #
# #         # Goes through the text we want to hide, char by char
# #         for ch in range(0, len(steg_text)):
# #
# #             current_char = steg_text[ch] # Gets current Char
# #             current_char_binary = '{0:08b}'.format(ord(current_char)) # Gets the binary value of current character
# #
# #             # Goes through current char binary - bit by bit
# #             for bit in range(0, len(current_char_binary)):
# #                 new_byte_binary = ''
# #
# #                 ### Overwriting the image's byte LSB with our current Bit
# #
# #                 # Gets the binary value of original image byte
# #                 current_image_binary = '{0:08b}'.format(ord(self.original_image[self.image_byte_counter]))
# #
# #                 # Copies the first 7 bits (we want them to be the same)
# #                 new_byte_binary = current_image_binary[:7]
# #
# #                 # Set the last bit to be our bit
# #                 new_byte_binary += current_char_binary[bit]
# #
# #                 # Gets the new char value by it's binary
# #                 new_byte = chr(int(new_byte_binary, 2))
# #
# #                 # Adds new byte to output
# #                 self.new_image_data += new_byte
# #                 self.image_byte_counter += 1
# #
# #     def copy_rest(self):
# #         # Copies the what's left of the file
# #         self.new_image_data += self.original_image[self.image_byte_counter:]
# #
# #     def close_file(self):
# #         with open(StegImageFile, "wb") as out:
# #             out.write(self.new_image_data)
# #
# #     def run(self, stega_text):
# #         self.text_to_hide = stega_text
# #         self.open_image()
# #         self.read_header()
# #         self.hide_text_size()
# #         self.do_steg(self.text_to_hide)
# #         self.copy_rest()
# #         self.close_file()
# # HEADER_SIZE = 54 # Header size of BMP
# # DELIMITER = "$" # Separator between number of characters and text
# # TextToHide = "I Am Secret Information!"
# # ImageFile = "C:/secret.jpg"
# # StegImageFile = "hidden_secret.png"
# # stega_instance = LSBEncrypter()
# # stega_instance.run(TextToHide)
#
#
#
#
#
#
#
#
#
#  # def __init__(self):
# #     self.image_byte_counter = 0
# #     self.new_image_data = ''
# #     self.original_image = ''
# #     self.text_to_hide = ''
# #
# # def open_image(self):
# #         # Open the image file
# #     with open(ImageFile, "rb") as f:
# #         self.original_image = f.read()
# #
# #     # Reading first chunk of the file - we don't want to overwrite the header
# # def read_header(self):
# #     for x in range(0, HEADER_SIZE):
# #         self.new_image_data += self.original_image[x]
# #         self.image_byte_counter += 1
# #
# # def hide_text_size(self):
# #     sz = len(self.text_to_hide)
# #     s_sz = str(sz)
# #     s_sz += DELIMITER # s_sz now equal to size of text to hide + Delimiter
# #     self.do_steg(s_sz)
# #
# #     # Hides the text in the image.
# #     # Does that by replacing the bytes LSB (Least significant bit) to be our bit
# # def do_steg(self, steg_text):
# #
# #         # Goes through the text we want to hide, char by char
# #     for ch in range(0, len(steg_text)):
# #
# #         current_char = steg_text[ch] # Gets current Char
# #         current_char_binary = '{0:08b}'.format(ord(current_char)) # Gets the binary value of current character
# #
# #             # Goes through current char binary - bit by bit
# #         for bit in range(0, len(current_char_binary)):
# #             new_byte_binary = ''
# #
# #                 ### Overwriting the image's byte LSB with our current Bit
# #
# #                 # Gets the binary value of original image byte
# #             current_image_binary = '{0:08b}'.format(ord(self.original_image[self.image_byte_counter]))
# #
# #                 # Copies the first 7 bits (we want them to be the same)
# #             new_byte_binary = current_image_binary[:7]
# #
# #                 # Set the last bit to be our bit
# #             new_byte_binary += current_char_binary[bit]
# #
# #                 # Gets the new char value by it's binary
# #             new_byte = chr(int(new_byte_binary, 2))
# #
# #                 # Adds new byte to output
# #             self.new_image_data += new_byte
# #             self.image_byte_counter += 1
# #
# # def copy_rest(self):
# #         # Copies the what's left of the file
# #     self.new_image_data += self.original_image[self.image_byte_counter:]
# #
# # def close_file(self):
# #     with open(StegImageFile, "wb") as out:
# #         out.write(self.new_image_data)
# #
# # def run(self, stega_text):
# #     self.text_to_hide = stega_text
# #     self.open_image()
# #     self.read_header()
# #     self.hide_text_size()
# #     self.do_steg(self.text_to_hide)
# #     self.copy_rest()
# #     self.close_file()
# #
# #
# # TextToHide = "I Am Secret Information!"
# # ImageFile = "secret.jpg"
# # StegImageFile = "hidden_secret.png"
# #
# # run()
#
#
#
#
#
#
#
#
#
# # from hide import hide
# # import os
# # src = "C:/Users/Sherif/OneDrive/P3/source.zip"
# # # print (src)
# # hide("secret.jpg", src)
# # from LSBEncrypter import main
# #
# # TextToHide = "I Am Secret Information!"
# # ImageFile = "secret.jpg"
# # StegImageFile = "hidden_cat.jpg"
# #
# # main()
# # import Image
# # import stepic
# # import os
# # def enc_():
# #     # filename = os.path.join("C:\\Users\\Sherif\\OneDrive\\P3", "secret.jpg")
# #     im = Image.open("C:/Users/Sherif/OneDrive/P3/secret.jpg")
# #     text = ''.join(map(chr, open("source.zip", "rb").read()))
# #     im = stepic.encode(im, text)
# #     im.save('stegolena.png','PNG')
# #
# # enc_()
#
# # def dec_():
# #     im1=Image.open('stegolena.png')
# #     out = stepic.decode(im1)
# #     plaintext = open("out.zip", "wb")
# #     plaintext.write(bytearray(map(ord, out)))
# #     # plaintext.write(out)
# #     plaintext.close()
# # enc_()
