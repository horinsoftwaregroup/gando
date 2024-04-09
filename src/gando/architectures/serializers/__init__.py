from typing import OrderedDict
from rest_framework.serializers import ModelSerializer as DRFModelSerializer


class ModelSerializer(DRFModelSerializer):
    def to_dict(self):
        data = self.data
        data_ = self._to_dict(data)
        return data_

    def _to_dict(self, data):
        if isinstance(data, list):
            data_ = []
            for i in data:
                data_.append(self._to_dict(i))
            return data_

        if isinstance(data, dict) or isinstance(data, OrderedDict):
            data = dict(data)
            data_ = {}
            for k, v in data.items():
                data_[k] = self._to_dict(v)
            return data_

        if isinstance(data, str) or isinstance(data, int) or isinstance(data, float) or isinstance(data, bool):
            data_ = data
            return data_

        data_ = str(data)
        return data_
