from rest_framework.serializers import OrderedDict
from rest_framework.serializers import ModelSerializer
from uuid import UUID


class DRFBaseModelSerializer(ModelSerializer):
    def to_dict(self):
        tmp = self.data
        if isinstance(tmp, list):
            tmp_ = []
            for i in tmp:
                tmp__ = {}
                for k, v in i.items():
                    if isinstance(v, OrderedDict):
                        tmp__[k] = dict(v)
                    elif isinstance(v, UUID):
                        tmp__[k] = str(v)
                    else:
                        tmp__[k] = v
                tmp_.append(tmp__)

            ret = tmp_
            return ret

        if isinstance(tmp, dict):
            tmp_ = {}
            for k, v in tmp.items():
                if isinstance(v, OrderedDict):
                    tmp_[k] = dict(v)
                elif isinstance(v, UUID):
                    tmp_[k] = str(v)
                else:
                    tmp_[k] = v

            ret = tmp_
            return ret

        if isinstance(tmp, OrderedDict):
            tmp_ = {}
            for k, v in tmp.items():
                if isinstance(v, OrderedDict):
                    tmp_[k] = dict(v)
                elif isinstance(v, UUID):
                    tmp_[k] = str(v)
                else:
                    tmp_[k] = v

            ret = tmp_
            return ret

        return tmp
