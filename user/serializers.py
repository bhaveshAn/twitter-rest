from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.models import Profile, CustomUser


class ProfileSerializerOut(
    serializers.ModelSerializer
):  # Serializer for when data needs for GET purposes
    class Meta:
        model = Profile
        fields = ("id", "following")


class UserSerializerOut(
    serializers.ModelSerializer
):  # Serializer for when data needs for GET purposes

    following = ProfileSerializerOut(many=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "replies",
            "username",
            "email",
            "followers",
            "following",
        )


class UserSerializerCreate(
    serializers.ModelSerializer
):  # Serializer for creating an account

    username = serializers.SlugField(
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(), message="Username already taken."
            )
        ],
    )
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            **validated_data
        )  # When being created, call create user function
        return user
