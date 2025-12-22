# Card Sort App

A simple web application for sorting data from a CSV or JSON file.

## How to Use

1.  **Run the application:**

    ```bash
    flask run
    ```

2.  **Open the application in your browser:**

    Go to `http://127.0.0.1:5000`

3.  **Upload your data:**

    *   Click "Choose File" and select a CSV or JSON file.
    *   Enter a "topic" for your sorting session.
    *   If your file contains a column with image URLs, enter the column name in the "Image column name" field.
    *   Click "Upload".

4.  **Sort your data:**

    *   The application will display one item at a time from your file.
    *   Click "Yes" or use the right arrow key (→) to add the item to the "yes" list.
    *   Click "No" or use the left arrow key (←) to add the item to the "no" list.

5.  **Download your results:**

    *   After sorting all the items, you will be taken to a results page.
    *   Click "Download result" to download a zip file containing `yes.csv` and `no.csv`.

