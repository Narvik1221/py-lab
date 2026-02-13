import os
import uuid
from flask import Flask, render_template, request, url_for, send_from_directory
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import image_utils as img_utils


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard-to-guess-secret-key'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdeR2osAAAAAA6-Vm6Z_pgitdi4mKj4s6hWCbvv'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdeR2osAAAAAHlvseS5WjyY4JU-0W_9gcj7augO'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['HISTOGRAM_FOLDER'] = os.path.join(BASE_DIR, 'static', 'histograms')

# Создаём папки, если их нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['HISTOGRAM_FOLDER'], exist_ok=True)


Bootstrap(app)

class ResizeForm(FlaskForm):
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    scale = FloatField('Scale factor', validators=[
        DataRequired(),
        NumberRange(min=0.1, max=5.0, message='Scale must be between 0.1 and 5.0')
    ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Resize')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ResizeForm()
    original_img = None
    resized_img = None
    hist_original = None
    hist_resized = None

    if form.validate_on_submit():
        # Генерируем уникальный идентификатор для файлов
        unique_id = str(uuid.uuid4())
        uploaded_file = form.image.data
        filename = secure_filename(uploaded_file.filename)

        # Сохраняем оригинал
        orig_path = os.path.join(app.config['UPLOAD_FOLDER'], f'orig_{unique_id}_{filename}')
        uploaded_file.save(orig_path)

        # Изменяем размер
        scale = form.scale.data
        resized_path = os.path.join(app.config['UPLOAD_FOLDER'], f'resized_{unique_id}_{filename}')
        img_utils.resize_image(orig_path, resized_path, scale)

        # Строим гистограммы
        hist_orig_path = os.path.join(app.config['HISTOGRAM_FOLDER'], f'hist_orig_{unique_id}.png')
        hist_resized_path = os.path.join(app.config['HISTOGRAM_FOLDER'], f'hist_resized_{unique_id}.png')
        img_utils.create_histogram(orig_path, hist_orig_path)
        img_utils.create_histogram(resized_path, hist_resized_path)

        # Формируем URL для отображения в шаблоне
        original_img = url_for('static', filename=f'uploads/orig_{unique_id}_{filename}')
        resized_img = url_for('static', filename=f'uploads/resized_{unique_id}_{filename}')
        hist_original = url_for('static', filename=f'histograms/hist_orig_{unique_id}.png')
        hist_resized = url_for('static', filename=f'histograms/hist_resized_{unique_id}.png')

    return render_template('index.html', form=form,
                           original_img=original_img,
                           resized_img=resized_img,
                           hist_original=hist_original,
                           hist_resized=hist_resized)

# Для корректной раздачи статических файлов (если потребуется)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)