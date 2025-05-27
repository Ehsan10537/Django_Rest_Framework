from rest_framework import serializers
from ads_app.models import CarAd, MotorcycleAd, Review, CarAdImage, MotorcycleAdImage

# --------------------------------------------------------------------

class ContentCheck_CarAdSerializer(serializers.ModelSerializer):
    ad_user = serializers.StringRelatedField(read_only=True)
    status = serializers.ChoiceField(required=True, choices=CarAd.status_choices)
    class Meta:
        model = CarAd
        fields = ['id', 'ad_user', 'title', 'city', 'brand', 'model', 'mileage', 'fuel_type', 'production_year', 'color','body_condition',
                  'front_chassis_condition', 'rear_chassis_condition', 'engine_condition', 'gearbox','third_party_insurance_period','price',
                    'willing_to_exchange', 'description', 'phone_number','created', 'updated', 'status']
    
    # in generic views put and patch request are handled together automatically.
    # when sending patch request, required fields will not be required anymore, because partial=True in patch by default.
    # so one way to handle this, is to handle it in the validation function in the serializer.
    # we set status as required but it's ignored while sending patch request.
    def validate(self, attrs):
        if 'status' not in attrs:
            raise serializers.ValidationError('status field is required. please provide a value for it then try again')
        return attrs
    
# --------------------------------------------------------------------

class ContentCheck_MotorcycleAdSerializer(serializers.ModelSerializer):
    ad_user = serializers.StringRelatedField(read_only=True)
    status = serializers.ChoiceField(required=True, choices=MotorcycleAd.status_choices)
    class Meta:
        model = MotorcycleAd
        fields = ['id', 'ad_user', 'title', 'city', 'brand', 'model', 'mileage', 'production_year', 'price','willing_to_exchange',
                  'description', 'phone_number', 'created', 'updated', 'status']

    # handle status to be required even if PATCH request is sent
    def validate(self, attrs):
        if 'status' not in attrs:
            raise serializers.ValidationError('status field is required. please provide a value for it then try again')
        return attrs

# --------------------------------------------------------------------

class ContentCheck_ReviewSerializer(serializers.ModelSerializer):
    content_object = serializers.StringRelatedField(read_only=True)
    review_user = serializers.StringRelatedField(read_only=True)
    status = serializers.ChoiceField(required=True, choices=Review.status_choices)
    class Meta:
        model = Review
        fields = ['id', 'review_user', 'text', 'created', 'updated', 'content_type', 'object_id', 'content_object', 'status']
        read_only_fields = ['review_user', 'content_type', 'object_id', 'content_object']

    # handle status to be required even if PATCH request is sent
    def validate(self, attrs):
        if 'status' not in attrs:
            raise serializers.ValidationError('status field is required. please provide a value for it then try again')
        return attrs

# --------------------------------------------------------------------

class ContentCheck_CarAdImageSerializer(serializers.ModelSerializer):
    car_ad = serializers.StringRelatedField(read_only=True)
    status = serializers.ChoiceField(required=True, choices=CarAdImage.status_choices)
    class Meta:
        model = CarAdImage
        fields = ['id','car_ad', 'image', 'uploaded', 'status']
        read_only_fields = ['image']

    # handle status to be required even if PATCH request is sent
    def validate(self, attrs):
        if 'status' not in attrs:
            raise serializers.ValidationError('status field is required. please provide a value for it then try again')
        return attrs
    
# --------------------------------------------------------------------

class ContentCheck_MotorcycleAdImageSerializer(serializers.ModelSerializer):
    motorcycle_ad = serializers.StringRelatedField(read_only=True)
    status = serializers.ChoiceField(required=True, choices=MotorcycleAdImage.status_choices)
    class Meta:
        model = MotorcycleAdImage
        fields = ['id', 'motorcycle_ad', 'image', 'uploaded', 'status']
        read_only_fields = ['image']

    # handle status to be required even if PATCH request is sent
    def validate(self, attrs):
        if 'status' not in attrs:
            raise serializers.ValidationError('status field is required. please provide a value for it then try again')
        return attrs

# --------------------------------------------------------------------
