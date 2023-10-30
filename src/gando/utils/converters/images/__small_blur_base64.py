from PIL import Image, ImageFilter
import base64
import io


def small_blur_base64(image_file_path):
    try:
        im = Image.open(image_file_path)
        (width, height) = (im.width // 8, im.height // 8)
        mimetype = im.get_format_mimetype()
        im_resized = im.resize((width, height))
        blurred_image = im_resized.filter(ImageFilter.BLUR)
        buffered = io.BytesIO()
        blurred_image.save(buffered, format="PNG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:{mimetype};base64,{encoded_image}"
    except Exception as exc:
        return
