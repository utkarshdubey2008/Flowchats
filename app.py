from flask import Flask, request, send_file
from ppt_generator import create_slide_images, convert_slides_to_images
from ai_structures import get_presentation_structure
from file_utils import merge_images_to_pdf, merge_images_to_ppt
import tempfile
import os

app = Flask(__name__)

@app.route('/generate/<format>/', methods=['GET'])
def generate_presentation(format):
    prompt = request.args.get('prompt')
    if not prompt or format not in ['pdf', 'ppt']:
        return "Usage: /generate/{ppt|pdf}/?prompt=Your+Topic", 400

    presentation_data = get_presentation_structure(prompt)
    slides = create_slide_images(presentation_data)
    image_buffers = convert_slides_to_images(slides)

    temp_dir = tempfile.mkdtemp()
    image_files = []
    for idx, buf in enumerate(image_buffers):
        img_path = os.path.join(temp_dir, f"slide_{idx+1}.png")
        with open(img_path, "wb") as f:
            f.write(buf.read())
        image_files.append(img_path)

    if format == 'pdf':
        result_file = merge_images_to_pdf(image_files, temp_dir)
        mimetype = 'application/pdf'
        download_name = 'presentation.pdf'
    else:
        result_file = merge_images_to_ppt(image_files, temp_dir)
        mimetype = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        download_name = 'presentation.pptx'

    return send_file(result_file, mimetype=mimetype, as_attachment=True, download_name=download_name)

if __name__ == "__main__":
    app.run(debug=True)
