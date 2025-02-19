import ffmpeg
import subprocess
import re


def reduce_bitrate_128k(input_audio, output_audio, bitrate):
    """
    Riduce il bitrate di un file audio usando FFmpeg.
    
    Args:
        input_audio (str): Percorso del file audio originale.
        output_audio (str): Percorso del file audio con bitrate ridotto.
        bitrate (str): Nuovo bitrate desiderato (es. "128k", "96k").
    """
    try:
        ffmpeg.input(input_audio).output(output_audio, audio_bitrate=bitrate).run(overwrite_output=True)
        print(f"Bitrate ridotto con successo: {output_audio}")
        return output_audio
    except ffmpeg.Error as e:
        print("Errore durante la conversione:", e)


def get_bitrate(audio_file):
    result = subprocess.run(
        ["ffmpeg", "-i", audio_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    
    # Scandisci le linee di stderr (dove ffmpeg scrive le info audio)
    for line in result.stderr.split("\n"):
        if "Audio:" in line:
            match = re.search(r"(\d+)\s*kb/s", line)  # Cerca il numero prima di "kb/s"
            if match:
                return int(match.group(1))  # Restituisce il bitrate come numero intero
    return None  # Se non trova nulla, restituisce None