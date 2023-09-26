import asyncio
import os
from typing import List

import openai
import streamlit as st
from deepgram import Deepgram
from dotenv import find_dotenv, load_dotenv

from filigree.personas import PERSONAS

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4"


def form_select(opt):
    return opt[1]
async def analyze_audio(file, options):
    if options is None:
        options = {"punctuate": True}
    dg_key = os.environ.get("DEEPGRAM_API_KEY")
    if dg_key is None:
        raise ValueError("Please set the DEEPGRAM_API_KEY environment variable")
    deepgram = Deepgram(dg_key)
    source = {"buffer": file, "mimetype": file.type}
    response = await deepgram.transcription.prerecorded(source, options)
    return response

def extract_speakers(text: str) -> List[str]:
    lines = text.split("\n")
    speakers = []
    for line in lines:
        parts = line.split(":")
        if len(parts) > 1:
            speaker = parts[0].strip()
            if speaker not in speakers:
                speakers.append(speaker)
    return speakers

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # Streamlit App
    st.title("Filigree")
    file_buffer = st.file_uploader("Upload an audio file", type=["wav", "flac", "mp3", "mp4", "m4a"])
    if file_buffer is not None:
        st.write("Audio file uploaded successfully!")
        st.session_state["audio_upload"] = True
        st.audio(file_buffer.read(), format=file_buffer.type)
        file_buffer.seek(0) # reset file pointer to beginning of file

    if "audio_upload" in st. session_state and st.session_state["audio_upload"]:
        options = st.multiselect(
            "Select options for transcription",
            [("punctuate", "punctuate"), 
            ("smart_format", "smart formatting"),
            ("utterances", "split into utterances"),
            ("profanity_filter", "remove profanity"), 
            ("diarize", "is a conversation")],
            [("punctuate", "punctuate"),
            ("smart_format", "smart formatting"),
            ("utterances", "split into utterances"),
            ("diarize", "is a conversation")], 
            format_func=form_select
        )
        transcription_options = dict(zip([opt[0] for opt in options], [True for opt in options]))
        transcription_options["language"] = "en-US"
        transcription_options["detect_language"] = True
        transcription_options["tier"] = "enhanced"
        transcription_options["model"] = "meeting"# "general" # conversationalai, meeting
        transcribe_click = st.button("Transcribe")
        if transcribe_click:
            st.session_state["transcribe_click"] = True


    if "transcribe_click" in st.session_state and \
        (st.session_state["transcribe_click"] and "transcribe_success" not in st.session_state):
        st.session_state["transcript"] = "Unsuccessful"
        with st.spinner("Transcribing..."):
            results = asyncio.run(analyze_audio(file_buffer, transcription_options))
            st.session_state["transcribe_success"] = True
            if "smart_format" in transcription_options.keys() and "diarize" in transcription_options.keys():
                transcript = results["results"]["channels"][0]["alternatives"][0]["paragraphs"]["transcript"]
                st.session_state["transcript"] = transcript
                st.success("Transcription successful!")

    # Update Transcriptions
    if "transcribe_success" in st.session_state and \
        (st.session_state["transcribe_success"] and "transcript_update" not in st.session_state):
        transcript_box = st.text_area("Original Transcript", st.session_state["transcript"], height=300)
        speakers = extract_speakers(st.session_state["transcript"])
        new_speakers = dict()
        with st.form(key="speaker_update_form"):
            for speaker in speakers:
                new_speakers[speaker] = st.text_input(f"Enter name for {speaker}") 
            submit_button = st.form_submit_button(label="Update Transcript")
            if submit_button:
                for speaker in speakers:
                    new_speaker = new_speakers[speaker]
                    st.session_state["transcript"] = st.session_state["transcript"].replace(speaker + ":", new_speaker + ":")
                st.session_state["transcript_update"] = True
                st.session_state["num_speakers"] = len(extract_speakers(st.session_state["transcript"]))

    # Display updated transcript
    if "transcript_update" in st.session_state and st.session_state["transcript_update"]:
        transcript_box = st.text_area("Updated Transcript", st.session_state["transcript"], height=300)

    # Select Persona
    persona = st.selectbox("Select Persona Type", ["Default", "Therapist", "Critic"])
    persona_template = PERSONAS[persona.lower()]
    container = st.container()
    if "transcribe_success" in st.session_state and st.session_state["transcribe_success"]:
        st.write("##### Chat with the transcription via the Persona selected.")
        with container:
            if "openai_model" not in st.session_state:
                st.session_state["openai_model"] = OPENAI_MODEL

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Input"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    system_content = persona_template.format(conversation=st.session_state["transcript"], number=st.session_state["num_speakers"])
                    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    messages = [{"role": "system", "content": system_content}] + messages
                    for response in openai.ChatCompletion.create(
                        model=st.session_state["openai_model"],
                        messages=messages,
                        stream=True,
                    ):
                        full_response += response.choices[0].delta.get("content", "")
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
