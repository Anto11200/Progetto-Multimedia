from bitstring import BitArray
import cv2
from tqdm import tqdm

def audio_to_binary(image_path, filename):
    """
    Converte un file audio in una rappresentazione binaria e lo prepara per l'incorporazione in un'immagine.
    Args:
        image_path (str): Percorso dell'immagine che conterrà i dati nascosti.
        filename (str): Percorso del file audio da nascondere.
    Returns:
        str: Stringa di bit rappresentante i dati del file audio.
    """
    
    SEP = "FINE"    # Separatore che indica la fine dei dati
    data = BitArray(bytes=open(filename,'rb').read())  # Legge il file audio in formato binario

    # Carica l'immagine per determinare la capacità di archiviazione
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image not found or could not be read.")

    # Calcola la dimensione massima di dati incorporabili in base ai pixel disponibili
    max_data_size_to_bytes = (image.shape[0] * image.shape[1] * 3) // 8
    data_size_to_bytes = (len(data) / 8) + len(SEP)

    # Controlla se il file audio è troppo grande per essere nascosto nell'immagine
    if data_size_to_bytes > max_data_size_to_bytes:
        raise ValueError(f"Data is too large to embed. Maximum size: {max_data_size_to_bytes} bytes.")
    
    ext = filename.split(".")[1]  # Estrai l'estensione del file audio
    
    # Converte i dati in una stringa binaria
    # binary_Data = lunghezza estensione + estensione + dati audio
    binary_data = format(len(ext), '08b') + ''.join(format(ord(l), '08b') for l in ext) + data.bin
    binary_data += ''.join(format(ord(l), '08b') for l in SEP)
    
    return binary_data


def steganography_embed(binary_data, output_path):
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
    for i in tqdm(range(len(binary_data)), desc="Embedding Data", unit="bit"):
        if data_index < len(binary_data):
            pixel_bin = format(flat_image[i], '08b')  # Converte il pixel in binario (8 bit)
            flat_image[i] = int(pixel_bin[:-1] + binary_data[data_index], 2)  # Sostituisce l'ultimo bit
            data_index += 1
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
    
    # Carica l'immagine
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image not found or could not be read.")
    
    binary_data = ""
    
    # Estrae gli ultimi bit di ogni valore di colore
    last_bits = (image & 1).reshape(-1, 3)
    
    # Converte i bit estratti in una stringa binaria
    binary_data = ''.join(map(lambda x: ''.join(map(str, x)), tqdm(last_bits, desc="Extracting Data", unit="bit")))

    # Divide i dati in blocchi da 8 bit (byte)
    byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data),8)]

    # Ricostruisce il nome dell'estensione
    filename_ext_length = int(byte_data[0], 2)  # Lunghezza dell'estensione
    filename_ext = ''.join(map(lambda x: chr(int(x, 2)), byte_data[1:filename_ext_length+1]))
    binary_data = ''.join(byte_data[filename_ext_length+1:])

    # Rimuove i dati successivi al separatore "FINE" (in binario)
    binary_data = binary_data.split("01000110010010010100111001000101")[0]  # "FINE" in ASCII
    byte_data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))

    # Scrive i dati estratti in un file binario
    with open(f"./decode/extracted.{filename_ext}", "wb") as fp:
        fp.write(byte_data)


if __name__=="__main__":
    """
    Esegue la steganografia: nasconde un file audio in un'immagine e lo estrae successivamente.
    """
    
    image_path = "image/japan.png"  # Immagine sorgente
    # image_path = "image/rosso.png"  # Immagine sorgente

    output_path = "encode/encode_audio_in_image.png"  # Immagine di output
    
    # source_audio_path = "audio/relaxing-guitar.mp3"  # File audio da nascondere
    source_audio_path = "audio/Damned.mp3"

    binary_data= audio_to_binary(image_path, source_audio_path)  # Converte l'audio in binario
    steganography_embed(binary_data, output_path)  # Nasconde i dati nell'immagine
    steganography_extract(output_path)  # Estrae i dati dall'immagine