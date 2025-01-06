# Voice Cloning and Video Generation API

A FastAPI-based service that creates videos with cloned voices from text input. The API supports multiple languages and combines voice cloning with image-to-video generation.

## Features

- Voice cloning using XTTS v2 model
- Multi-language support (14 languages)
- Text-to-speech generation with cloned voices
- Video generation with static images and synthesized audio
- Automatic user-specific directory management

## Prerequisites

- Python 3.8+
- PyTorch
- FastAPI
- TTS (Text-to-Speech)
- MoviePy
- CUDA-capable GPU (optional, for faster processing)

## Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install fastapi torch TTS moviepy python-multipart
```

## Project Structure

```
project/
├── main.py              # FastAPI application and endpoints
├── audio_processing.py  # Audio and video processing functions
└── user_folders/        # Generated automatically for each user
    └── user_name/
        ├── original_voice.wav
        ├── image.jpg
        └── cloned_voice.wav
```

## API Endpoints

### POST /clone_audio

Creates a video with cloned voice narration.

**Parameters:**
- `name` (form): User identifier
- `speech_text` (form): Text to be converted to speech (max 120 characters)
- `language` (form): Target language for speech synthesis

**Returns:**
- Video file (MP4) with the cloned voice and static image
- Error JSON response if processing fails

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Polish (pl)
- Turkish (tr)
- Russian (ru)
- Dutch (nl)
- Czech (cs)
- Arabic (ar)
- Chinese (Simplified) (zh-cn)
- Hindi (hi)

## Usage Example

```python
import requests

url = "http://your-api-url/clone_audio"
files = {
    'name': (None, 'john_doe'),
    'speech_text': (None, 'Hello, this is a test message.'),
    'language': (None, 'English')
}

response = requests.post(url, files=files)

if response.status_code == 200:
    # Save the video
    with open('output_video.mp4', 'wb') as f:
        f.write(response.content)
else:
    print(f"Error: {response.json()}")
```

## Technical Details

- Maximum text length: 120 characters
- Video output format: MP4 (H.264 codec)
- Audio output format: WAV
- Video frame rate: 24 fps
- Required files per user:
  - `original_voice.wav`: Source voice file for cloning
  - `image.jpg`: Static image for video generation

## Error Handling

The API includes comprehensive error handling for:
- Missing user files
- Unsupported languages
- Text length restrictions
- Processing failures

