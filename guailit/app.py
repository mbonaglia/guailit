# Path: guailit/app.py
# -*- coding: utf-8 -*-
"""
Main Streamlit application for the guailit library.

This file contains the core structure of the Streamlit web interface
for interacting with the fastlabio library.
"""

__author__ = "Marco Bonaglia"
__version__ = "0.1.0"
__date__ = "2023-10-27" # Placeholder: Update with actual creation date

from fastlabio import camera
import streamlit as st
import time # Import time for periodic updates
import io # Import io for image handling
from PIL import Image # Import Image from Pillow
import asyncio # Import asyncio

# Import the synchronous camera getter from fastlabio
from fastlabio.camera import get_pysilico_camera_sync

try:
    from fastlabio import motor # Import both motor and camera modules
except ImportError as e:
    st.error(f"Could not import fastlabio modules. Make sure fastlabio is accessible in the Python path. Error: {e}")
    motor = None # Set motor to None if import fails
    camera = None # Set camera to None if import fails

# --- Helper functions for interacting with fastlabio (more testable) ---
def move_motor_action(position: float):
    """
    Action to move the motor to a specified position.
    """
    if motor is not None:
        try:
            st.write(f"Attempting to move motor to {position}...")
            motor.move_motor(position)
            st.success(f"Motor move command sent for position: {position}")
        except Exception as e:
            st.error(f"Error moving motor: {e}")
    else:
        st.error("Motor module not loaded.")

def set_motor_speed_action(speed: float):
    """
    Action to set the motor speed.
    """
    if motor is not None:
        try:
            st.write(f"Attempting to set motor speed to {speed}...")
            motor.set_motor_speed(speed)
            st.success(f"Motor speed set to: {speed}")
        except Exception as e:
            st.error(f"Error setting motor speed: {e}")
    else:
        st.error("Motor module not loaded.")

def get_motor_position_action():
    """
    Action to get and display the current motor position.
    """
    if motor is not None:
        try:
            current_position = motor.get_motor_position()
            st.info(f"Current Motor Position: {current_position}")
        except Exception as e:
            st.error(f"Error getting motor position: {e}")
    else:
        st.error("Motor module not loaded.")

def set_exposure_action(exposure_time: float):
    """
    Action to set the camera exposure time.
    """
    if camera is not None:
        try:
            st.write(f"Attempting to set exposure time to {exposure_time} us...")
            camera.set_exposure(exposure_time)
            st.success(f"Exposure time set to: {exposure_time} us")
        except Exception as e:
            st.error(f"Error setting exposure time: {e}")
    else:
        st.error("Camera module not loaded.")

def set_gain_action(gain_value: float):
    """
    Action to set the camera gain.
    """
    if camera is not None:
        try:
            st.write(f"Attempting to set gain to {gain_value}...")
            camera.set_gain(gain_value)
            st.success(f"Gain set to: {gain_value}")
        except Exception as e:
            st.error(f"Error setting gain: {e}")
    else:
        st.error("Camera module not loaded.")

async def get_single_frame_action():
    """
    Action to acquire and display a single frame from the camera.
    """
    # Get the camera instance using the new synchronous function
    camera_instance = get_pysilico_camera_sync()

    if camera_instance is not None:
        try:
            st.write("Acquiring single frame...")
            # Use getFutureFrames(1) to get a frame
            frame_object = await asyncio.to_thread(camera_instance.getFutureFrames, 1)

            if frame_object:
                # Assuming the frame object has a toNumpyArray() method
                frame = frame_object.toNumpyArray()

                # Encode the frame to JPEG format (using a basic approach for now)
                # This might need adjustment based on the actual frame object type and content
                # If the frame is already a numpy array, cv2.imencode should work.
                import cv2
                is_success, buffer = cv2.imencode(".jpg", frame)
                if is_success:
                    jpeg_bytes = buffer.tobytes()
                    image = Image.open(io.BytesIO(jpeg_bytes))
                    st.image(image, caption="Single Frame")
                    st.success("Single frame acquired and displayed.")
                else:
                    st.error("Could not encode frame to JPEG.")

            else:
                st.warning("No frames received.")
        except Exception as e:
            st.error(f"Error acquiring or displaying frame: {e}")
    else:
        st.error("Camera connection not available.") # Update error message

def render_motor_control():
    """
    Renders the motor control section in the Streamlit app.
    """
    st.header("Motor Control")

    if motor is not None:
        # Input for target position
        target_position = st.number_input("Enter Target Position:", step=0.01, key='motor_pos_input')

        # Button to move motor
        if st.button("Move Motor", key='move_motor_button'):
            move_motor_action(target_position)

        st.markdown("---") # Separator

        # Input for speed
        target_speed = st.number_input("Enter Target Speed:", step=0.01, min_value=0.0, key='motor_speed_input')

        # Button to set speed
        if st.button("Set Motor Speed", key='set_speed_button'):
            set_motor_speed_action(target_speed)

        st.markdown("---") # Separator

        # Display current position
        if st.button("Get Current Position", key='get_position_button'):
            get_motor_position_action()

    else:
        st.warning("Motor module not loaded due to import error.")

async def render_camera_control():
    """
    Renders the camera control section and stream in the Streamlit app.
    """
    st.markdown("===") # Larger separator
    st.header("Camera Control")

    if camera is not None:
        # Input for exposure time
        exposure_time = st.number_input("Set Exposure Time (us):", min_value=0.0, key='exposure_input')

        # Button to set exposure time
        if st.button("Set Exposure", key='set_exposure_button'):
            set_exposure_action(exposure_time)

        st.markdown("---") # Separator

        # Input for gain
        gain_value = st.number_input("Set Gain:", min_value=0.0, key='gain_input')

        # Button to set gain
        if st.button("Set Gain", key='set_gain_button'):
            set_gain_action(gain_value)

        st.markdown("---") # Separator

        # Button to get a single frame
        if st.button("Get Single Frame", key='get_frame_button'):
            # Await the async function directly within the running event loop
            await get_single_frame_action()

        st.markdown("---") # Separator

        # --- Camera Streaming Section (Periodic Update) ---
        st.subheader("Camera Stream")
        st.write("Click the button below to start/stop the camera stream (periodic updates).")

        if 'streaming' not in st.session_state:
            st.session_state.streaming = False

        # Note: Camera instance for streaming is now handled by get_pysilico_camera_sync
        # in the while loop to ensure it's acquired within the loop's context.
        # The start button primarily toggles the 'streaming' state.
        if st.button('Start Streaming', key='start_stream_button'):
            # Get the camera instance for streaming and store in session state
            st.session_state.camera_instance_stream = get_pysilico_camera_sync()
            if st.session_state.camera_instance_stream:
                st.session_state.streaming = True
                # Trigger the first frame acquisition by rerunning the script
                st.rerun()
            else:
                st.error("Could not connect to camera for streaming.")

        if st.button('Stop Streaming', key='stop_stream_button'):
            st.session_state.streaming = False
            # Close the camera connection when stopping stream
            if 'camera_instance_stream' in st.session_state and st.session_state.camera_instance_stream:
                try:
                    st.session_state.camera_instance_stream.close()
                except AttributeError:
                    pass
                finally:
                    del st.session_state.camera_instance_stream
            # Rerun to update the UI and stop the streaming loop
            st.rerun()

        # Separate async function to stream a single frame
        async def stream_single_frame():
            if st.session_state.streaming and 'camera_instance_stream' in st.session_state and st.session_state.camera_instance_stream:
                st.write("Streaming... (Click 'Stop Streaming' to end)")
                image_placeholder = st.empty()

                camera_instance_stream = st.session_state.camera_instance_stream

                try:
                    # Use getFutureFrames(1) for streaming
                    # Await the async function directly
                    frame_object = await asyncio.to_thread(camera_instance_stream.getFutureFrames, 1)

                    if frame_object:
                        frame = frame_object.toNumpyArray()

                        # Encode and display frame
                        import cv2
                        is_success, buffer = cv2.imencode(".jpg", frame)
                        if is_success:
                            jpeg_bytes = buffer.tobytes()
                            image = Image.open(io.BytesIO(jpeg_bytes))
                            image_placeholder.image(image)
                        else:
                            st.error("Could not encode frame to JPEG in stream.")

                    # Add a small delay
                    await asyncio.sleep(0.05)

                except Exception as e:
                    st.error(f"Error during streaming: {e}")
                    st.session_state.streaming = False
                    if 'camera_instance_stream' in st.session_state and st.session_state.camera_instance_stream:
                         try:
                             st.session_state.camera_instance_stream.close()
                         except AttributeError:
                             pass
                         finally:
                             del st.session_state.camera_instance_stream
                finally:
                    # If streaming is still active, rerun the script to get the next frame
                    if st.session_state.streaming:
                         st.rerun()

            elif st.session_state.streaming and ('camera_instance_stream' not in st.session_state or not st.session_state.camera_instance_stream):
                 st.error("Streaming is active but camera instance is not available.")
                 st.session_state.streaming = False

        # Call the async single frame streaming function if streaming is active
        if st.session_state.streaming:
            # Await the async streaming function directly
            await stream_single_frame()

    else:
        st.warning("Camera module not loaded due to import error.")

def main():
    """
    Main function to run the Streamlit application.
    """
    st.title("fastlabio Web Interface (guailit)")
    st.write("Welcome to the fastlabio web interface built with Streamlit.")
    st.write("Use the sections below to control the motor and camera.")

    render_motor_control()
    # Run the async camera control rendering function
    asyncio.run(render_camera_control())

if __name__ == "__main__":
    main() 