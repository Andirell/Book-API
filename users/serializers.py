from rest_framework import serializers
from .models import User, Author
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'about', 'role', 'confirm_password')

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if first_name[0] == first_name[0].lower():
            raise serializers.ValidationError({"firstname": "Must start with capital letter"})
        
        if last_name[0] == last_name[0].lower():
            raise serializers.ValidationError({"lastname": "Must start with capital letter"})
        
        if confirm_password != password:
            raise serializers.ValidationError({"password": "Password did not match"})
        
        validate_password(password)

        return attrs
    
    def create(self, validated_data):
        user = User(
                first_name = validated_data.get("first_name"),
                last_name = validated_data.get("last_name"),
                email = validated_data.get("email")
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user
    

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Author
        fields = ["user", "genres"]
        read_only_field = ("user")