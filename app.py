import streamlit as st
import os
import tempfile
import subprocess
import shutil

# Ensure required dependencies are installed
def check_dependencies():
    missing = []
    if shutil.which("whisperx") is None:
        missing.append("whisperx")
    if shutil.which("ffmpeg") is None:
        missing.append("ffmpeg")

    if missing:
        st.warning(f"⚠️ Missing dependencies: {', '.join(missing)}")
        st.write("To install them, run:")
        if "whisperx" in missing:
            st.code("pip install whisperx")
        if "ffmpeg" in missing:
            st.code("brew install ffmpeg  # macOS (Homebrew)")
            st.code("sudo apt install ffmpeg  # Ubuntu/Debian")
            st.code("choco install ffmpeg  # Windows (Chocolatey)")
        return False
    return True

# Streamlit UI
st.title("📝 WhisperX Transcriber")
st.write("Upload an audio file to transcribe using WhisperX.")

# Check dependencies before proceeding
if not check_dependencies():
    st.stop()

# File Upload
uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.success("✅ File uploaded successfully!")

    # Transcription Button
    if st.button("Transcribe Audio"):
        st.info("Transcribing... This may take some time ⏳")

        # Run WhisperX command (using relative path)
        output_dir = tempfile.mkdtemp()
        command = ["whisperx", temp_audio_path, "--model", "medium", "--diarize", "--output_format", "txt", "--output_dir", output_dir]

        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode == 0:
            # Find the transcript file in the output directory
            transcript_file = os.path.join(output_dir, "transcript.txt")
            if os.path.exists(transcript_file):
                with open(transcript_file, "r") as f:
                    transcript = f.read()
                st.success("✅ Transcription Complete!")
                st.text_area("📄 Transcript:", transcript, height=300)
            else:
                st.error("❌ Transcription complete, but output file not found.")
        else:
            st.error(f"❌ Error in transcription:\n{process.stderr}")
