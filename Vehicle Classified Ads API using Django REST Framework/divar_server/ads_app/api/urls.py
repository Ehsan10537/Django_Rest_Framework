from django.urls import path
from ads_app.api.views import (GetCarAdList, PostCarAd, GetCarAd, UpdateCarAd, DeleteCarAd, 
                               GetMotorcycleAdList, GetMotorcycleAd, PostMotorcycleAd, UpdateMotorcycleAd, DeleteMotorcycleAd, 
                               PostCarAdReview, GetCarAdReviewList, 
                               PostMotorcycleAdReview, getMotorcycleAdReviewList,
                               GetReview, UpdateReview, DeleteReview,
                               PostCarAdImage, GetCarAdImageList, GetCarAdImage, UpdateCarAdImage, DeleteCarAdImage,
                               PostmotorcycleAdImage, GetMotorcycleAdImageList, GetMotorcycleAdImage, UpdateMotorcycleAdImage, DeleteMotorcycleAdImage)

urlpatterns = [

    

    path('car/list/', GetCarAdList.as_view(), name='cars-list'), #
    path('car/create/', PostCarAd.as_view(), name='car-post'),  #
    path('car/<int:num>/', GetCarAd.as_view(), name='car-detail'), #
    path('car/<int:num>/update/', UpdateCarAd.as_view(), name='car-update'), #
    path('car/<int:num>/delete/', DeleteCarAd.as_view(), name='car-delete'), 

    path('motorcycle/list/', GetMotorcycleAdList.as_view(), name='motorcycles-list'),
    path('motorcycle/create/', PostMotorcycleAd.as_view(), name='motorcycle-post'),
    path('motorcycle/<int:num>/', GetMotorcycleAd.as_view(), name='motorcycle-review'),
    path('motorcycle/<int:num>/update/', UpdateMotorcycleAd.as_view(), name='motorcycle-update'),
    path('motorcycle/<int:num>/delete/', DeleteMotorcycleAd.as_view(), name='motorcycle-delete'),

    path('car/<int:num>/review/create/', PostCarAdReview.as_view(), name='car-review-post'), #
    path('car/<int:num>/review/list/', GetCarAdReviewList.as_view(), name='car-review-list'), #

    path('motorcycle/<int:num>/review/create/', PostMotorcycleAdReview.as_view(), name='mororcycle-review-post'),
    path('motorcycle/<int:num>/review/list/', getMotorcycleAdReviewList.as_view(), name='motorcycle-review-list'),

    path('review/<int:num>/', GetReview.as_view(), name='review-detail'), #
    path('review/<int:num>/update/', UpdateReview.as_view(), name='review-update'), #
    path('review/<int:num>/delete/', DeleteReview.as_view(), name='review-delete'), #

    path('car/<int:num>/image/create/', PostCarAdImage.as_view(), name='car-ad-image-post'), #
    path('car/<int:num>/image/list/', GetCarAdImageList.as_view(), name='car-ad-image-list'), #
    path('car/<int:num_1>/image/<int:num_2>/', GetCarAdImage.as_view(), name='car-image-detail'), #
    path('car/<int:num_1>/image/<num_2>/update/', UpdateCarAdImage.as_view(), name='car-image-update'), #
    path('car/<num_1>/image/<num_2>/delete/', DeleteCarAdImage.as_view(), name='car-image-delete'), #

    path('motorcycle/<int:num>/image/create/', PostmotorcycleAdImage.as_view(), name='motorcycle-image-post'),
    path('motorcycle/<int:num>/image/list/', GetMotorcycleAdImageList.as_view(), name='motorcycle-image-list'),
    path('motorcycle/<int:num_1>/image/<int:num_2>/', GetMotorcycleAdImage.as_view(), name='motorcycle-image-detail'),
    path('motorcycle/<int:num_1>/image/<int:num_2>/update/', UpdateMotorcycleAdImage.as_view(), name='motorcycle-image-update'),
    path('motorcycle/<int:num_1>/image/<int:num_2>/delete/', DeleteMotorcycleAdImage.as_view(), name='motorcycle-image-delete'),
    

]
