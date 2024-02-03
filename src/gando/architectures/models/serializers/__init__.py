class QueryDictSerializer:

    def __init__(self, image_fields_name=None):
        self.image_fields_name = [] if not image_fields_name else image_fields_name

    def __call__(self, input_data):
        return self.__parser(input_data)

    def __parser(self, input_data):
        if isinstance(input_data, list):
            return [self.__parser(i) for i in input_data]

        if isinstance(input_data, dict):
            tmp = dict()
            for k, v in input_data.items():
                k__split = k.split('__', 1)
                if len(k__split) == 1:
                    k_split = self.__image_field_name_parser(k)
                    if len(k_split) == 1:
                        _ = self.__parser(v)
                        v_ = _ if k not in tmp else self.__updater(tmp[k], _)
                        tmp[k] = v_ if k != 'src' else f'{self.__media_url}{v_}'
                    else:
                        _ = self.__parser({k_split[1]: v})
                        v_ = _ if k_split[0] not in tmp else self.__updater(tmp[k_split[0]], _)
                        tmp[k_split[0]] = v_ if k != 'src' else f'{self.__media_url}{v_}'
                else:
                    _ = self.__parser({k__split[1]: v})
                    v_ = _ if k__split[0] not in tmp else self.__updater(tmp[k__split[0]], _)
                    tmp[k__split[0]] = v_ if k != 'src' else f'{self.__media_url}{v_}'
            return tmp
        return input_data

    def __updater(self, a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            tmp = {}
            for k_a, v_a in a.items():
                for k_b, v_b in b.items():
                    if k_a == k_b:
                        tmp[k_a] = self.__updater(v_a, v_b)
                    else:
                        tmp[k_a] = v_a
                        tmp[k_b] = v_b
            return tmp

        if isinstance(a, list):
            a.append(b)
            return a

        if isinstance(b, list):
            return [a, b]
        return [a] + [b]

    def __image_field_name_parser(self, filed_name):
        equal = True
        for img in self.image_fields_name:

            len_img = len(img)
            if len_img > len(filed_name):
                continue

            for idx in range(len_img):
                if img[idx] != filed_name[idx]:
                    equal = False
                    break
                else:
                    continue
            if equal:
                return [img] + [filed_name.split(f'{img}_', 1)[1]]

        return [filed_name]

    @property
    def __media_url(self):
        try:
            from django.conf import settings

            return settings.MEDIA_URL
        except:
            return ''
