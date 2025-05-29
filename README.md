# Path: guailit/README.md
# -*- coding: utf-8 -*-
"""
README for the guailit library.
"""

__author__ = "Marco Bonaglia"
__version__ = "0.1.0"
__date__ = "2023-10-27" # Placeholder: Update with actual creation date

# guailit: Streamlit Web Interface for fastlabio

`guailit` is a Python library that provides a web-based graphical user interface (GUI) using the `streamlit` package to control and monitor the functionalities exposed by the `fastlabio` library (motor and camera).

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Navigate to the `guailit` directory:**

    ```bash
    cd guailit
    ```

3.  **Create and activate a conda environment (recommended):**

    ```bash
    conda create -n guailit python=3.9
    conda activate guailit
    ```

4.  **Install the required packages:**

    Make sure the `fastlabio` library is accessible (e.g., cloned in the same parent directory as `guailit`).

    ```bash
    pip install streamlit fastapi uvicorn pysilico plico_motor opencv-python
    # If fastlabio is not installed as a package, you might need to add its path
    # to your Python environment or install it locally.
    ```

## Usage

1.  **Ensure your `fastlabio` servers (motor and camera) are running.**

2.  **Activate the conda environment:**

    ```bash
    conda activate guailit
    ```

3.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

    This will open the application in your web browser.

## Development

### Running Tests

1.  **Activate the conda environment:**

    ```bash
    conda activate guailit
    ```

2.  **Navigate to the `guailit` directory:**

    ```bash
    cd guailit
    ```

3.  **Run pytest:**

    ```bash
    pytest
    ```

## Project Structure

```
git/
├── fastlabio/
│   ├── camera.py
│   ├── motor.py
│   └── ...
└── guailit/
    ├── __init__.py
    ├── app.py
    ├── README.md
    └── tests/
        └── test_guailit.py
```

## Contributing

(Add contributing guidelines here)

## License

(Add license information here)