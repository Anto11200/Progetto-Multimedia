from bitstring import BitArray
import cv2

def steganography_embed(image_path, output_path, filename):
    SEP = "FINE"
    data = BitArray(bytes=open(filename,'rb').read())

    # Leggi l'immagine
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image not found or could not be read.")

    # Calcola la dimensione massima dei dati che possono essere incorporati
    max_data_size_to_bytes = (image.shape[0] * image.shape[1] * 3) // 8
    data_size_to_bytes = (len(data) / 8) + len(SEP)

    # Controlla se i dati sono troppo grandi per essere incorporati
    if data_size_to_bytes > max_data_size_to_bytes:
        raise ValueError(f"Data is too large to embed. Maximum size: {max_data_size_to_bytes} bytes.")
    
    ext = filename.split(".")[1]

    # Converti i dati in una stringa binaria
    binary_data = format(len(ext), '08b') + ''.join(format(ord(l), '08b') for l in ext) + data.bin
    binary_data += ''.join(format(ord(l), '08b') for l in SEP)

    data_index = 0
    flat_image = image.flatten()

    # Incorpora i dati binari nell'immagine
    for i in range(len(binary_data)):
        if data_index < len(binary_data):
            pixel_bin = format(flat_image[i], '08b')
            flat_image[i] = int(pixel_bin[:-1] + binary_data[data_index], 2)
            data_index += 1
        else:
            break

    # Rimodella l'immagine nella sua forma originale
    embedded_image = flat_image.reshape(image.shape)

    # Salva l'immagine modificata
    cv2.imwrite(output_path, embedded_image)

def steganography_extract(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image not found or could not be read.")
    
    binary_data = ""
    
    last_bits = (image & 1).reshape(-1, 3)

    # Converte i bit in una stringa binaria
    binary_data = ''.join(map(lambda x: ''.join(map(str, x)), last_bits)) 

    byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data),8)]

    filename_ext_length = int(byte_data[0], 2)
    filename_ext = "".join(map(lambda x: chr(int(x, 2)), byte_data[1:filename_ext_length+1]))
    binary_data = "".join(byte_data[filename_ext_length+1:])

    binary_data = binary_data.split("01000110010010010100111001000101")[0] #FINE sep.
    byte_data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))

    # Scrivi i byte in un file binario
    with open(f"./extracted_audio/test.{filename_ext}", "wb") as fp:
        fp.write(byte_data)

image_path = "rosso.png"
output_path = "encode_image.png"
audio = "encode_image.png"

steganography_embed(image_path, output_path, "relaxing-guitar.mp3")
steganography_extract(output_path)