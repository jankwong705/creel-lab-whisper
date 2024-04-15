# Whisper Installation Guide (MacOS)

### Step 1: Install Homebrew
You can go to [this link](www.brew.sh) for a more detailed installation guide for Homebrew.

First, open your terminal and type in the following line:

``/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"``

You will be prompted to enter your computer passwords.

### Step 2: Install ffmpeg 

In your terminal, type in the following line:

``brew install ffmpeg``

After installation finished, run:

``pip3 install ffmpeg ``

To check whether `ffmpeg` has been successfully installed, you can run:

``ffmpeg -version``

### Step 3: Install Whisper

In your terminal, type in the following line:

``pip3 install git+https://github.com/openai/whisper.git ``

### Step 4: Run Whisper 

Before running Whisper, it would be helpful to have an audio file ready. 

To run whisper, type in the following line in your terminal:

``whisper <file_name>.wav``

The output will appear in the terminal and be saved to `<file_name>.wav.txt`.

## Running Whisper on Python

We will need to import Whisper to Python first. Make sure that you have Whisper installed already on your computer.
```
import whisper
```

To load the model:

```
model = whisper.load(<model>)
```
Whisper has various models: `tiny, base, small, medium, large`. Replace `<model>` with the desired model you wish to install.

