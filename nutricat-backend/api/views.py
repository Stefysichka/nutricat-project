from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Cat
from .serializers import UserSerializer, CatSerializer
from .services import process_chat_message, generate_ration_with_ai                                 
from .models import Cat, FoodProduct, CatRation
from django.shortcuts import get_object_or_404

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    permission_classes = (AllowAny,)

    serializer_class = UserSerializer


@api_view(['GET'])

@permission_classes([IsAuthenticated])

def get_cats(request):

    cats = Cat.objects.filter(owner=request.user)

    serializer = CatSerializer(cats, many=True)

    return Response(serializer.data)
                       

@api_view(['GET'])

@permission_classes([IsAuthenticated])

def get_cat_detail(request, pk):
    try:
        cat = Cat.objects.get(pk=pk, owner=request.user)

    except Cat.DoesNotExist:
        return Response({"error": "Cat not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CatSerializer(cat)

    return Response(serializer.data)

@api_view(['PATCH'])

@permission_classes([IsAuthenticated])

def update_cat_photo(request, pk):
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)
    photo_url = request.data.get('photo_url')
    if photo_url:

        cat.photo_url = photo_url
        cat.save()
        return Response({"status": "success"})
    return Response({"error": "No photo provided"}, status=400)


@api_view(['POST'])

@permission_classes([IsAuthenticated])

def cat_chat_endpoint(request):

    messages_history = request.data.get('messages', [])

    cat_id = request.data.get('cat_id')                                  
    if not messages_history:

        return Response({"error": "No messages provided"}, status=status.HTTP_400_BAD_REQUEST)
    ai_result = process_chat_message(messages_history, cat_id, request.user)
    if ai_result["status"] == "chatting":

        return Response({"status": "chatting", "message": {"role": "assistant", "content": ai_result["reply"]}})
    elif ai_result["status"] == "completed":

        data = ai_result["data"]
        if cat_id:
            target_cat = Cat.objects.get(id=cat_id, owner=request.user)
            cat_data = data.get("cat", {})
            for key, value in cat_data.items():

                setattr(target_cat, key, value)
            target_cat.save()

        else:
            target_cat = Cat.objects.create(owner=request.user, **data["cat"])
        raw_diet = data.get("diet", [])

        unique_diet = []

        seen_foods = set()
        for item in raw_diet:

            food_id = f"{item.get('brand', '')}_{item.get('product_name', '')}"

            if food_id not in seen_foods:

                seen_foods.add(food_id)

                unique_diet.append(item)
        if len(unique_diet) > 0:
            if cat_id:

                target_cat.rations.all().delete()
            for item in unique_diet:

                food, _ = FoodProduct.objects.get_or_create(
                    brand=item.get("brand", "Невідомо"),
                    product_name=item.get("product_name", "Невідомо"),
                    food_type=item.get("food_type", "dry"),
                    calories_100g=item.get("calories_100g", 0),
                    protein_pct=item.get("protein_pct", 0),
                    fat_pct=item.get("fat_pct", 0),
                    fiber_pct=item.get("fiber_pct", 0)

                )

                CatRation.objects.create(

                    cat=target_cat,

                    product=food,

                    daily_portion_g=item.get("daily_portion_g", 0),

                    feeding_time=item.get("feeding_time", "Увесь день")

                )
        return Response({"status": "success", "cat_id": target_cat.id})

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_cat_ration(request, pk):
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)

    ration_text = generate_ration_with_ai(cat)

    return Response({"ration_text": ration_text})
                                              

@api_view(['GET', 'DELETE']) 

@permission_classes([IsAuthenticated])

def get_cat_detail(request, pk):
    try:
        cat = Cat.objects.get(pk=pk, owner=request.user)
    except Cat.DoesNotExist:
        return Response({"error": "Cat not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':

        cat.delete()                   

        return Response(status=status.HTTP_204_NO_CONTENT)                                          
    serializer = CatSerializer(cat)

    return Response(serializer.data)
