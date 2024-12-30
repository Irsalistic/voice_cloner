import os
import io
from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, JSONResponse
from audio_processing import process_text, process_language, tts_file, create_video_with_audio

app = FastAPI()


@app.post("/clone_audio")
async def audio_clone(
        name: str = Form(...),
        speech_text: str = Form(...),
        language: str = Form(...)
):
    try:
        name = name.lower().replace(" ", "_")
        print(name)
        # Create directory based on the user's name
        user_folder = os.path.join(name)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Process the input text and language
        speech_text = process_text(speech_text)
        target_language = process_language(language)

        # Paths to the cloned voice file and image in the user's folder
        audio_file_path = os.path.join(name, "original_voice.wav")
        image_file_path = os.path.join(name, "image.jpg")

        # Check if the necessary files exist
        if not os.path.exists(audio_file_path):
            return JSONResponse(status_code=400, content={"error": "Cloned voice file does not exist."})
        if not os.path.exists(image_file_path):
            return JSONResponse(status_code=400, content={"error": "Image file does not exist."})

        # Generate the cloned voice file path
        cloned_voice_path = tts_file(audio_file_path, speech_text, target_language, user_folder)

        if cloned_voice_path:
            # Create a video with the cloned audio and the image
            video_stream = create_video_with_audio(cloned_voice_path, image_file_path)

            # Return the video stream as a response
            return StreamingResponse(io.BytesIO(video_stream), media_type="video/mp4")

    except Exception as e:
        # Return an error message if any exception occurs
        return JSONResponse(status_code=500, content={"error": f"Lip-syncing failed: {str(e)}"})
