from rest_framework import permissions




# --------------------------------------------------------------------------------------------------
                                                        # Ad Permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.ad_user or request.user.is_staff)

# --------------------------------------------------------------------------------------------------
                                                        # Review Permissions

class IsReviewUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user==obj.review_user or request.user.is_staff)


# --------------------------------------------------------------------------------------------------
                                                        # Car Ad Image Permissions

class IsCarAdOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.car_ad.ad_user or request.user.is_staff)
    


# --------------------------------------------------------------------------------------------------
                                                        # Motorcycle Ad Image Permissions

class IsMotorcycleAdOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.motorcycle_ad.ad_user or request.user.is_staff)
