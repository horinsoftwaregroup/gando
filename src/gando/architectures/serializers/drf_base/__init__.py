from rest_framework.serializers import ModelSerializer


class DRFBaseModelSerializer(ModelSerializer):
    def to_dict(self):
        return self.data
