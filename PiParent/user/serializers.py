from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','phone','password']
        
class UserSerializers(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','phone','password','first_name']
        