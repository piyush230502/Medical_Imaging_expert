import os
from PIL import Image as PILImage
from agno.media import Image as AgnoImage
from backend.llm import get_medical_agent
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from backend.prompt import MEDICAL_ANALYSIS_QUERY
import uuid # For unique temporary filenames
import logging

# --- Logging Configuration ---
logging.basicConfig(
                    filename='app.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# Optional: If you want to log to a file as well, uncomment the following lines
# file_handler = logging.FileHandler('app.log')
# file_handler.setLevel(logging.INFO) # Or another level
# app.logger.addHandler(file_handler)

# --- Configuration ---
# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


app = Flask(__name__, template_folder='frontend', static_folder='frontend/static')
app.secret_key = os.urandom(24) # Needed for session management
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit


@app.route('/')
def index():
    return render_template('index.html', api_key_configured=bool(session.get("GOOGLE_API_KEY")))

@app.route('/configure_api_key', methods=['POST'])
def configure_api_key():
    api_key = request.form.get('api_key')
    if api_key:
        session['GOOGLE_API_KEY'] = api_key
        logging.warning("API KEY CONFIGURED SUCCESSFULLY")
        return jsonify({'success': True, 'message': 'API Key saved!'})
    logging.warning("API Key configuration attempt failed: Key was empty.")
    return jsonify({'success': False, 'message': 'API Key cannot be empty.'}), 400

@app.route('/reset_api_key', methods=['POST'])
def reset_api_key():
    session.pop('GOOGLE_API_KEY', None)
    logging.info("API Key has been reset.")
    return jsonify({'success': True, 'message': 'API Key reset.'})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'GOOGLE_API_KEY' not in session:
        logging.warning("Image upload attempt failed: API Key not configured.")
        return jsonify({'success': False, 'error': 'API Key not configured.'}), 403

    logging.info("Image upload process started.")
    if 'file' not in request.files:
        logging.warning("Image upload failed: No file part in request.")
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    if file:
        try:
            # Save original file temporarily
            original_filename = str(uuid.uuid4()) + "_" + file.filename
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            file.save(original_path)

            # Resize image
            pil_image = PILImage.open(original_path)
            pil_image.thumbnail((500, 500)) # Resize while maintaining aspect ratio, max 500px

            # Save resized image (e.g., as PNG for consistency)
            resized_filename = "resized_" + str(uuid.uuid4()) + ".png"
            resized_path = os.path.join(app.config['UPLOAD_FOLDER'], resized_filename)
            pil_image.save(resized_path, "PNG")
            
            # Clean up original large file if different from resized
            if original_path != resized_path and os.path.exists(original_path):
                 # Keep original for AgnoImage if it needs the original format/data
                 # For now, let's assume AgnoImage works best with the path to the image file
                 # If AgnoImage needs the original, pass original_path. If it can work with resized, pass resized_path.
                 # The Streamlit example saved the resized image and used its path.
                 pass

            logging.info(f"Image '{file.filename}' processed and saved as '{resized_filename}'. Preview URL generated.")
            return jsonify({
                'success': True,
                'image_url': url_for('static', filename=f'../{UPLOAD_FOLDER}/{resized_filename}'), # URL to serve the image
                'image_path': resized_path # Path for backend processing
            })
        except Exception as e:
            logging.error(f"Error processing image '{file.filename}': {e}", exc_info=True)
            # Clean up temp file on error
            if 'resized_path' in locals() and os.path.exists(resized_path):
                os.remove(resized_path)
            if 'original_path' in locals() and os.path.exists(original_path):
                os.remove(original_path)
            return jsonify({'success': False, 'error': 'Error processing image. Please check server logs.'}), 500
        

@app.route('/analyze_image', methods=['POST'])
def analyze_image_route():
    if 'GOOGLE_API_KEY' not in session:
        logging.warning("Image analysis attempt failed: API Key not configured.")
        return jsonify({'success': False, 'error': 'API Key not configured.'}), 403
    
    # Set the API key in the environment for agno before using it
    os.environ["GOOGLE_API_KEY"] = session["GOOGLE_API_KEY"]

    logging.info("Image analysis request received.")
    
    data = request.get_json()
    image_path = data.get('image_path')

    if not image_path or not os.path.exists(image_path):
        return jsonify({'success': False, 'error': 'Image path is invalid or file does not exist.'}), 400

    medical_agent = get_medical_agent()
    if not medical_agent:
        logging.error("Analysis failed: Medical agent could not be initialized. This might be due to an invalid API Key or an issue with the 'agno' library setup.")
        return jsonify({'success': False, 'error': 'Medical agent could not be initialized. Check API Key.'}), 500

    try:
        # Create AgnoImage object
        logging.info(f"Starting analysis for image: {image_path}")
        # Ensure the AgnoImage can handle the path correctly.
        # The original code saved a resized PNG and used its path.
        agno_image = AgnoImage(filepath=image_path)
        
        response = medical_agent.run(MEDICAL_ANALYSIS_QUERY, images=[agno_image])
        
        # Clean up the processed image file after analysis
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Also clean up the original if it was different and still exists
        # This part needs careful management of which file was used by AgnoImage
        # For simplicity, assuming image_path was the one used and now deleted.
        logging.info(f"Analysis successful for image: {image_path}")
        return jsonify({'success': True, 'analysis': response.content})
    except Exception as e:
        logging.error(f"Error during analysis for image '{image_path}': {e}", exc_info=True)
        # Clean up image file on error too
        if os.path.exists(image_path):
            os.remove(image_path)
        return jsonify({'success': False, 'error': 'An error occurred during analysis. Please check server logs.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
