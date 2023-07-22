# Import necessary libraries
import streamlit as st
import sounddevice as sd
import numpy as np
import threading
import matplotlib.pyplot as plt

# Parameters
duration = 9  # Duration of audio recording in seconds
sampling_rate = 44100  # Sampling rate (samples per second)

# Function to record audio using Sounddevice library
def record_audio(duration, sampling_rate):
    # Set a session state variable to track recording status
    st.session_state.is_recording = True

    # Display a button to indicate recording
    st.button("Recording...")

    # Record audio using Sounddevice
    audio_data = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=1)
    sd.wait()

    # Update the button text after recording is finished
    st.button("Recording finished & Fetching Parameters from audio 👍.")

    # Update the session state variable to indicate recording is complete
    st.session_state.is_recording = False

    return audio_data

# Function to plot waveform of the audio data
def plot_waveform(audio_data, sampling_rate, title="Waveform Visualization"):
    # Create a new figure and axis using Matplotlib
    fig, ax = plt.subplots()

    # Generate time values for the x-axis based on the sampling rate
    time = np.linspace(0, len(audio_data) / sampling_rate, num=len(audio_data))

    # Plot the audio data on the axis
    ax.plot(time, audio_data[:, 0])

    # Set labels and title for the plot
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)

    # Display the plot using Streamlit's "st.pyplot()" function
    st.pyplot(fig)

# Function to play audio asynchronously using threading
def play_audio_async(audio_data, sampling_rate):
    def play():
        # Display a button to indicate audio playback
        st.button("Playing audio...")

        # Play the audio using Sounddevice
        sd.play(audio_data, samplerate=sampling_rate)
        sd.wait()

        # Update the button text after audio playback is finished
        st.button("Playback finished.")

    # Start a new thread to play the audio asynchronously
    threading.Thread(target=play).start()

# Function to extract parameters from the recorded audio
def get_parameters(audio_data, sampling_rate):
    # Extract parameters here (e.g., frequency, amplitude, etc.)
    parameters = {
        "sampling_rate": sampling_rate,
        "audio_data": audio_data,
        # Add other parameters as needed
    }
    return parameters

# Function to generate audio from parameters (reverse of capturing parameters)
def generate_audio_from_parameters(parameters):
    return parameters["audio_data"]

# Function to display audio parameters in a formatted way
def display_audio_parameters(parameters):
    st.subheader("Generated Audio Parameters:")
    for key, value in parameters.items():
        # Use custom CSS style to color the parameter names and values
        st.markdown(f"<span style='color:#3366ff'>{key}:</span> <span style='color:#008080'>{value}</span>", unsafe_allow_html=True)

# Main function that defines the Streamlit application
def main():
    # Set the title of the app
    st.title("Voice Transmission Application 📻")

    # Check if the "is_recording" session state variable exists, if not, set it to False
    if "is_recording" not in st.session_state:
        st.session_state.is_recording = False

    # If not recording, display the "Record Voice" button
    if not st.session_state.is_recording:
        if st.button("Record Voice"):
            # Record audio
            recorded_audio_data = record_audio(duration, sampling_rate)

            # Get parameters of the recorded audio
            audio_parameters = get_parameters(recorded_audio_data, sampling_rate)

            # Plot waveform of recorded audio
            st.subheader("Waveform Visualization")
            plot_waveform(recorded_audio_data, sampling_rate, title="Recorded Voice")

            # Play the recorded audio
            play_audio_async(recorded_audio_data, sampling_rate)

            # Save the audio parameters in the session state
            st.session_state.audio_parameters = audio_parameters

    # Display "Generate Voice from given audio Parameters 🤖" button outside the else block
    if "audio_parameters" in st.session_state and not st.session_state.is_recording:
        if st.button("Generate Voice from given audio Parameters 🤖"):
            # Generate audio from parameters and play it
            generated_audio_data = generate_audio_from_parameters(st.session_state.audio_parameters)
            play_audio_async(generated_audio_data, sampling_rate)

            # Display audio parameters
            display_audio_parameters(st.session_state.audio_parameters)

            # Plot waveform of generated audio
            st.subheader("Waveform Visualization (Generated Voice)🎶")
            plot_waveform(generated_audio_data, sampling_rate, title="Generated Voice")

# Run the Streamlit app if this script is executed directly
if __name__ == "__main__":
    main()
