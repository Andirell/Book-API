from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from users import serializers
from rest_framework import permissions
from .models import Author
from rest_framework import serializers as drf_serializers
'''
Swagger / OpenApi (drf-spectacular)
@extend_schema sits Above @Api_view so spectacular can document each endpoint 

'''

from drf_spectacular.utils import extend_schema, inline_serializer

# Auth imports
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# Successfu; signup: { "message": "..."}
SignupSuccess = inline_serializer(
    name="SignupSuccess",
    fields={"message": drf_serializers.CharField()},
)
# Validation or other errors: {"error": {...}}
SignupError = inline_serializer(
    name="SignupError",
    fields={"error": drf_serializers.DictField()},
)

# Body the client sends to /users/signin/ (email + password)
SignInRequest = inline_serializer(
    name= "SignInRequest",
    fields={
        "email": drf_serializers.EmailField(),
        "password": drf_serializers.CharField(),
    }
)

# Successful sign-in JSON (matches what signin() returns)
SignInResponse = inline_serializer(
    name= "SignInResponse",
    fields={
        "message": drf_serializers.CharField(),
        "access_token": drf_serializers.CharField(),
        "refresh_token": drf_serializers.CharField(),
    },
)

# Wrong email/password: {"error": "invalid credentials"}
SignInUnauthorized = inline_serializer(
    name="SignInUnauthorized",
    fields={"error": drf_serializers.CharField()}
)

# Author profile created successfully
AuthorCreated = inline_serializer(
    name="AuthorCreatedResponse",
    fields={"message": drf_serializers.CharField()},
)
# Serializer failed (shown as 401 in your view when invalid)
AuthorError = inline_serializer(
    name="AuthorErrorResponse",
    fields={"error": drf_serializers.DictField()},
)
# User already has an author row (your view returns 400 with a message)
AuthorExists = inline_serializer(
    name="AuthorAlreadyExists",
    fields={"message": drf_serializers.CharField()},
)



# Document POST /Users/signup/ - swagger shows the same fields as Userserializer
@extend_schema(
        summary="Register User",
        description="Create a new user account",
        tags=["Authentication"],
        request=serializers.UserSerializer,
        responses={
            201:SignupSuccess,
            400: SignupError,
        },

)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "sign up successful"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        summary="Sign in",
        description="Obtain JWT access and refresh tokens using email and password.",
        tags=["Authentication"],
        request=SignInRequest,
        responses={
            201:SignInResponse,
            400: SignInUnauthorized,
        },

)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signin(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email , password=password)

    if user is not None:
        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)
        return Response({"message": "sign in successful", "access_token": str(access), "refresh": str(refresh)}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Document POST /users/author/ — needs JWT: students click "Authorize" in Swagger first
@extend_schema(
    summary="Create author profile",
    description="Link the authenticated user to an author profile (genres, etc.). Requires a valid Bearer token.",
    tags=["Authors"],
    request=serializers.AuthorSerializer,
    responses={
        201: AuthorCreated,
        400: AuthorExists,
        401: AuthorError,
    },
)
@api_view(["POST"])
def add_author(request):
    print(request.user, ":the owner of token")
    serializer = serializers.AuthorSerializer(data=request.data)

   
    if Author.objects.filter(user=request.user).exists():
        return Response({"message": "An Author already exists for this user"}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"message": "Author data created"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)