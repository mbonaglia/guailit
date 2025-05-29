# Work Plan for guailit Library (Streamlit Web Interface for fastlabio)

## Project Goal
Create a Python library `guailit` that provides a web-based graphical user interface (GUI) using the `streamlit` package to control and monitor the functionalities exposed by the `fastlabio` library (motor and camera).

## Analysis of fastlabio Capabilities
Based on the analysis of `fastlabio/motor.py` and `fastlabio/camera.py`, the following key functionalities are available:

### Motor Module (`fastlabio.motor`)
- `move_motor(position: float)`: Move the motor to a specified absolute position.
- `get_motor_position() -> float`: Get the current position of the motor.
- `set_motor_speed(speed: float)`: Set the speed of the motor.

### Camera Module (`fastlabio.camera`)
- `get_single_frame() -> bytes (JPEG)`: Acquire a single image frame and return it as a JPEG byte stream.
- `set_exposure(exposure_time_us: float)`: Set the camera exposure time in microseconds.
- `set_gain(gain: float)`: Set the camera gain.
- `websocket_camera_stream()`: WebSocket endpoint for streaming real-time camera frames (this will require a different approach in Streamlit, likely involving periodic image updates rather than a direct WebSocket).

## Work Plan

### Phase 1: Setup and Basic Structure
1.  **Set up the development environment**:
    *   Ensure the `conda petalometer Environment` is active.
    *   Install necessary packages: `streamlit`, `fastapi`, `uvicorn`, `pysilico`, `plico_motor`, `opencv-python`.
2.  **Create the basic `guailit` library structure**:
    *   Create an `__init__.py` file.
    *   Create a main Streamlit application file (e.g., `app.py`).
3.  **Basic Streamlit App**:
    *   Create a simple Streamlit app that displays a title and some introductory text.

### Phase 2: Integrate Motor Control
1.  **Import `fastlabio.motor`**:
    *   Import the necessary functions from the `fastlabio.motor` module.
2.  **Implement Motor Control GUI**:
    *   Add input fields for target position and speed.
    *   Add buttons for "Move" and "Set Speed".
    *   Add a display area for the current motor position, updated periodically or on button click.
    *   Implement the logic to call the corresponding `fastlabio.motor` functions when buttons are clicked.
    *   Add error handling and feedback to the user interface.

### Phase 3: Integrate Camera Control
1.  **Import `fastlabio.camera`**:
    *   Import the necessary functions from the `fastlabio.camera` module.
2.  **Implement Camera Control GUI**:
    *   Add input fields for exposure time and gain.
    *   Add buttons for "Set Exposure" and "Set Gain".
    *   Add a button to acquire and display a single frame.
    *   Implement the logic to call the corresponding `fastlabio.camera` functions.
    *   Add error handling and feedback.
3.  **Implement Camera Streaming (Streamlit Approach)**:
    *   Since direct WebSocket streaming is not a native Streamlit feature for displaying images, explore methods for periodic image updates:
        *   Use `st.image` in a loop with `time.sleep` and a button to start/stop streaming.
        *   Consider using `st.empty` to update the image in place.
    *   Implement the logic to acquire frames from `fastlabio.camera` periodically and display them.

### Phase 4: Refinement and Testing
1.  **Refactor Code**:
    *   Apply the "AI-Optimized Modularity (AOM) Principle" by creating lean, focused files if the application grows.
    *   Ensure code adheres to PEP 8 and includes type hints and docstrings.
2.  **Add Tests**:
    *   Write unit tests for the `guailit` functions that interact with `fastlabio`, using `pytest`.
    *   Consider integration tests for the Streamlit application, potentially using `streamlit.testing`.
3.  **Documentation**:
    *   Add README.md to the `guailit` directory explaining how to install and run the application.
    *   Add docstrings to all functions and classes.

## Considerations and Open Questions
*   **Error Handling**: How should errors from `fastlabio` be displayed to the user in the Streamlit interface?
*   **Concurrency**: How to handle potentially blocking calls to `fastlabio` functions within the asynchronous nature of Streamlit (though Streamlit itself is not async)? Using `asyncio.to_thread` within `fastlabio` helps, but Streamlit's execution model needs consideration.
*   **GUI Framework**: The request specifically mentions `streamlit`. The project instructions for `petalometer` mention `guietta`. For this specific library, `streamlit` is the target, but this difference should be noted if future GUI development within the broader project occurs.
*   **Configuration**: How will the connection parameters for `fastlabio` (host, port) be configured in the `guailit` app? (e.g., environment variables, a configuration file, or input fields in the GUI).

## Next Steps
Proceed with Phase 1: Environment setup and basic Streamlit app structure. 