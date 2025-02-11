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
    pip install requests openpyxl Pillow
```

**Run your Python script**:
   You can run your Python script in the terminal by using the following command:

```bash
    python your_script.py
```

For example, if you have a script named `tmdb-api-top.py`, you can run it using the following command:

```bash
    python tmdb-api-top.py --genre=16
```

For example, if you have a script named `tmdb-api-a-z.py`, you can run it using the following command:

```bash
    python tmdb-api-a-z.py  -t A
```

```bash
    python tmdb-api-a-z.py  -t A && python tmdb-api-a-z.py  -t B && python tmdb-api-a-z.py  -t C && python tmdb-api-a-z.py  -t D && python tmdb-api-a-z.py  -t E && python tmdb-api-a-z.py  -t F && python tmdb-api-a-z.py  -t G && python tmdb-api-a-z.py  -t H && python tmdb-api-a-z.py  -t I && python tmdb-api-a-z.py  -t J && python tmdb-api-a-z.py  -t K && python tmdb-api-a-z.py  -t L && python tmdb-api-a-z.py  -t M && python tmdb-api-a-z.py  -t N && python tmdb-api-a-z.py  -t O && python tmdb-api-a-z.py  -t P && python tmdb-api-a-z.py  -t Q && python tmdb-api-a-z.py  -t R && python tmdb-api-a-z.py  -t S && python tmdb-api-a-z.py  -t T && python tmdb-api-a-z.py  -t U && python tmdb-api-a-z.py  -t V && python tmdb-api-a-z.py  -t W && python tmdb-api-a-z.py  -t X && python tmdb-api-a-z.py  -t Y && python tmdb-api-a-z.py  -t Z
```

```bash
    python tmdb-api-a-z.py -t 0 && python tmdb-api-a-z.py -t 1 && python tmdb-api-a-z.py -t 2 && python tmdb-api-a-z.py -t 3 && python tmdb-api-a-z.py -t 4 && python tmdb-api-a-z.py -t 5 && python tmdb-api-a-z.py -t 6 && python tmdb-api-a-z.py -t 7 && python tmdb-api-a-z.py -t 8 && python tmdb-api-a-z.py -t 9
```

By following these steps, you can run your Python script within a virtual environment in Visual Studio Code.
