from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from .models import Book
from users.models import Author
from django.shortcuts import get_object_or_404
from .permissions import is_Author

# -----------------------------------------------------------------------------
# Swagger / OpenAPI (drf-spectacular)
# These imports do NOT change how the API runs. They tell drf-spectacular how
# to build the schema file that Swagger UI reads at /api/docs/.
# -----------------------------------------------------------------------------

from rest_framework import serializers as drf_serializers  # tiny "shape" serializers used only for docs
from drf_spectacular.utils import (
    extend_schema,  # describes ONE HTTP method (GET, POST, etc.)
    extend_schema_view,  # attaches those descriptions to a class-based view
    inline_serializer,  # defines a JSON shape in code without a separate Serializer class
    OpenApiParameter,  # documents query params (?genre=) or path params (/.../5/)
    OpenApiResponse,  # documents a response that has no JSON body (e.g. 204)
)
from drf_spectacular.types import OpenApiTypes  # common OpenAPI types (string, int, etc.)

# --- Response "envelopes" for Swagger only (match what your views actually return) ---
# inline_serializer(..., name="...") becomes a named schema in the OpenAPI document.

# Documents: {"message": "...", "data": [...books...]} for successful GET list
_book_list_response = inline_serializer(
    name="BookListEnvelope",
    fields={
        "message": drf_serializers.CharField(),
        "data": BookSerializer(many=True),
    }
)

# Documents: { "message": "..." } after successful POST / PUT / PATCH
_book_message_ok = inline_serializer(
    name="BookMessageOk",
    fields={"message": drf_serializers.CharField()},
)

# Documents: { "message": "..." } when the book id does not exist (404)
_book_not_found = inline_serializer(
    name="BookMessageOk",
    fields={"message": drf_serializers.CharField()}
)

# Documents: { "errors": { ...field errors... } } when validation fails (400)
_book_validation_errors = inline_serializer(
    name="BookValidationErrors",
    fields={"errors": drf_serializers.DictField()},
)

# Re-used for PUT, PATCH, DELETE: the `{id}` piece in the URL
_path_id = OpenApiParameter(
    name= "id",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.PATH,
    required=True,
    description="Book primary key",
)

# @extend_schema_view maps each HTTP method on Books to its own extend_schema(...).
# Swagger UI will show: summary, description, request body, responses, and tags.
# JWT is picked up automatically from settings (DEFAULT_AUTHENTICATION_CLASSES).
@extend_schema_view(
    # GET /books/endpoint/ — list books; optional ?genre= in Swagger "Parameters"
    get=extend_schema(
        summary="List books",
        description="Retrieve all books. Optionally filter by genre using the query parameter.",
        parameters=[
            OpenApiParameter(
                name="genre",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter books by genre",
            ),
        ],
        responses={200: _book_list_response},
        tags=["Books"],  # groups this operation under "Books" in Swagger sidebar
    ),
    # POST /books/endpoint/ — Swagger shows JSON body from BookSerializer; "Try it out" can send it
    post=extend_schema(
        summary="Create book",
        request=BookSerializer,
        responses={
            200: _book_message_ok,
            400: _book_validation_errors,
        },
        tags=["Books"],
    ),
    # PUT /books/endpoint/<id>/ — full replace; path id + JSON body in Swagger
    put=extend_schema(
        summary="Replace book",
        parameters=[_path_id],
        request=BookSerializer,
        responses={
            200: _book_message_ok,
            400: _book_validation_errors,
            404: _book_not_found,
        },
        tags=["Books"],
    ),
    # PATCH /books/endpoint/<id>/ — partial update; Spectacular may show "PatchedBook" (all fields optional)
    patch=extend_schema(
        summary="Partially update book",
        parameters=[_path_id],
        request=BookSerializer,
        responses={
            200: _book_message_ok,
            400: _book_validation_errors,
            404: _book_not_found,
        },
        tags=["Books"],
    ),
    # DELETE /books/endpoint/<id>/ — 204 means success with empty body
    delete=extend_schema(
        summary="Delete book",
        parameters=[_path_id],
        responses={
            204: OpenApiResponse(description="No content"),
            404: _book_not_found,
        },
        tags=["Books"],
    ),
)


# Create your views here.
class Books(APIView):
    permission_classes= [is_Author]
    def get(self, request):
        books = Book.objects.all()

        genre = request.query_params.get("genre") # retrieving data frm query params

        if genre:
            books = Book.objects.filter(genre=genre)


        serializer = BookSerializer(books, many=True)
        return Response({"message": "get request successful", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)

        author = get_object_or_404(Author, user=request.user)

        if serializer.is_valid():
            serializer.save(author=author)
            return Response({"message": "post request successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({"message": "put request successful"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "post request successful"}, status=status.HTTP_200_OK) 
        else:
            return Response({"errors": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({"message": "put request successful"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "patch request successful"}, status=status.HTTP_200_OK) 
        else:
            return Response({"errors": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({"message": "The book you are looking for does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
