from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from ads_app.models import CarAd, MotorcycleAd, Review, CarAdImage, MotorcycleAdImage
from ads_app.api.serializers import CarAdSerializer, MotorcycleAdSerializer, ReviewSerializer, CarAdImageSerializer, MotorcycleAdImageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ads_app.api.permissions import IsOwnerOrAdmin, IsReviewUserOrAdmin, IsCarAdOwnerOrAdmin, IsMotorcycleAdOwnerOrAdmin
from ads_app.api.pagination import CarAdListPagination, MotorcycleAdPagination
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, FormParser
import os

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ads_app.api.filters import CarAdFilter, MotorcycleAdFilter


# -------------------------------------------------------------------------------------------------------------------
                                                                  # Car Ad views

class GetCarAdList(generics.ListAPIView):
    serializer_class = CarAdSerializer
    permission_classes = [AllowAny]
    pagination_class = CarAdListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarAdFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created']
    ordering = ['-created']   # default ordering behaviour. no need for ordering parameter in the url when this is set.

    def get_queryset(self):
        queryset = CarAd.objects.filter(status='approved')
        return queryset



class PostCarAd(generics.CreateAPIView):
    serializer_class = CarAdSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(ad_user=user)



class GetCarAd(generics.RetrieveAPIView):
    serializer_class = CarAdSerializer
    permission_classes = [AllowAny]
    def get_object(self):
        return CarAd.objects.get(pk=self.kwargs['num'], status='approved')



class UpdateCarAd(generics.UpdateAPIView):
    serializer_class = CarAdSerializer
    permission_classes = [IsOwnerOrAdmin]
    def get_object(self):
        car_ad_object = CarAd.objects.get(pk=self.kwargs['num'], status='approved')
        self.check_object_permissions(self.request, car_ad_object)
        return car_ad_object



class DeleteCarAd(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    def get_object(self):
        car_ad_object = CarAd.objects.get(pk=self.kwargs['num'], status='approved')
        self.check_object_permissions(self.request, car_ad_object)
        return car_ad_object


# ---------------------------------------------------------------------------------------------------------------
                                                                  # Motorcycle Ad views

class GetMotorcycleAdList(generics.ListAPIView):
    serializer_class = MotorcycleAdSerializer
    permission_classes = [AllowAny]
    pagination_class = MotorcycleAdPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MotorcycleAdFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created']
    ordering = ['-created']   # default ordering behaviour. no need for ordering parameter in the url when this is set.

    def get_queryset(self):
        return MotorcycleAd.objects.filter(status='approved')



class PostMotorcycleAd(generics.CreateAPIView):
    serializer_class = MotorcycleAdSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        request_user = self.request.user
        serializer.save(ad_user=request_user)



class GetMotorcycleAd(generics.RetrieveAPIView):
    serializer_class = MotorcycleAdSerializer
    permission_classes = [AllowAny]
    def get_object(self):
        return MotorcycleAd.objects.get(pk=self.kwargs['num'], status='approved')



class UpdateMotorcycleAd(generics.UpdateAPIView):
    serializer_class = MotorcycleAdSerializer
    permission_classes = [IsOwnerOrAdmin]
    def get_object(self):
        motorcycle_ad_object =  MotorcycleAd.objects.get(pk=self.kwargs['num'], status='approved')
        self.check_object_permissions(self.request, motorcycle_ad_object)
        return motorcycle_ad_object



class DeleteMotorcycleAd(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    def get_object(self):
        motorcycle_ad_object = MotorcycleAd.objects.get(pk=self.kwargs['num'], status='approved')
        self.check_object_permissions(self.request, motorcycle_ad_object)
        return motorcycle_ad_object

# -------------------------------------------------------------------------------------------------------------------
                                                                  # Car Ad Review views

class PostCarAdReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        car_ad_id = self.kwargs['num']
        car_ad_object = CarAd.objects.get(pk=car_ad_id)
        request_user = self.request.user
        # way 1:
        # serializer.save(review_user=request_user, content_object=car_ad_object) #content_type and object_id will be filled by DRF automatically

        # way 2:
        content_type = ContentType.objects.get_for_model(CarAd)
        object_id = car_ad_object.id
        serializer.save(review_user=request_user, content_type=content_type, object_id=object_id) #content_object will be filled by DRF automatically


class GetCarAdReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    

    def get_queryset(self):
        car_ad_id = self.kwargs['num']
        car_ad_object = CarAd.objects.get(pk=car_ad_id)
        content_type = ContentType.objects.get_for_model(CarAd)
        object_id = car_ad_object.id

        # way 1:
        # queryset = car_ad_object.reviews.filter(status='approved')

        # way 2:
        queryset = Review.objects.filter(status='approved', content_type=content_type, object_id=object_id)

        return queryset

# ------------------------------------------------------------------------------------------------------------------
                                                             # Motorcycle Ad Review views

class PostMotorcycleAdReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        motorcycle_ad_id = self.kwargs['num']
        motorcycle_ad_object = MotorcycleAd.objects.get(pk=motorcycle_ad_id)
        content_type = ContentType.objects.get_for_model(MotorcycleAd)
        request_user = self.request.user
        object_id = motorcycle_ad_object.id

        # way 1:
        # serializer.save(review_user=request_user, content_object=motorcycle_ad_object)

        # way 2:
        serializer.save(review_user=request_user, content_type=content_type, object_id=object_id)


class getMotorcycleAdReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        motorcycle_ad_id = self.kwargs['num']
        motorcycle_ad_object = MotorcycleAd.objects.get(pk=motorcycle_ad_id)
        content_type = ContentType.objects.get_for_model(MotorcycleAd)
        object_id = motorcycle_ad_object.id

        # way 1:
        # queryset = motorcycle_ad_object.reviews.all(status='approved')

        # way 2:
        queryset = Review.objects.filter(status='approved' , content_type=content_type, object_id=object_id)

        return queryset

# --------------------------------------------------------------------------------------------------------------------
                                                                  # Review views

class GetReview(generics.RetrieveAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    def get_object(self):
        return Review.objects.get(pk=self.kwargs['num'], status='approved')


class UpdateReview(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrAdmin]
    def get_object(self):
        review_object = Review.objects.get(pk=self.kwargs['num'], status='approved')
        self.check_object_permissions(self.request, review_object)
        return review_object


class DeleteReview(generics.DestroyAPIView):
    permission_classes = [IsReviewUserOrAdmin]
    def get_object(self):
        review_object = Review.objects.get(pk=self.kwargs['num'], status='approved')
        self.check_object_permissions(self.request, review_object)
        return review_object

# ------------------------------------------------------------------------------------------------------------------------------
                                                            # Car Ad image views


# class PostCarAdImage(APIView):            # each request form should contain one image and a description for this view.
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request, *args, **kwargs):
#         car_ad_id  = kwargs['num']
#         car_ad_object = CarAd.objects.get(pk=car_ad_id)

#         if request.user == car_ad_object.ad_user or request.user.is_staff:   # This is a permission to let the car owner or the admin to add image.
#             serializer = CarAdImageSerializer(data=request.data, context={'request':request})
#             if serializer.is_valid():
#                 serializer.save(car_ad=car_ad_object)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             raise ValidationError('you are not the owner of the car or the admin of the website.')



class PostCarAdImage(APIView):       # each request form can contain multiple image files. no description
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, num):
        car_ad_object = CarAd.objects.get(pk=num)

        # object level permission check manually.
        if request.user != car_ad_object.ad_user and not request.user.is_staff:
            raise PermissionDenied('you are not the owner of the car or admin.')


        images = request.FILES.getlist('images')
        instances_data = []
        for img in images:
            data = {"image":img}
            serializer = CarAdImageSerializer(data=data, context={'request':request})
            if serializer.is_valid():
                serializer.save(car_ad=car_ad_object)
                instances_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(instances_data, status=status.HTTP_200_OK)


class GetCarAdImageList(generics.ListAPIView):
    serializer_class = CarAdImageSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        car_ad_object = CarAd.objects.get(pk=self.kwargs['num'])

        # return CarAdImage.objects.filter(car_ad=car_ad_object, status='approved')
        return car_ad_object.images.filter(status='approved')


class GetCarAdImage(generics.RetrieveAPIView):
    serializer_class = CarAdImageSerializer
    permission_classes = [AllowAny]
    def get_object(self):
        car_ad_object = CarAd.objects.get(pk=self.kwargs['num_1'])
        image_id = self.kwargs['num_2']
        return CarAdImage.objects.get(pk=image_id, car_ad=car_ad_object, status='approved')


class UpdateCarAdImage(generics.UpdateAPIView):
    serializer_class = CarAdImageSerializer
    permission_classes = [IsCarAdOwnerOrAdmin]
    def get_object(self):
        car_ad_object = CarAd.objects.get(pk=self.kwargs['num_1'])
        image_id = self.kwargs['num_2']
        image_object = CarAdImage.objects.get(pk=image_id, car_ad=car_ad_object, status='approved')
        self.check_object_permissions(self.request, image_object)
        return image_object

    def perform_update(self, serializer):
        if self.request.data.get('image'):          # if user updates the image (if image is included in the request)(this is for situations when you have other fields that you can update without changing the image)
            os.remove(self.get_object().image.path)
            serializer.save(status='pending')
        else:
            serializer.save()


class DeleteCarAdImage(generics.DestroyAPIView):
    permission_classes = [IsCarAdOwnerOrAdmin]
    def get_object(self):
        car_ad_object = CarAd.objects.get(pk=self.kwargs['num_1'])
        image_id = self.kwargs['num_2']
        image_object = CarAdImage.objects.get(pk=image_id, car_ad=car_ad_object, status='approved')
        self.check_object_permissions(self.request, image_object)
        return image_object

# ---------------------------------------------------------------------------------------------------------------------
                                                        # Motorcycle Ad image views

class PostmotorcycleAdImage(APIView):                  # each request form can contain multiple image files. no description
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, num):
        motorcycle_ad_object = MotorcycleAd.objects.get(pk=num)

        # permission check manually.
        if request.user != motorcycle_ad_object.ad_user and not request.user.is_staff:   # This is the Permission
            raise PermissionDenied('You are not the owner of the motorcycle or admin.')

        images = request.FILES.getlist('images')
        instances_data = []
        for img in images:
            data = {"image":img}
            serializer = MotorcycleAdImageSerializer(data=data, context={'request':request})
            if serializer.is_valid():
                serializer.save(motorcycle_ad=motorcycle_ad_object)
                instances_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(instances_data, status=status.HTTP_200_OK)



class GetMotorcycleAdImageList(generics.ListAPIView):
    serializer_class = MotorcycleAdImageSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        motorcycle_ad_object = MotorcycleAd.objects.get(pk=self.kwargs['num'])

        # return MotorcycleAdImage.objects.filter(motorcycle_ad=motorcycle_ad_object, status='approved')
        return motorcycle_ad_object.images.filter(status='approved')


class GetMotorcycleAdImage(generics.RetrieveAPIView):
    serializer_class = MotorcycleAdImageSerializer
    permission_classes = [AllowAny]
    def get_object(self):
        motorcycle_ad_object = MotorcycleAd.objects.get(pk=self.kwargs['num_1'])
        return MotorcycleAdImage.objects.get(pk=self.kwargs['num_2'], motorcycle_ad=motorcycle_ad_object, status='approved')



class UpdateMotorcycleAdImage(generics.UpdateAPIView):
    serializer_class = MotorcycleAdImageSerializer
    permission_classes = [IsMotorcycleAdOwnerOrAdmin]
    def get_object(self):
        motorcycle_ad_object = MotorcycleAd.objects.get(pk=self.kwargs['num_1'])
        image_object = MotorcycleAdImage.objects.get(pk=self.kwargs['num_2'], motorcycle_ad=motorcycle_ad_object, status='approved')
        self.check_object_permissions(self.request, image_object)
        return image_object

    def perform_update(self, serializer):
        if self.request.data.get('image'):          # if user updates the image (if image is included in the request)(this is for situations when you have other fields that you can update without changing the image)
            os.remove(self.get_object().image.path)
            serializer.save(status='pending')
        else:
            serializer.save()


class DeleteMotorcycleAdImage(generics.DestroyAPIView):
    permission_classes = [IsMotorcycleAdOwnerOrAdmin]
    def get_object(self):
        motorcycle_ad_object = MotorcycleAd.objects.get(pk=self.kwargs['num_1'])
        image_object = MotorcycleAdImage.objects.get(pk=self.kwargs['num_2'], motorcycle_ad=motorcycle_ad_object, status='approved')
        self.check_object_permissions(self.request, image_object)
        return image_object
