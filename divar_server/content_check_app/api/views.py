from rest_framework.views import APIView
from ads_app.models import MotorcycleAd, CarAd, Review, CarAdImage, MotorcycleAdImage
from ads_app.api.serializers import CarAdSerializer, MotorcycleAdSerializer, ReviewSerializer, CarAdImageSerializer, MotorcycleAdImageSerializer
from content_check_app.api.serializers import (ContentCheck_CarAdSerializer, ContentCheck_MotorcycleAdSerializer, ContentCheck_ReviewSerializer,
                                               ContentCheck_MotorcycleAdImageSerializer, ContentCheck_CarAdImageSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ValidationError


# ------------------------------------------------------------------------------------

class GetPendingCarAdList(generics.ListAPIView):
    serializer_class = ContentCheck_CarAdSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return CarAd.objects.filter(status='pending')


class GetPendingCarAd(generics.RetrieveAPIView):
    serializer_class = ContentCheck_CarAdSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        car_ad_id = self.kwargs['num']
        car_ad_object = CarAd.objects.get(pk=car_ad_id, status='pending')
        return car_ad_object


class UpdatePendingCarAd(generics.UpdateAPIView):    # you can send patch request for partial update.
    serializer_class = ContentCheck_CarAdSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        car_ad_id = self.kwargs['num']
        car_ad_object = CarAd.objects.get(pk=car_ad_id, status='pending')
        return car_ad_object
    
    def perform_update(self, serializer):
        if serializer.validated_data['status'] == 'approved':      # allow to approve the car ad only if its images are either approved or rejected.
            if self.get_object().images.exclude(status__in=['approved', 'rejected']).first():  # even if no images were uploaded at all, this returns False.
                raise ValidationError('you still have pending images left.')
            
        serializer.save()
    

class BulkUpdatePendingCarAd(APIView): # updates all car ads unless it has unapproved images     # generic views don't support bulk operations.
    permission_classes = [IsAdminUser]
    def put(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"Error":"Expected a list of objects."}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_instances = []
        logs = []

        for item in data:
            obj = CarAd.objects.get(pk=item['id'], status='pending')
            serializer = ContentCheck_CarAdSerializer(obj, data=item, partial=True)
            if serializer.is_valid():
                if serializer.validated_data['status'] == 'approved':
                    if obj.images.exclude(status__in=['approved', 'rejected']).first():
                        logs.append(f'ERROR : you still have pending images left for car ad {obj.id}')
                        continue
                serializer.save()
                updated_instances.append(serializer.data)
                logs.append(f'UPDATED : car ad {obj.id} is updated and the status is {obj.status}')  #after .save(), obj.status is the new status value
            else:
                logs.append(f'ERROR : car ad {obj.id} did not update due to serialization Error')
        
        final_responce = {'updated_instances':updated_instances, 'logs':logs}
        return Response(final_responce, status=status.HTTP_200_OK)
    
# -------------------------------------------------------------------------------------------------------------

class GetRejectedCarAdlist(generics.ListAPIView):
    serializer_class = ContentCheck_CarAdSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return CarAd.objects.filter(status='rejected')



class GetRejectedCarAd(generics.RetrieveAPIView):
    serializer_class = ContentCheck_CarAdSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return CarAd.objects.get(pk=self.kwargs['num'], status='rejected')



class DeleteRejectedCarAd(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    def get_object(self):
        return CarAd.objects.get(pk=self.kwargs['num'], status='rejected')
    


class BulkDeleteRejectedCarAd(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"Error":"Expected a list of objects."})

        selected_ids = []
        for item in data:
            selected_ids.append(item['id'])
        
        car_ad_objects = CarAd.objects.filter(pk__in=selected_ids, status='rejected')
        count, _ = car_ad_objects.delete()
        return Response({"message":f"selected rejected car ads were deleted successfully. {count} car ads in total."})

# ------------------------------------------------------------------------------------

class GetPendingMotorcycleAdList(generics.ListAPIView):
    serializer_class = ContentCheck_MotorcycleAdSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return MotorcycleAd.objects.filter(status='pending')


class GetPendingMotorcycleAd(generics.RetrieveAPIView):
    serializer_class = ContentCheck_MotorcycleAdSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return MotorcycleAd.objects.get(pk=self.kwargs['num'], status='pending')


class UpdatePendingMotorcycleAd(generics.UpdateAPIView):
    serializer_class = ContentCheck_MotorcycleAdSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return MotorcycleAd.objects.get(pk=self.kwargs['num'], status='pending')
    
    def perform_update(self, serializer):
        if serializer.validated_data['status'] == 'approved':
            if self.get_object().images.exclude(status__in=['approved', 'rejected']).first():
                raise ValidationError('you still have pending images left')
        serializer.save()


class BulkUpdatePendingMotorcycleAd(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"Error":"Expected a list of objects."}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_instances = []
        logs = []

        for item in data:
            obj = MotorcycleAd.objects.get(pk=item['id'], status='pending')
            serializer = ContentCheck_MotorcycleAdSerializer(obj, data=item, partial=True)
            if serializer.is_valid():
                if serializer.validated_data['status'] == 'approved':
                    if obj.images.exclude(status__in=['approved', 'rejected']).first():
                        logs.append(f'ERROR : you still have pending images left for motorcycle ad {obj.id}')
                        continue
                serializer.save()
                updated_instances.append(serializer.data)
                logs.append(f'UPDATED : motorcycle ad {obj.id} is updated and the status is {obj.status}')
            else:
                logs.append(f'ERROR : motorcycle ad {obj.id} did not update due to serialization Error')
        
        final_responce = {'updated_instances':updated_instances, 'logs':logs}
        return Response(final_responce, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------
class GetRejectedMotorcycleAdList(generics.ListAPIView):
    serializer_class = ContentCheck_MotorcycleAdSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return MotorcycleAd.objects.filter(status='rejected')



class GetRejectedMotorcycleAd(generics.RetrieveAPIView):
    serializer_class = ContentCheck_MotorcycleAdSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return MotorcycleAd.objects.get(pk=self.kwargs['num'], status='rejected')



class DeleteRejectedMotorcycleAd(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    def get_object(self):
        return MotorcycleAd.objects.get(pk=self.kwargs['num'], status='rejected')



class BulkDeleteRejectedMotorcycleAd(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"Error":"Expected a list of objects."})
        
        selected_ids = []
        for item in data:
            selected_ids.append(item['id'])
        motorcycle_ad_objects = MotorcycleAd.objects.filter(pk__in=selected_ids, status='rejected')
        count , _ = motorcycle_ad_objects.delete()
        return Response({"message":f"Selected rejected motorcycle ads were deleted successfully. {count} motorcycle ads in total."})

# ------------------------------------------------------------------------------------

class GetPendingReviewList(generics.ListAPIView):
    serializer_class = ContentCheck_ReviewSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return Review.objects.filter(status='pending')


class GetPendingReview(generics.RetrieveAPIView):
    serializer_class = ContentCheck_ReviewSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return Review.objects.get(pk=self.kwargs['num'], status='pending')


class UpdatePendingReview(generics.UpdateAPIView):
    serializer_class = ContentCheck_ReviewSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return Review.objects.get(pk=self.kwargs['num'], status='pending')


class BulkUpdatePendingReview(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({'Error':'Expected a list of objects.'})
        
        updated_instances = []
        logs = []

        for item in data:
            review_object = Review.objects.get(pk=item['id'], status='pending')
            serializer  = ContentCheck_ReviewSerializer(review_object, data=item, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_instances.append(serializer.data)
                logs.append(f"Review {review_object.id} is updated and the status is {review_object.status}")
            else:
                logs.append(f"ERROR: Review {review_object.id} did not update!")
        final_response = {"updated instances":updated_instances, "logs":logs}
        return Response(final_response, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------
class GetRejectedReviewList(generics.ListAPIView):
    serializer_class = ContentCheck_ReviewSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return Review.objects.filter(status='rejected')


class GetRejectedReview(generics.RetrieveAPIView):
    serializer_class = ContentCheck_ReviewSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return Review.objects.get(pk=self.kwargs['num'], status='rejected')


class DeleteRejectedReview(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    def get_object(self):
        return Review.objects.get(pk=self.kwargs['num'], status='rejected')
    

class BulkDeleteRejectedReview(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"Error":"Expected a list of objects"})
        
        selected_ids = []
        for item in data:
            selected_ids.append(item['id'])
        
        review_objects = Review.objects.filter(pk__in=selected_ids, status='rejected')
        count, _ = review_objects.delete()
        return Response({"message":f"Selected rejected reviews were deleted successfully. {count} reviews ads in total."})
    
# ------------------------------------------------------------------------------------

class GetPendingCarAdImageList(generics.ListAPIView):
    serializer_class = ContentCheck_CarAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return CarAdImage.objects.filter(status='pending')


class GetPendingCarAdImage(generics.RetrieveAPIView):
    serializer_class = ContentCheck_CarAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return CarAdImage.objects.get(pk=self.kwargs['num'], status='pending')


class UpdatePendingCarAdImage(generics.UpdateAPIView):
    serializer_class = ContentCheck_CarAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return CarAdImage.objects.get(pk=self.kwargs['num'], status='pending')



class BulkUpdatePendingCarAdImage(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response("{'Error':'Expected a list of objects.'}")
        
        updated_instances = []
        logs = []

        for item in data:
            image_object = CarAdImage.objects.get(pk=item['id'], status='pending')
            serializer = ContentCheck_CarAdImageSerializer(image_object, data=item, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_instances.append(serializer.data)
                logs.append(f"Image {image_object.id} is updated and the status is {image_object.status}")
            else:
                logs.append(f"ERROR: Image {image_object.id} did not update!")
        final_response = {"updated instances":updated_instances, "logs":logs}
        return Response(final_response, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------
class GetRejetedCarAdImageList(generics.ListAPIView):
    serializer_class = ContentCheck_CarAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return CarAdImage.objects.filter(status='rejected')
    

class GetRejectedCarAdImage(generics.RetrieveAPIView):
    serializer_class = ContentCheck_CarAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return CarAdImage.objects.get(pk=self.kwargs['num'], status='rejected')


class DeleteRejectedCarAdImage(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    def get_object(self):
        return CarAdImage.objects.get(pk=self.kwargs['num'], status='rejected')
    

class BulkDeleteRejectedCarAdImage(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"Error":"Expected a list of objects"})
        
        selected_ids = []
        for item in data:
            selected_ids.append(item['id'])
        
        image_objects = CarAdImage.objects.filter(pk__in=selected_ids, status='rejected')
        count, _ = image_objects.delete()
        return Response({"message":f"Selected rejected images were deleted successfully. {count} images in total."})
            
# ------------------------------------------------------------------------------------

class GetPendingmotorcycleAdImageList(generics.ListAPIView):
    serializer_class = ContentCheck_MotorcycleAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return MotorcycleAdImage.objects.filter(status='pending')


class GetPendingMotorcycleAdImage(generics.RetrieveAPIView):
    serializer_class = ContentCheck_MotorcycleAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return MotorcycleAdImage.objects.get(pk=self.kwargs['num'], status='pending')


class UpdatePendingMotorcycleAdImage(generics.UpdateAPIView):
    serializer_class = ContentCheck_MotorcycleAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return MotorcycleAdImage.objects.get(pk=self.kwargs['num'], status='pending')


class BulkUpdatePendingMotorcycleAdImage(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"Error":"Expected a list of objects"})
        
        updated_instances = []
        logs = []

        for item in data:
            image_object = MotorcycleAdImage.objects.get(pk=item['id'], status='pending')
            serializer = ContentCheck_MotorcycleAdImageSerializer(image_object, data=item, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_instances.append(serializer.data)
                logs.append(f"Image {image_object.id} is updated and the status is {image_object.status}")
            else:
                logs.append(f"ERROR: Image {image_object.id} did not update")
        
        final_response = {"updated instances":updated_instances, "logs":logs}
        return Response(final_response, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------
class GetRejectedMotorcycleAdImageList(generics.ListAPIView):
    serializer_class = ContentCheck_MotorcycleAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return MotorcycleAdImage.objects.filter(status='rejected')


class GetRejectedMotorcycleAdImage(generics.RetrieveAPIView):
    serializer_class = ContentCheck_MotorcycleAdImageSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        return MotorcycleAdImage.objects.get(pk=self.kwargs['num'], status='rejected')


class DeleteRejectedMotorcycleAdImage(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    def get_object(self):
        return MotorcycleAdImage.objects.get(pk=self.kwargs['num'], status='rejected')
    

class BulkDeleteRejectedMotorcycleAdImage(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"Error":"Expected a list of objects"})
        
        selected_ids = []
        for item in data:
            selected_ids.append(item['id'])
        
        image_objects = MotorcycleAdImage.objects.filter(pk__in=selected_ids, status='rejected')
        count, _ = image_objects.delete()
        return Response({"message":f"Selected rejected images were deleted successfully. {count} images in total."})

# ------------------------------------------------------------------------------------
