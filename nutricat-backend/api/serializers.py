from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cat, FoodProduct, CatRation


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('id', 'username', 'email', 'password')

        extra_kwargs = {

            'password': {'write_only': True},
            'username': {'required': False}                                                     
        }

    def validate(self, attrs):

        email = attrs.get('email', '')
        if User.objects.filter(username=email).exists():
            raise serializers.ValidationError({"email": "Користувач з такою поштою вже існує!"})
        return attrs


    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['email'],                                
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('username', '')                      
        )
        return user


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = '__all__'


class CatRationSerializer(serializers.ModelSerializer):

    product = FoodProductSerializer(read_only=True) 
    class Meta:
        model = CatRation
        fields = ['id', 'daily_portion_g', 'feeding_time', 'product']

class CatSerializer(serializers.ModelSerializer):
    rations = CatRationSerializer(many=True, read_only=True)
    chart_data = serializers.SerializerMethodField()
    class Meta:

        model = Cat
        fields = [
            'id', 'name', 'breed', 'gender', 'birth_date', 'weight_kg', 
            'body_condition', 'activity_level', 'is_neutered', 'description', 
            'tips', 'photo_url', 'rations', 'chart_data'
        ]
        read_only_fields = ('owner',)

    def get_chart_data(self, obj):
        cat_rations = obj.rations.all() 
        if not cat_rations.exists():

            return {'protein': 0, 'fat': 0, 'fiber': 0}

        total_protein = sum(r.product.protein_pct for r in cat_rations if r.product.protein_pct)
        total_fat = sum(r.product.fat_pct for r in cat_rations if r.product.fat_pct)
        total_fiber = sum(r.product.fiber_pct for r in cat_rations if r.product.fiber_pct)
        count = cat_rations.count()

        return {
            'protein': round(total_protein / count, 1),
            'fat': round(total_fat / count, 1),
            'fiber': round(total_fiber / count, 1)
        }