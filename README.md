# Card Sort App

A small web app for sorting records from a CSV or JSON file. Upload a file, choose a topic, mark each record Yes or No, then download the results as CSV files in a ZIP archive.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for installing dependencies and running the app

## Start the app

From the project directory, run:

```bash
uv run app.py
```

uv creates the virtual environment and installs the dependencies from `uv.lock` the first time you run it. To install them separately, use `uv sync`.

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Press `Ctrl+C` in the terminal to stop the server.

## Use

- Upload a CSV or JSON file and enter a topic.
- Optionally provide the name of the column containing image URLs.
- Choose Yes or No for each record, or use the right and left arrow keys.
- Download the completed sort as a ZIP containing `yes.csv` and `no.csv`.

For deployments beyond local development, set a private `SECRET_KEY` environment variable. The app generates a temporary key automatically when one is not configured.

