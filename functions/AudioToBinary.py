from bitstring import BitArray
import cv2


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
