from django.urls import path
from content_check_app.api.views import (
                GetPendingCarAdList, GetPendingCarAd, UpdatePendingCarAd, BulkUpdatePendingCarAd,
                GetRejectedCarAdlist, GetRejectedCarAd, DeleteRejectedCarAd, BulkDeleteRejectedCarAd,
                GetPendingMotorcycleAdList, GetPendingMotorcycleAd, UpdatePendingMotorcycleAd, BulkUpdatePendingMotorcycleAd,
                GetRejectedMotorcycleAdList, GetRejectedMotorcycleAd, DeleteRejectedMotorcycleAd, BulkDeleteRejectedMotorcycleAd,
                GetPendingReviewList, GetPendingReview, UpdatePendingReview, BulkUpdatePendingReview,
                GetRejectedReviewList, GetRejectedReview, DeleteRejectedReview, BulkDeleteRejectedReview,
                GetPendingCarAdImageList, GetPendingCarAdImage, UpdatePendingCarAdImage, BulkUpdatePendingCarAdImage,
                GetRejetedCarAdImageList, GetRejectedCarAdImage, DeleteRejectedCarAdImage, BulkDeleteRejectedCarAdImage,
                GetPendingmotorcycleAdImageList, GetPendingMotorcycleAdImage, UpdatePendingMotorcycleAdImage, BulkUpdatePendingMotorcycleAdImage,
                GetRejectedMotorcycleAdImageList, GetRejectedMotorcycleAdImage, DeleteRejectedMotorcycleAdImage, BulkDeleteRejectedMotorcycleAdImage
                )

urlpatterns = [
    path('pending/car/list/', GetPendingCarAdList.as_view(), name='pending-car-list'), #
    path('pending/car/<int:num>/', GetPendingCarAd.as_view(), name='pending-car-detail'), #
    path('pending/car/<int:num>/update/', UpdatePendingCarAd.as_view(), name='pending-car-update'), #
    path('pending/car/bulk/update/', BulkUpdatePendingCarAd.as_view(), name='pending-car-bulk-update'), #

    path('rejected/car/list/', GetRejectedCarAdlist.as_view(), name='rejected-car-list'), #
    path('rejected/car/<int:num>/', GetRejectedCarAd.as_view(), name='rejected-car-detail'), #
    path('rejected/car/<int:num>/delete/', DeleteRejectedCarAd.as_view(), name='rejected-car-delete'), #
    path('rejected/car/bulk/delete/', BulkDeleteRejectedCarAd.as_view(), name='rejected-car-delete-all'), #
 
    path('pending/motorcycle/list/', GetPendingMotorcycleAdList.as_view(), name='pending-motorcycle-list'),
    path('pending/motorcycle/<int:num>/', GetPendingMotorcycleAd.as_view(), name='pending-motorcycle-detail'),
    path('pending/motorcycle/<int:num>/update/', UpdatePendingMotorcycleAd.as_view(), name='pending-motorcycle-update'),
    path('pending/motorcycle/bulk/update/', BulkUpdatePendingMotorcycleAd.as_view(), name='pending-motorcycle-bulk-update'),

    path('rejected/motorcycle/list/', GetRejectedMotorcycleAdList.as_view(), name='rejected-motorcycle-list'),
    path('rejected/motorcycle/<int:num>/', GetRejectedMotorcycleAd.as_view(), name='rejected-motorcycle-detail'),
    path('rejected/motorcycle/<int:num>/delete/', DeleteRejectedMotorcycleAd.as_view(), name='rejected-motorcycle-delete'),
    path('rejected/motorcycle/bulk/delete', BulkDeleteRejectedMotorcycleAd.as_view(), name='rejected-motorcycle-bulk-delete'),

    path('pending/review/list/', GetPendingReviewList.as_view(), name='pending-review-list'), #
    path('pending/review/<int:num>/', GetPendingReview.as_view(), name='pending-review-detail'), #
    path('pending/review/<int:num>/update/', UpdatePendingReview.as_view(), name='pending-review-update'), #
    path('pending/review/bulk/update/', BulkUpdatePendingReview.as_view(), name='pending-review-bulk-update'), #

    path('rejected/review/list/', GetRejectedReviewList.as_view(), name='rejected-review-list'), #
    path('rejected/review/<int:num>/', GetRejectedReview.as_view(), name='rejected-review-detail'), #
    path('rejected/review/<int:num>/delete/', DeleteRejectedReview.as_view(), name='rejected-review-delete'), #
    path('rejected/review/bulk/delete/', BulkDeleteRejectedReview.as_view(), name='rejected-review-bulk-delete'), #

    path('pending/car/image/list/', GetPendingCarAdImageList.as_view(), name='pending-car-image-list'), #
    path('pending/car/image/<int:num>/', GetPendingCarAdImage.as_view(), name='pending-car-image-detail'), #
    path('pending/car/image/<int:num>/update/', UpdatePendingCarAdImage.as_view(), name='pending-car-image-update'), #
    path('pending/car/image/bulk/update/', BulkUpdatePendingCarAdImage.as_view(), name='pending-car-image-bulk-update'), #

    path('rejected/car/image/list/', GetRejetedCarAdImageList.as_view(), name='rejected-car-image-list'), #
    path('rejected/car/image/<int:num>/', GetRejectedCarAdImage.as_view(), name='rejected-car-image-detail'), #
    path('rejected/car/image/<int:num>/delete/', DeleteRejectedCarAdImage.as_view(), name='rejected-car-image-delete'), #
    path('rejected/car/image/bulk/delete/', BulkDeleteRejectedCarAdImage.as_view(), name='rejected-car-image-bulk-delete'), #

    path('pending/motorcycle/image/list/', GetPendingmotorcycleAdImageList.as_view(), name='pending-motorcycle-image-list'),
    path('pending/motorcycle/image/<int:num>/', GetPendingMotorcycleAdImage.as_view(), name='pending-motorcycle-image-detail'),
    path('pending/motorcycle/image/<int:num>/update/', UpdatePendingMotorcycleAdImage.as_view(), name='pending-motorcycle-image-update'),
    path('pending/motorcycle/image/bulk/update/', BulkUpdatePendingMotorcycleAdImage.as_view(), name='pending-motorcycle-image-bulk-update'),

    path('rejected/motorcycle/image/list/', GetRejectedMotorcycleAdImageList.as_view(), name='rejected-motorcycle-image-list'),
    path('rejected/motorcycle/image/<int:num>/', GetRejectedMotorcycleAdImage.as_view(), name='rejected-motorcycle-image-detail'),
    path('rejected/motorcycle/image/<int:num>/delete/', DeleteRejectedMotorcycleAdImage.as_view(), name='rejected-motorcycle-image-delete'),
    path('rejected/motorcycle/image/bulk/delete/', BulkDeleteRejectedMotorcycleAdImage.as_view(), name='rejected-motorcycle-image-bulk-delete'),

    
]