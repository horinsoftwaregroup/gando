from PIL import Image as ImagePIL, ImageFilter
import base64
import io


class Image:
    def __init__(self, src):
        self.__src = src

        self._width = None
        self._height = None

        self._size = None

        self._proportion = None

        self._file_format = None

        self._b64 = None

        self._open_image = None

    def get_width(self):
        if not self._width:
            self._width = self.__open_image().width
        return self._width

    def get_height(self):
        if not self._height:
            self._height = self.__open_image().height
        return self._height

    def get_size(self):
        if not self._size:
            self._size = self.__src.size
        return self._size

    def get_proportion(self):
        if not self._proportion:
            self._proportion = self.__proportion()
        return self._proportion

    def get_file_format(self):
        if not self._file_format:
            self._file_format = self.__src.name.split('.')[-1].lower()
        return self._file_format

    def get_b64(self):
        if not self._b64:
            self._b64 = self.__b64()
        return self._b64

    def __open_image(self):
        if not self._open_image:
            self._open_image = ImagePIL.open(self.__src)
        return self._open_image

    def __b64(self):
        try:
            (b64width, b64height) = (self.get_width() // 8, self.get_height() // 8)

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
        image_p = round(self.get_height() / self.get_width(), 15)

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
