
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time

CHANNELS = 1         
RATE = 44100         
CHUNK = 1024        
THRESHOLD = 1           
SILENCE_DURATION = 2  

def rms(data):
    """Calculate RMS of audio data."""
    return np.sqrt(np.mean(np.square(data)))

def record_on_sound():
    print("Listening for sound...")
    frames = []
    silence_start = None
    recording = False
    recording_complete = False

    def callback(indata, frame_count, time_info, status):
        nonlocal recording, silence_start, recording_complete, frames
        volume_norm = rms(indata) * 10
        
        if volume_norm > THRESHOLD:
            if not recording:
                print("Sound detected, recording...")
                recording = True
            frames.append(indata.copy())
            silence_start = None
        elif recording:
            if silence_start is None:
                silence_start = time_info.inputBufferAdcTime
            elif (time_info.inputBufferAdcTime - silence_start) > SILENCE_DURATION:
                print("Silence detected, stopping recording...")
                recording_complete = True
                return
            frames.append(indata.copy())

    with sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=callback):
        while not recording_complete:
            sd.sleep(100)

    return frames

def save_wav(filename, frames):
    frames_np = np.concatenate(frames, axis=0)
    frames_np = np.int16(frames_np * 32767)
    wav.write(filename, RATE, frames_np)



