import whisper
import tempfile

class WhisperHandler:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_file):
        if not audio_file.name.lower().endswith(".wav"):
            raise ValueError("Only .wav files are supported")

        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name

        # Force decoding raw WAV without ffmpeg
        result = self.model.transcribe(tmp_path, fp16=False)  
        return result["text"]
