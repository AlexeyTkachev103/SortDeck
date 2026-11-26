import os
import secrets
import uuid
import zipfile
from flask import Flask, render_template, request, redirect, session, send_file
import pandas as pd

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form['topic']
        image_column = request.form.get('image_column') or None
        file = request.files['file']

        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.json'):
            df = pd.read_json(file)
        else:
            return "Формат не поддерживается."

        session_id = str(uuid.uuid4())
        session['id'] = session_id
        session['topic'] = topic
        session['image_column'] = image_column
        session['index'] = 0
        session['yes'] = []
        session['no'] = []

        path = os.path.join(UPLOAD_FOLDER, session_id)
        os.makedirs(path, exist_ok=True)
        df.to_json(os.path.join(path, 'data.json'), orient='records')

        return redirect('/sort')
    return render_template('index.html')



@app.route('/sort', methods=['GET', 'POST'])
def sort():
    session_id = session.get('id')
    if not session_id:
        return redirect('/')
    path = os.path.join(UPLOAD_FOLDER, session_id)
    data_path = os.path.join(path, 'data.json')
    df = pd.read_json(data_path)

    index = session['index']
    if index >= len(df):
        return redirect('/result')

    item = df.iloc[index].to_dict()

    # Извлечение URL изображения
    image_url = None
    image_column = session.get('image_column')
    if image_column and image_column in item:
        parts = str(item[image_column]).split()
        for part in parts:
            if part.startswith('http') and ('.jpg' in part or '.png' in part):
                image_url = part
                break

    return render_template('sort.html',
                           item=item,
                           index=index + 1,
                           total=len(df),
                           topic=session['topic'],
                           image_url=image_url,
                           image_column=image_column)



@app.route('/swipe/<direction>', methods=['POST'])
def swipe(direction):
    index = session['index']
    session['index'] += 1
    item = request.json['item']
    if direction == 'right':
        session['yes'].append(item)
    else:
        session['no'].append(item)
    return {'status': 'ok'}


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/download')
def download():
    session_id = session['id']
    path = os.path.join(UPLOAD_FOLDER, session_id)

    df_yes = pd.DataFrame(session['yes'])
    df_no = pd.DataFrame(session['no'])

    df_yes.to_csv(os.path.join(path, 'yes.csv'), index=False)
    df_no.to_csv(os.path.join(path, 'no.csv'), index=False)

    zip_path = os.path.join(path, 'sorted.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(os.path.join(path, 'yes.csv'), 'yes.csv')
        zipf.write(os.path.join(path, 'no.csv'), 'no.csv')

    return send_file(zip_path, as_attachment=True)


if __name__ == '__main__':
    app.run()