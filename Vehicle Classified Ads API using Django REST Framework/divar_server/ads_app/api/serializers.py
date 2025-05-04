from rest_framework import serializers
from ads_app.models import CarAd, MotorcycleAd, Review, CarAdImage, MotorcycleAdImage
from PIL import Image   # this is to access image file pixel sizes(image dimenssions) using .size method

# ------------------------------------------------------------------



class CarAdSerializer(serializers.ModelSerializer):
    ad_user = serializers.StringRelatedField(read_only=True)
    # reviews = serializers.StringRelatedField(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CarAd
        fields = ['id', 'ad_user', 'title', 'city', 'brand', 'model', 'mileage', 'fuel_type', 'production_year', 'color', 'body_condition',
                'front_chassis_condition', 'rear_chassis_condition', 'engine_condition', 'gearbox', 'third_party_insurance_period',
                'price', 'willing_to_exchange', 'description', 'phone_number', 'images', 'reviews', 'created', 'updated']
        
    def get_reviews(self, obj):
        review_list = []
        for review_obj in obj.reviews.filter(status='approved'):
            review_list.append(review_obj.text)
        return review_list
    
    def get_images(self, obj):
        image_list = []
        for image_object in obj.images.filter(status='approved'):
            image_list.append(image_object.image.url)
        return image_list

# ------------------------------------------------------------------

class MotorcycleAdSerializer(serializers.ModelSerializer):
    ad_user = serializers.StringRelatedField(read_only=True)
    # reviews = serializers.StringRelatedField(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MotorcycleAd
        fields = ['id', 'ad_user', 'title', 'city', 'brand', 'model', 'mileage', 'production_year', 'price', 'willing_to_exchange',
                 'description', 'phone_number', 'images', 'reviews', 'created', 'updated']
        
    def get_reviews(self, obj):
        review_list = []
        for review_obj in obj.reviews.filter(status='approved'):
            review_list.append(review_obj.text)
        return review_list
    
    def get_images(self, obj):
        image_list = []
        for image_object in obj.images.filter(status='approved'):
             image_list.append(image_object.image.url)
        return image_list
        

# ------------------------------------------------------------------

class ReviewSerializer(serializers.ModelSerializer):
    content_object = serializers.StringRelatedField(read_only=True)
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'review_user', 'text', 'created', 'updated', 'content_type', 'object_id', 'content_object']
        read_only_fields = ['review_user', 'content_type', 'object_id', 'content_object']


# ------------------------------------------------------------------

class CarAdImageSerializer(serializers.ModelSerializer):
    car_ad = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CarAdImage
        fields = ['id', 'car_ad', 'image', 'uploaded']


    # value is not an object. but when dealing with file. it'll be an object of either InMemoryUploadedFile or TemporaryUploadedFile classes
    # And they have a .size attribute, which gives you the file size in bytes.    
    def validate_image(self, value): 
        max_size = 1 * 1024 * 1024  #1MB
        if value.size > max_size:
            raise serializers.ValidationError('your image is over 1MB. please try again.')
        
        img = Image.open(value)     #Image is imported from PIL (pillow)
        max_width = 2000
        max_height = 1900
        width, height = img.size       #when using pillow library, .size method returns the image dimessions
        if width > max_width or height > max_height:
            raise serializers.ValidationError(f"image dimenssions should not exceed {max_width}x{max_height} pixels")
        
        return value

# ------------------------------------------------------------------

class MotorcycleAdImageSerializer(serializers.ModelSerializer):
    motorcycle_ad = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = MotorcycleAdImage
        fields = ['id', 'motorcycle_ad', 'image', 'uploaded']

    def validate_image(self, value):
        max_size = 1 * 1024 *1024   #1MB
        if value.size > max_size:
            raise serializers.ValidationError('your image is over 1MB. please try again.')
        
        img = Image.open(value)
        max_width = 2000
        max_height = 1900
        width, height = img.size
        if width > max_width or height > max_height:
                        raise serializers.ValidationError(f"image dimenssions should not exceed {max_width}x{max_height} pixels")
        
        return value

