#!/usr/bin/env python

import numpy as np
import audiosegment
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import subprocess as sp

from pathlib import Path

import functools as ft

from scipy.fftpack import fft

from time import sleep

AUDIO_FILE_PATH = Path("/home/adrien/Downloads/Telegram Desktop/mr_x_1997_01_25.mp3")

def split_chunks(file_path, duration=1, sample_rate=44100):
    command = [
        "ffmpeg", 
        "-loglevel", "error",
		"-i", str(file_path),
		"-acodec", "pcm_s16le", 
		"-f", "s16le", 
		"-ac", "1",
		"-ar", str(sample_rate),
		"-"
    ]
    print(" ".join(command))
    process = sp.Popen(command, stdout=sp.PIPE)
    byte_buffer_size = sample_rate * duration *  2 # s16le => bit depth of 2 bytes per channel
    for byte_buffer in iter(ft.partial(process.stdout.read, byte_buffer_size), b""):
        print("Yielding chunk... ")
        chunk = np.frombuffer(byte_buffer, dtype=np.int16)
        #print(chunk)
        yield chunk
        print("Chunk yielded!")

def play_chunk(chunk, sample_rate=44100):
    print("Playing chunk... ")
    command = [
        "ffplay", 
        "-autoexit",
        "-nodisp", 
        #"-showmode", "2",
        "-f", "s16le",
		"-ar", str(sample_rate), 
		"-ac", "1", 
        "-",
    ]
    process = sp.Popen(command, stdin=sp.PIPE)
    process.stdin.write(chunk.tobytes())
    process.stdin.close()
    process.wait()
    print("Chunk played! ")

def write_chunk(chunk, file_path, sample_rate=41000):
    print("Writing chunk... ")
    command = [
        "ffmpeg", 
        "-y", 
        "-f", "s16le",
		"-ar", str(sample_rate), 
		"-ac", "1", 
        "-i", "-",
        str(file_path)
    ]
    process = sp.Popen(command, stdin=sp.PIPE)
    process.stdin.write(chunk.tobytes())
    process.stdin.close()
    process.wait()
    print("Chunk written! ")


DURATION = 1
SAMPLE_RATE = 44100
SAMPLE_SIZE = DURATION * 2 * SAMPLE_RATE

def plot_waveform(chunk, subplot):
    subplot.clear()
    subplot.plot(chunk)

def main():
    chunks = split_chunks(AUDIO_FILE_PATH, duration=DURATION, sample_rate=SAMPLE_RATE)
    figure, (waveform_subplot, fft_subplot) = plt.subplots(nrows=2, ncols=1)
    for chunk in chunks:
        plot_waveform(chunk, waveform_subplot)
        plot_fft(fft_subplot)
        plt.pause(0.5)
        #print(chunk)
        #print(chunk.shape)
        #print(chunk.dtype)

        #plt.figure(1)
        #plt.title("Signal Wave...")
        #plt.plot(chunk)
        #plt.show()
        
        #play_chunk(chunk, sample_rate=SAMPLE_RATE)
        #write_chunk(chunk, Path("./test.mp3"), sample_rate=SAMPLE_RATE)
        #break
