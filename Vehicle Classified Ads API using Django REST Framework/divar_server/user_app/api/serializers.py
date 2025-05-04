from rest_framework import serializers
from django.contrib.auth.models import User
from user_app.models import Profile
from django.core.validators import RegexValidator

# -----------------------------------------------------------------------------------------

class RegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=50, write_only=True)
    family_name = serializers.CharField(max_length=50, write_only=True)
    phone_number = serializers.CharField(validators=[RegexValidator(regex=r'^09\d{9}$', message='Phone number must be in the format: 09xxxxxxxxx')], write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    bio = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'name', 'family_name', 'phone_number', 'date_of_birth', 'bio']
        extra_kwargs = {'password':{'write_only':True}}

    
    def validate(self, attrs):
        if attrs['password'] != attrs['password']:
            raise serializers.ValidationError('Passwords do not match. try again please.')
        elif User.objects.filter(email=attrs['email']).first():
            raise serializers.ValidationError('This email address is already in use. try another email address.')
        else:
            return attrs

    def create(self, validated_data):
        name = validated_data.pop('name')
        family_name = validated_data.pop('family_name')
        phone_numer = validated_data.pop('phone_number')
        date_of_birth = validated_data.pop('date_of_birth')
        bio = validated_data.pop('bio')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)
        user.save()  #after .save() method the signal triggers automatically right away.

        # now the signal is ran and a Profile instance is created and connected to the User instance OneToOne
        # now I should fill the other Profile fields with these data
        user.profile.name = name
        user.profile.family_name = family_name
        user.profile.phone_number = phone_numer
        user.profile.date_of_birth = date_of_birth
        user.profile.bio = bio
        user.profile.save()   # don't forget to save!

        return user




class GetUserInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='profile.name', read_only=True)
    family_name = serializers.CharField(source='profile.family_name', read_only=True)
    phone_number = serializers.CharField(source='profile.phone_number', read_only=True)
    date_of_birth = serializers.DateField(source='profile.date_of_birth', read_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'family_name', 'phone_number', 'date_of_birth', 'bio']
        read_only_fields = ['username', 'email']




class UserPasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password2']

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError("The old password you entered is incorrect. Try again.")
        return value

    def validate(self, attrs):
        if not attrs['new_password'] == attrs['new_password2']:
            raise serializers.ValidationError("your new passwords don't match. try again.")
        return attrs

    def update(self, instance, validated_data):
        password = validated_data['new_password']
        instance.set_password(password)
        instance.save()
        return instance
    
