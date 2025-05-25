import numpy as np
from PIL import Image
import random


# Każda macierzy ze zbiorów C0 i C1 ma 2 wiersze po 4 bity - jeden wiersz do udziału 1, drugi do udziału 2
C0 = [  # dla białych pikseli
    [[0, 0, 1, 1], [0, 0, 1, 1]],
    [[1, 1, 0, 0], [1, 1, 0, 0]],
    [[1, 0, 1, 0], [1, 0, 1, 0]],
    [[1, 0, 1, 0], [1, 0, 1, 0]],
    [[0, 1, 1, 0], [0, 1, 1, 0]],
    [[1, 0, 0, 1], [1, 0, 0, 1]],
]

C1 = [  # dla czarnych pikseli
    [[1, 0, 0, 1], [0, 1, 1, 0]],
    [[0, 1, 1, 0], [1, 0, 0, 1]],
    [[0, 0, 1, 1], [1, 1, 0, 0]],
    [[1, 1, 0, 0], [0, 0, 1, 1]],
    [[0, 1, 0, 1], [1, 0, 1, 0]],
    [[1, 0, 1, 0], [0, 1, 0, 1]],
]


def load_image(path, size=(100, 100)):
    image = Image.open(path).convert('1')
    return image.resize(size)


# Szyfrowanie obrazu (podział na dwa udziały)
def encrypt(image):
    width, height = image.size
    # Zmiana każdego piksela na 2x2
    share1 = Image.new('1', (width * 2, height * 2))
    share2 = Image.new('1', (width * 2, height * 2))

    pixels = image.load()
    s1 = share1.load()
    s2 = share2.load()

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]

            if pixel == 255:
                pattern = random.choice(C0)  # Biały piksel - losowa macierz z C0

            else:
                pattern = random.choice(C1)  # Czarny piksel - losowa macierz z C1

            p1, p2 = pattern 

            # Współrzędne subpikseli (przy zamianie każdego piksela na 2x2)
            coords = [
                [x * 2, y * 2],
                [x * 2 + 1, y * 2],
                [x * 2, y * 2 + 1],
                [x * 2 + 1, y * 2 + 1]
            ]

            # Przypisanie wartości ze wzorców do subpikseli
            for i, (cx, cy) in enumerate(coords):
                s1[cx, cy] = 255 if p1[i] == 0 else 0
                s2[cx, cy] = 255 if p2[i] == 0 else 0

    return share1, share2


# Łączenie dwóch udziałów (deszyfrowanie)
def combine_shares(share1, share2):
    width, height = share1.size
    combined = Image.new('1', (width, height))
    p1 = share1.load()
    p2 = share2.load()
    pc = combined.load()

    for y in range(height):
        for x in range(width):
            # Jeśli którykolwiek subpiksel jest czarny, to wynik jest czarny
            pc[x, y] = 0 if p1[x, y] == 0 or p2[x, y] == 0 else 255

    return combined


if __name__ == "__main__":
    input_img = load_image("./input.png")

    # Zaszyfruj
    share1, share2 = encrypt(input_img)

    # Zapisz oba udziały
    share1.save("share1.png")
    share2.save("share2.png")

    # Obraz rozszyfrowany
    combined = combine_shares(share1, share2)
    combined.save("result.png")
