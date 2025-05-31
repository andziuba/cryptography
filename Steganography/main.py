from PIL import Image


def encode_lsb(image_path, message, output_path):
    img = Image.open(image_path)

    # Zamiana znaku na 8-biotwy ciąg binary, dodanie znacznika końca wiadomości
    binary_message = ''.join([format(ord(i), "08b") for i in message]) + '11111110'
    
    img_data = img.getdata()  # Dane pikseli obrazu

    new_data = []
    data_index = 0

    for pixel in img_data:  # Iteracja po pikselach obrazu
        new_pixel = list(pixel)

        # Modyfikacja dla każdego kanału koloru (R, G, B)
        for i in range(3):
            if data_index < len(binary_message):
                # Zerowanie ostatniego bitu, ustawianie nowego bitu
                new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[data_index])
                data_index += 1
        new_data.append(tuple(new_pixel))

    img.putdata(new_data)
    img.save(output_path)
    print(f"Zaszyfrowano wiadomość w {output_path}")


def decode_lsb(image_path):
    img = Image.open(image_path)
    img_data = img.getdata()

    binary_data = ""
    for pixel in img_data:
        # Odczyt z każdego kanału koloru (R, G, B)
        for value in pixel[:3]:
            binary_data += str(value & 1)  # Pobranie ostatniego bitu

    # Podział na bajty
    bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in bytes_data:
        if byte == '11111110':  # Koniec wiadomości
            break
        message += chr(int(byte, 2))  # Zamiana bajtu na znak

    return message


# Ukrywanie wiadomości
encode_lsb("input_image.png", "Secret test message", "output_image.png")

# Odczytywanie wiadomości
print(decode_lsb("output_image.png"))
