from PIL import Image as ImagePIL, ImageFilter
import base64
import io


class Image:
    def __init__(self, src):
        self.__src = src

        self.width = self.__open_image().width
        self.height = self.__open_image().height

        self.size = self.__src.size

        self.proportion = self.__proportion()

        self.file_format = self.__open_image().format.lower()

        self.b64 = self.__b64()

    __open_image_ = None

    def __open_image(self):
        if not self.__open_image_:
            self.__open_image_ = ImagePIL.open(self.__src)
        return self.__open_image_

    def __b64(self):
        try:
            (b64width, b64height) = (self.width // 8, self.height // 8)

            mimetype = self.__open_image().get_format_mimetype()
            im_resized = self.__open_image().resize((b64width, b64height))
            blurred_image = im_resized.filter(ImageFilter.BLUR)
            buffered = io.BytesIO()
            blurred_image.save(buffered, format='PNG')
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

            return f'data:{mimetype};base64,{encoded_image}'
        except:
            return ''

    def __proportion(self) -> int:
        image_p = round(self.height / self.width, 15)

        b__p_9_16__p_2_3 = round(9 / 16 + abs(9 / 16 - 2 / 3) / 2, 15)
        b__p_2_3__p_3_4 = round(2 / 3 + abs(2 / 3 - 3 / 4) / 2, 15)
        b__p_3_4__p_4_5 = round(3 / 4 + abs(3 / 4 - 4 / 5) / 2, 15)
        b__p_4_5__p_1_1 = round(4 / 5 + abs(4 / 5 - 1 / 1) / 2, 15)
        b__p_1_1__p_5_4 = round(1 / 1 + abs(1 / 1 - 5 / 4) / 2, 15)
        b__p_5_4__p_4_3 = round(5 / 4 + abs(5 / 4 - 4 / 3) / 2, 15)
        b__p_4_3__p_3_2 = round(4 / 3 + abs(4 / 3 - 3 / 2) / 2, 15)
        b__p_3_2__p_16_9 = round(3 / 2 + abs(3 / 2 - 16 / 9) / 2, 15)

        if image_p <= b__p_9_16__p_2_3:
            return 916

        elif b__p_9_16__p_2_3 < image_p <= b__p_2_3__p_3_4:
            return 23

        elif b__p_2_3__p_3_4 < image_p <= b__p_3_4__p_4_5:
            return 34

        elif b__p_3_4__p_4_5 < image_p <= b__p_4_5__p_1_1:
            return 45

        elif b__p_4_5__p_1_1 < image_p <= b__p_1_1__p_5_4:
            return 11

        elif b__p_1_1__p_5_4 < image_p <= b__p_5_4__p_4_3:
            return 54

        elif b__p_5_4__p_4_3 < image_p <= b__p_4_3__p_3_2:
            return 43

        elif b__p_4_3__p_3_2 < image_p <= b__p_3_2__p_16_9:
            return 32

        else:
            return 169
