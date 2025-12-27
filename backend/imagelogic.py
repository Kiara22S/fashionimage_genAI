from PIL import Image
import io

def prepareimage(uploaded_file):
 
    try:
        img = Image.open(uploaded_file)
        img_rgb = img.convert("RGB")
        
        return img_rgb
    except Exception as e:
        print(f"Error processing image: {e}")
        return None                                