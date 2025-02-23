from flask import Flask, request, render_template, send_file
from PIL import Image, ImageOps
import io

app = Flask(__name__)

def apply_filter(image):
    return ImageOps.grayscale(image)  # Przykładowy filtr (czarno-biały)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Brak pliku!"
        file = request.files['file']
        if not  file or file.filename == '':
            return "Błąd: Nie wybrano pliku lub plik jest uszkodzony", 400

try:
    file = request.files['file']
    image = Image.open(file)
except Exception as e:
    return f"Błąd podczas otwierania obrazu: {str(e)}", 500
        
        image = Image.open(file)
        processed_image = apply_filter(image)

        img_io = io.BytesIO()
        processed_image.save(img_io, 'JPEG', quality=90)
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
from flask import Flask, request, render_template, send_file
from PIL import Image, ImageOps
import io

app = Flask(__name__)  # Tworzymy aplikację Flask

def apply_filter(image, filter_type):
    if filter_type == "wood_lamp":
        return ImageOps.colorize(ImageOps.grayscale(image), black="blue", white="purple")
    elif filter_type == "hdr":
        return ImageOps.autocontrast(image, cutoff=10)
    elif filter_type == "oily_skin":
        return ImageOps.colorize(ImageOps.grayscale(image), black="yellow", white="red")
    elif filter_type == "hydration":
        return ImageOps.colorize(ImageOps.grayscale(image), black="cyan", white="lightblue")
    elif filter_type == "pigmentation":
        return ImageOps.colorize(ImageOps.grayscale(image), black="brown", white="orange")
    elif filter_type == "infrared":
        return ImageOps.colorize(ImageOps.grayscale(image), black="red", white="white")
    else:
        return image

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Brak pliku"
        file = request.files['file']
        if file.filename == '':
            return "Nie wybrano pliku"
        
        image = Image.open(file).convert("L")
        filters = ["wood_lamp", "hdr", "oily_skin", "hydration", "pigmentation", "infrared"]
        processed_images = [apply_filter(image, f) for f in filters]

        collage_width = 3
        collage_height = 2
        collage = Image.new('RGB', (image.width * collage_width, image.height * collage_height))

        for i, img in enumerate(processed_images):
            x_offset = (i % collage_width) * image.width
            y_offset = (i // collage_width) * image.height
            collage.paste(img, (x_offset, y_offset))

        img_io = io.BytesIO()
        collage.save(img_io, 'JPEG', quality=90)
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg')
    
    return render_template('index.html')

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=10000)
