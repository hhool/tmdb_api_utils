# HOWTO

## How to use python on venv

To run Python with a virtual environment (venv) in Visual Studio Code, follow these steps:

**Create a virtual environment**:
   Open a terminal in Visual Studio Code and run the following command to create a virtual environment named `.venv`:

```bash
    python3 -m venv .venv
```

**Activate the virtual environment**:

On macOS/Linux:

```bash
    source .venv/bin/activate
```

On Windows:

```bash
    .venv\Scripts\activate
```

**Select the virtual environment in VS Code**:

   Use the **Python: Select Interpreter** command to select the virtual environment you just created.

Show in Command Palette

**Install necessary packages**:
   With the virtual environment activated, install any required packages using `pip`. For example:

```bash
    pip install requests
```

**Run your Python script**:
   You can run your Python script in the terminal by using the following command:

```bash
    python tmdb-api-a-z.py
```

By following these steps, you can run your Python script within a virtual environment in Visual Studio Code.
