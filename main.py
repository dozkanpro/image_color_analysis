import numpy as np
from PIL import Image
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Abcde46792degb2hgh!4'
Bootstrap5(app)


class UploadForm(FlaskForm):
    image = FileField('Upload Image')
    submit = SubmitField('Upload and Analyze')


def get_top_colors(image_path, num_colors=10):
    image = Image.open(image_path)
    image_array = np.array(image)

    pixels = image_array.reshape((-1, 3))

    color_counts = np.unique(pixels, axis=0, return_counts=True)
    color_counts = list(zip(color_counts[0], color_counts[1]))
    color_counts.sort(key=lambda x: -x[1])
    top_colors = color_counts[:num_colors]

    return top_colors


@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    top_colors = None

    if form.validate_on_submit():
        uploaded_file = form.image.data

        if uploaded_file:
            image_path = f"static/images/{uploaded_file.filename}"
            uploaded_file.save(image_path)
            top_colors = get_top_colors(image_path)

    return render_template("index.html", form=form, top_colors=top_colors)


if __name__ == "__main__":
    app.run(debug=True)
