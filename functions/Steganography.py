import cv2
from alive_progress import alive_bar

from functions.AudioToBinary import *


def steganography_embed(image_path, binary_data, output_path):
    """
    Incorpora i dati binari in un'immagine usando la tecnica LSB (Least Significant Bit). 
    Args:
        binary_data (str): Dati binari da nascondere nell'immagine.
        output_path (str): Percorso dell'immagine risultante con i dati nascosti.
    """
    
    data_index = 0  # Indice per iterare sui bit dei dati
    
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    flat_image = image.flatten()  # Appiattisce l'immagine in un array monodimensionale
        
    # Incorpora i bit dei dati nei bit meno significativi dei pixel dell'immagine
    with alive_bar(len(binary_data), title="Embedding Data", dual_line=True, bar='filling') as bar:
        bar.text("-> Inserimento audio nell\'immagine contenitore...")
        for i in range(len(binary_data)):
    # for i in tqdm(range(len(binary_data)), desc="Embedding Data", unit="bit"):
            if data_index < len(binary_data):
                pixel_bin = format(flat_image[i], '08b')  # Converte il pixel in binario (8 bit)
                flat_image[i] = int(pixel_bin[:-1] + binary_data[data_index], 2)  # Sostituisce l'ultimo bit
                data_index += 1
                bar()
            else:
                break

    # Ricostruisce l'immagine originale con i dati nascosti
    embedded_image = flat_image.reshape(image.shape)

    # Salva l'immagine con i dati incorporati
    cv2.imwrite(output_path, embedded_image)

def steganography_extract(image_path):
    """
    Estrae i dati nascosti da un'immagine che utilizza la tecnica LSB.
    Args:
        image_path (str): Percorso dell'immagine contenente i dati nascosti.
    """
    
    # Carica l'immagine a colori
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image not found or could not be read.")
    
    binary_data = ""
    
    # Estrazione dei bit meno significativi (LSB) di ogni canale colore (B, G, R)
    last_bits = (image & 1).reshape(-1, 3)
    
    # Converte i bit estratti in una stringa binaria
    with alive_bar(len(last_bits), title="Extracting Data", dual_line=True, bar="filling") as bar:
        bar.text("-> Estrazione audio dall'immagine contenitore...")
        binary_data = ''.join(map(lambda x: ''.join(map(str, x)), [bar() or bit for bit in last_bits]))

    # Divide i dati in blocchi da 8 bit (byte)
    byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data),8)]

    # Ricostruisce il nome dell'estensione
    filename_ext_length = int(byte_data[0], 2)  # Lunghezza dell'estensione
    filename_ext = ''.join(map(lambda x: chr(int(x, 2)), byte_data[1:filename_ext_length+1]))
    binary_data = ''.join(byte_data[filename_ext_length+1:])

    # Rimuove i dati successivi al separatore "FINE" (in binario)
    binary_data = binary_data.split("01000110010010010100111001000101")[0]  # "FINE" in ASCII
    
    # Converti la stringa binaria in dati binari
    byte_data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))

    # Scrive i dati estratti in un file binario
    with open(f"./decode/extracted.{filename_ext}", "wb") as fp:
        fp.write(byte_data)