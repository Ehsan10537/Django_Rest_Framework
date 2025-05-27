from rest_framework.decorators import api_view
from user_app.api.serializers import RegisterationSerializer, GetUserInfoSerializer, UserPasswordChangeSerializer
from ads_app.api.serializers import CarAdSerializer, MotorcycleAdSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from user_app.api.permissions import IsUser, IsUserOrAdmin

from utils.openai_service import welcome_user
# --------------------------------------------------------------------------



@api_view(['POST'])
def registeration(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {}
            data['Response'] = "user created successfully!"
            data['Username'] = user.username
            data['Email'] = user.email
            data['name'] = user.profile.name
            data['family_name'] = user.profile.family_name
            data['phone_number'] = user.profile.phone_number
            data['date_of_birth'] = user.profile.date_of_birth
            data['bio'] = user.profile.bio
            token = Token.objects.create(user=user)
            data['Token'] = token.key

            name = data['name']
            welcome_message = welcome_user(name=name)
            data['Welcome Message'] = welcome_message

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------------

@api_view(['DELETE'])
def logout(request):
    if request.method == 'DELETE':
        user = request.user
        # token_object = Token.objects.get(user=user)
        # token_object = request.auth

        token_key = request.headers.get('Authorization').split()[1]
        token_object = Token.objects.get(key=token_key)

        token_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------------------------------------------------------

class GetUserInformation(generics.RetrieveAPIView):
    serializer_class = GetUserInfoSerializer
    permission_classes = [IsUserOrAdmin]
    
    def get_object(self):
        user = User.objects.get(pk=self.kwargs['num'])
        return user


class UserPasswordChange(generics.UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer
    permission_classes = [IsUser]
    queryset = User.objects.all()
    lookup_url_kwarg = 'num'



class GetUserPendingAdList(APIView):
    permission_classes = [IsUser]

    def get(self, request, num):
        user = User.objects.get(pk=num)

        car_ads = user.car_ads.filter(status='pending')
        car_serializer = CarAdSerializer(car_ads, many=True)

        motorcycle_ads = user.motorcycle_ads.filter(status='pending')
        motorcycle_serializer = MotorcycleAdSerializer(motorcycle_ads, many=True)

        final_response = {"Pending Car Ads":car_serializer.data, "Pending Motorcycle Ads":motorcycle_serializer.data}

        return Response(final_response, status=status.HTTP_200_OK)
    


class GetUserRejectedAdList(APIView):
    permission_classes = [IsUser]

    def get(self, request, num):
        user = User.objects.get(pk=num)

        car_ads = user.car_ads.filter(status='rejected')
        car_serializer = CarAdSerializer(car_ads, many=True)

        motorcycle_ads = user.motorcycle_ads.filter(status='rejected')
        motorcycle_serializer = MotorcycleAdSerializer(motorcycle_ads, many=True)

        final_response = {"Rejected Car Ads":car_serializer.data, "Rejected Motorcycle Ads":motorcycle_serializer.data}

        return Response(final_response, status=status.HTTP_200_OK)
    
