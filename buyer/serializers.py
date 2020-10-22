from rest_framework.serializers import ModelSerializer
from seller.models import Goods


class GoodsSerializers(ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
