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

    def __init__(self, *args, **kwargs):
        self.list_display = [] if not self.list_display else self.list_display
        self.list_display_links = [] if not self.list_display_links else self.list_display_links
        self.list_filter = [] if not self.list_filter else self.list_filter
        self.search_fields = [] if not self.search_fields else self.search_fields
        self.readonly_fields = [] if not self.readonly_fields else self.readonly_fields

        super().__init__(*args, **kwargs)

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
                (f'{i}_`width`', f'{i}_`height`',),
                (f'{i}_alt', f'{i}_src',),
                f'{i}_description',
                f'{i}_blurbase64',
            ]

        ret = [('Images', {'fields': tmp})] if tmp else []
        return ret

    def __get_image_read_only_fields(self):
        ret = []
        for i in self.image_fields_name_list:
            ret.append(f'{i}_blurbase64')
            ret.append(f'{i}_width')
            ret.append(f'{i}_height')
        return ret

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

    _readonly_fields = []

    @property
    def readonly_fields(self):
        return self._readonly_fields

    @readonly_fields.setter
    def readonly_fields(self, value):
        value = list(value)

        tmp = ['id'] if 'id' not in value else []
        tmp += value
        tmp += self.__get_image_read_only_fields()
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
