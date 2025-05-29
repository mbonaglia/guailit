# Path: guailit/tests/test_guailit.py
# -*- coding: utf-8 -*-
"""
Unit tests for the guailit library.
"""

__author__ = "Marco Bonaglia"
__version__ = "0.1.0"
__date__ = "2023-10-27" # Placeholder: Update with actual creation date

import pytest
from unittest.mock import patch, MagicMock
import io
from PIL import Image

# We need to adjust the path to import modules from the parent directory (guailit)
import sys
import os

# Add the parent directory (guailit) to the Python path
guailit_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if guailit_path not in sys.path:
    sys.path.append(guailit_path)

# Import the app module from guailit
# We will mock the fastlabio import in the tests
from guailit import app

# Mock the fastlabio library and its modules
@pytest.fixture
def mock_fastlabio():
    with patch('guailit.app.motor') as mock_motor, \
         patch('guailit.app.camera') as mock_camera, \
         patch('streamlit.write') as mock_st_write, \
         patch('streamlit.success') as mock_st_success, \
         patch('streamlit.error') as mock_st_error, \
         patch('streamlit.info') as mock_st_info, \
         patch('streamlit.warning') as mock_st_warning, \
         patch('streamlit.image') as mock_st_image:

        # Configure the mock objects
        mock_motor.get_motor_position.return_value = 10.5
        # Create a dummy JPEG byte string for camera tests
        dummy_image = Image.new('RGB', (10, 10), color = 'red')
        byte_io = io.BytesIO()
        dummy_image.save(byte_io, 'JPEG')
        mock_camera.get_single_frame.return_value = byte_io.getvalue()

        yield mock_motor, mock_camera, mock_st_write, mock_st_success, mock_st_error, mock_st_info, mock_st_warning, mock_st_image

# Test motor actions
def test_move_motor_action(mock_fastlabio):
    mock_motor, _, mock_st_write, mock_st_success, mock_st_error, _, _, _ = mock_fastlabio
    
    test_position = 20.0
    app.move_motor_action(test_position)
    
    mock_motor.move_motor.assert_called_once_with(test_position)
    mock_st_write.assert_called_once_with(f"Attempting to move motor to {test_position}...")
    mock_st_success.assert_called_once_with(f"Motor move command sent for position: {test_position}")
    mock_st_error.assert_not_called()

def test_set_motor_speed_action(mock_fastlabio):
    mock_motor, _, mock_st_write, mock_st_success, mock_st_error, _, _, _ = mock_fastlabio
    
    test_speed = 5.0
    app.set_motor_speed_action(test_speed)
    
    mock_motor.set_motor_speed.assert_called_once_with(test_speed)
    mock_st_write.assert_called_once_with(f"Attempting to set motor speed to {test_speed}...")
    mock_st_success.assert_called_once_with(f"Motor speed set to: {test_speed}")
    mock_st_error.assert_not_called()

def test_get_motor_position_action(mock_fastlabio):
    mock_motor, _, mock_st_write, mock_st_success, mock_st_error, mock_st_info, _, _ = mock_fastlabio
    
    app.get_motor_position_action()
    
    mock_motor.get_motor_position.assert_called_once()
    mock_st_info.assert_called_once_with(f"Current Motor Position: {mock_motor.get_motor_position.return_value}")
    mock_st_write.assert_not_called()
    mock_st_success.assert_not_called()
    mock_st_error.assert_not_called()

# Test camera actions
def test_set_exposure_action(mock_fastlabio):
    _, mock_camera, mock_st_write, mock_st_success, mock_st_error, _, _, _ = mock_fastlabio
    
    test_exposure = 1000.0
    app.set_exposure_action(test_exposure)
    
    mock_camera.set_exposure.assert_called_once_with(test_exposure)
    mock_st_write.assert_called_once_with(f"Attempting to set exposure time to {test_exposure} us...")
    mock_st_success.assert_called_once_with(f"Exposure time set to: {test_exposure} us")
    mock_st_error.assert_not_called()
    
def test_set_gain_action(mock_fastlabio):
    _, mock_camera, mock_st_write, mock_st_success, mock_st_error, _, _, _ = mock_fastlabio
    
    test_gain = 1.5
    app.set_gain_action(test_gain)
    
    mock_camera.set_gain.assert_called_once_with(test_gain)
    mock_st_write.assert_called_once_with(f"Attempting to set gain to {test_gain}...")
    mock_st_success.assert_called_once_with(f"Gain set to: {test_gain}")
    mock_st_error.assert_not_called()

def test_get_single_frame_action(mock_fastlabio):
    _, mock_camera, mock_st_write, mock_st_success, mock_st_error, _, mock_st_warning, mock_st_image = mock_fastlabio
    
    app.get_single_frame_action()
    
    mock_camera.get_single_frame.assert_called_once()
    mock_st_write.assert_called_once_with("Acquiring single frame...")
    mock_st_image.assert_called_once() # Check if st.image was called
    mock_st_success.assert_called_once_with("Single frame acquired and displayed.")
    mock_st_warning.assert_not_called()
    mock_st_error.assert_not_called()

# Test case for when get_single_frame returns no data
def test_get_single_frame_action_no_data(mock_fastlabio):
    _, mock_camera, mock_st_write, mock_st_success, mock_st_error, _, mock_st_warning, mock_st_image = mock_fastlabio
    
    mock_camera.get_single_frame.return_value = None # Simulate no data returned
    
    app.get_single_frame_action()
    
    mock_camera.get_single_frame.assert_called_once()
    mock_st_write.assert_called_once_with("Acquiring single frame...")
    mock_st_warning.assert_called_once_with("No frame received.")
    mock_st_image.assert_not_called()
    mock_st_success.assert_not_called()
    mock_st_error.assert_not_called()

# Example Test: Test motor position display
# Note: Testing Streamlit UI directly is complex. These tests focus on 
# ensuring that the underlying fastlabio functions would be called correctly.
# For full UI testing, consider using streamlit.testing (more involved).
def test_get_motor_position_button(mock_fastlabio):
    mock_motor, _ = mock_fastlabio

    # Simulate clicking the 'Get Current Position' button in Streamlit
    # This part is conceptual as directly simulating button clicks in unit tests is tricky
    # We would typically test the function that the button *calls*.
    # Let's assume a function in app.py that the button triggers.

    # To properly test this, we might need to refactor app.py to have separate
    # functions for button actions that we can call and test here.

    # For demonstration, let's test the underlying fastlabio call indirectly
    # by seeing if the mock was called.
    
    # This requires a change in app.py to make the button logic testable.
    # For now, this test is a placeholder and a reminder to refactor app.py
    # to extract button actions into testable functions.
    
    # Example of how you *would* check if the fastlabio function was called
    # if the app structure supported it:
    # mock_motor.get_motor_position.assert_called_once()
    pass # Placeholder test

# Add more tests here for other functionalities (move, set speed, camera control)

# Example Placeholder Test for setting motor speed
def test_set_motor_speed(mock_fastlabio):
    mock_motor, _ = mock_fastlabio
    
    # Simulate setting speed via the UI and clicking the button.
    # This needs testable functions in app.py
    
    # Example check if the fastlabio function was called:
    # test_speed = 5.0
    # mock_motor.set_motor_speed.assert_called_once_with(test_speed)
    pass # Placeholder test

# Example Placeholder Test for setting camera exposure
def test_set_camera_exposure(mock_fastlabio):
    _, mock_camera = mock_fastlabio
    
    # Simulate setting exposure via the UI and clicking the button.
    # This needs testable functions in app.py
    
    # Example check if the fastlabio function was called:
    # test_exposure = 1000.0
    # mock_camera.set_exposure.assert_called_once_with(test_exposure)
    pass # Placeholder test 