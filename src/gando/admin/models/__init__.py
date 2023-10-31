from django.contrib import admin


def verbose_name(value: str):
    tmp = value[0].upper()
    i = 1
    while i < len(value):
        if value[i] != '_':
            tmp += value[i]
        else:
            tmp += ' '
            i += 1
            tmp += value[i].upper()
        i += 1
    ret = tmp
    return ret


class BaseModelAdmin(admin.ModelAdmin):
    _list_display = []

    @property
    def list_display(self):
        return self._list_display

    @list_display.setter
    def list_display(self, value):
        value = list(value)

        tmp = ['available'] if 'available' not in value else []
        tmp += ['id'] if 'id' not in value else []
        tmp += value
        tmp += ['created_dt'] if 'created_dt' not in value else []
        tmp += ['updated_dt'] if 'updated_dt' not in value else []

        self._list_display = tmp

    _list_display_links = []

    @property
    def list_display_links(self):
        return self._list_display_links

    @list_display_links.setter
    def list_display_links(self, value):
        value = list(value)

        tmp = ['available'] if 'available' not in value else []
        tmp += ['id'] if 'id' not in value else []
        tmp += value
        tmp += ['created_dt'] if 'created_dt' not in value else []
        tmp += ['updated_dt'] if 'updated_dt' not in value else []

        self._list_display_links = tmp

    image_fields_name_list = []

    def __set_image_fieldsets(self):
        tmp = []
        for i in self.image_fields_name_list:
            tmp += [
                (f'{i}_category', f'{i}_device_type',),
                (f'{i}_width', f'{i}_height',),
                (f'{i}_alt', f'{i}_src',),
                f'{i}_description',
                f'{i}_blurbase64',
            ]

        ret = [('Images', {'fields': tmp})] if tmp else []
        return ret

    def __get_image_read_only_fields(self):
        return [f'{i}_blurbase64' for i in self.image_fields_name_list]

    _fieldsets = []

    @property
    def fieldsets(self):
        return self._fieldsets

    @fieldsets.setter
    def fieldsets(self, value):
        tmp = [('Initial', {'fields': [('available', 'id',)]})]
        tmp += value
        tmp += self.__set_image_fieldsets()
        tmp += [('Extra', {'fields': [('created_dt', 'updated_dt',)]})]

        self._fieldsets = tmp

        _readonly_fields = ['id', 'created_dt', 'updated_dt'] + self.__get_image_read_only_fields()
        self._readonly_fields = _readonly_fields if not self._readonly_fields else self._readonly_fields

    _readonly_fields = []

    @property
    def readonly_fields(self):
        return self._readonly_fields

    @readonly_fields.setter
    def readonly_fields(self, value):
        value = list(value)

        tmp = ['id'] if 'id' not in value else []
        tmp += value
        tmp += ['created_dt'] if 'created_dt' not in value else []
        tmp += ['updated_dt'] if 'updated_dt' not in value else []

        self._readonly_fields = tmp

    _list_filter = []

    @property
    def list_filter(self):
        return self._list_filter

    @list_filter.setter
    def list_filter(self, value):
        value = list(value)

        tmp = ['available'] if 'available' not in value else []
        tmp += value
        tmp += ['created_dt'] if 'created_dt' not in value else []
        tmp += ['updated_dt'] if 'updated_dt' not in value else []

        self._list_filter = tmp

    _search_fields = []

    @property
    def search_fields(self):
        return self._search_fields

    @search_fields.setter
    def search_fields(self, value):
        value = list(value)

        tmp = ['id'] if 'id' not in value else []
        tmp += value

        self._search_fields = tmp
