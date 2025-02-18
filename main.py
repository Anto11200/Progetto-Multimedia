from functions.AudioToBinary import *
from functions.Steganography import *


if __name__=="__main__":
    """
    Esegue la steganografia: nasconde un file audio in un'immagine e lo estrae successivamente.
    """
    
    # image_path = "image/japan.png"  # Immagine sorgente
    image_path = "image/rosso.png"  # Immagine sorgente

    output_path = "encode/encoded_image.png"  # Immagine di output
    
    source_audio_path = "audio/relaxing-guitar.mp3"  # File audio da nascondere
    # source_audio_path = "audio/Damned.mp3"

    binary_data= audio_to_binary(image_path, source_audio_path)  # Converte l'audio in binario
    steganography_embed(image_path, binary_data, output_path)  # Nasconde i dati nell'immagine
    steganography_extract(output_path)  # Estrae i dati dall'immagine