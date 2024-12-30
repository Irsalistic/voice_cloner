import os
import torch
from TTS.api import TTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip


def process_text(speech_text):
    max_text_length = 120
    if len(speech_text) > max_text_length:
        last_space = speech_text[:max_text_length].rfind(" ")
        speech_text = speech_text[:last_space]
    return speech_text


def process_language(language):
    language_mapping = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Polish': 'pl',
        'Turkish': 'tr',
        'Russian': 'ru',
        'Dutch': 'nl',
        'Czech': 'cs',
        'Arabic': 'ar',
        'Chinese (Simplified)': 'zh-cn',
        'Hindi': 'hi',
    }
    language = language.capitalize()
    if language == 'Chinese':
        language = "Chinese (Simplified)"
    target_language = language_mapping.get(language)
    if target_language is None:
        supported_languages = ", ".join(language_mapping.keys())
        raise ValueError(f"Unsupported language {language}. Supported languages are {supported_languages}")
    return target_language


def tts_file(audio_file_path, speech_text, language, user_folder):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    output_file_path = os.path.join(user_folder, "cloned_voice.wav")
    tts.tts_to_file(
        text=speech_text,
        speaker_wav=audio_file_path,
        file_path=output_file_path,
        language=language
    )

    return output_file_path


def create_video_with_audio(cloned_voice_path, image_file_path):
    # Define the path to the temporary video file
    temp_video_path = os.path.join(os.path.dirname(cloned_voice_path), "temp_video.mp4")

    # Create an ImageClip and set the duration to match the audio length
    audio_clip = AudioFileClip(cloned_voice_path)
    image_clip = ImageClip(image_file_path, duration=audio_clip.duration)

    # Set the fps for the ImageClip
    image_clip = image_clip.set_fps(24)

    # Set the audio of the ImageClip
    video_clip = CompositeVideoClip([image_clip.set_audio(audio_clip)])

    # Write the final video to a temporary file
    video_clip.write_videofile(temp_video_path, codec="libx264", audio_codec="aac")

    # Read the video file and return its stream
    with open(temp_video_path, 'rb') as video_file:
        video_stream = video_file.read()

    # Clean up temporary video file
    os.remove(temp_video_path)

    return video_stream
