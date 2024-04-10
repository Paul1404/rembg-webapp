import logging
from rembg import remove
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_background(input_path, output_path):
    """
    Removes the background from an image.
    Args:
    - input_path: Path to the input image.
    - output_path: Path to save the output image with the background removed.
    """
    try:
        with Image.open(input_path) as img:
            output = remove(img)
            output.save(output_path)
            logging.info(f"Background removed and saved to {output_path}")
    except Exception as e:
        logging.error(f"Error removing background from {input_path}: {e}")

if __name__ == "__main__":
    input_path = 'path/to/your/dog.png'
    output_path = 'path/to/your/out.png'
    remove_background(input_path, output_path)
