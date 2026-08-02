from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)

from .models import Property, MentorshipProgram, Testimonial, Inquiry, Insight
from .permissions import IsAdminOrReadOnly
from .serializers import (
    UserRegisterSerializer,
    UserProfileSerializer,
    PropertySerializer,
    MentorshipProgramSerializer,
    TestimonialSerializer,
    InquirySerializer,
    InsightSerializer,
)

User = get_user_model()


# Property Views

@extend_schema_view(
    list=extend_schema(
        summary="List all properties",
        description="Retrieve a list of architectural properties. Supports filtering by featured flag and status.",
        parameters=[
            OpenApiParameter('featured', OpenApiTypes.STR, description="Filter by featured status ('true' or 'false')"),
            OpenApiParameter('status', OpenApiTypes.STR, description="Filter by property status (e.g., AVAILABLE, SOLD, RESERVED)"),
        ],
        tags=["Properties"]
    ),
    retrieve=extend_schema(
        summary="Get property details",
        description="Retrieve full details for a single property using its slug.",
        tags=["Properties"]
    ),
    create=extend_schema(
        summary="Create property",
        description="Add a new property listing. Requires staff permissions.",
        tags=["Properties"]
    ),
    update=extend_schema(
        summary="Update property",
        description="Update all fields of an existing property listing. Requires staff permissions.",
        tags=["Properties"]
    ),
    partial_update=extend_schema(
        summary="Partially update property",
        description="Update select fields of an existing property listing. Requires staff permissions.",
        tags=["Properties"]
    ),
    destroy=extend_schema(
        summary="Delete property",
        description="Remove a property listing. Requires staff permissions.",
        tags=["Properties"]
    ),
)
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'tagline', 'architectural_highlights', 'comfort_features']
    ordering_fields = ['created_at', 'price']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_featured = self.request.query_params.get('featured')
        status_filter = self.request.query_params.get('status')

        if is_featured == 'true':
            queryset = queryset.filter(is_featured=True)
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())

        return queryset


# Mentorship Program Views

@extend_schema_view(
    list=extend_schema(
        summary="List mentorship programs",
        description="Public visitors see only active programs open for application. Staff members can view all programs.",
        tags=["Mentorship"]
    ),
    retrieve=extend_schema(
        summary="Get mentorship program details",
        description="Retrieve details for a specific mentorship program.",
        tags=["Mentorship"]
    ),
    create=extend_schema(
        summary="Create mentorship program",
        description="Add a new mentorship program. Requires staff permissions.",
        tags=["Mentorship"]
    ),
    update=extend_schema(
        summary="Update mentorship program",
        description="Update an existing mentorship program. Requires staff permissions.",
        tags=["Mentorship"]
    ),
    partial_update=extend_schema(
        summary="Partially update mentorship program",
        description="Partially update an existing mentorship program. Requires staff permissions.",
        tags=["Mentorship"]
    ),
    destroy=extend_schema(
        summary="Delete mentorship program",
        description="Remove a mentorship program. Requires staff permissions.",
        tags=["Mentorship"]
    ),
)
class MentorshipProgramViewSet(viewsets.ModelViewSet):
    queryset = MentorshipProgram.objects.all()
    serializer_class = MentorshipProgramSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering = ['order', 'title']

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return MentorshipProgram.objects.all()
        return MentorshipProgram.objects.filter(is_open_for_application=True)


# Testimonial Views

@extend_schema_view(
    list=extend_schema(
        summary="List testimonials",
        description="Retrieve testimonials with optional filters for category and featured status.",
        parameters=[
            OpenApiParameter('category', OpenApiTypes.STR, description="Filter by category (REAL_ESTATE, MENTORSHIP, INVESTOR)"),
            OpenApiParameter('featured', OpenApiTypes.STR, description="Filter by featured status ('true' or 'false')"),
        ],
        tags=["Testimonials"]
    ),
    retrieve=extend_schema(summary="Get testimonial details", tags=["Testimonials"]),
    create=extend_schema(summary="Create testimonial", tags=["Testimonials"]),
    update=extend_schema(summary="Update testimonial", tags=["Testimonials"]),
    partial_update=extend_schema(summary="Partially update testimonial", tags=["Testimonials"]),
    destroy=extend_schema(summary="Delete testimonial", tags=["Testimonials"]),
)
class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        featured = self.request.query_params.get('featured')

        if category:
            queryset = queryset.filter(category=category.upper())
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset


# Insight Views

@extend_schema_view(
    list=extend_schema(
        summary="List insights / articles",
        description="Public visitors view published articles. Staff members view all articles including drafts.",
        tags=["Insights"]
    ),
    retrieve=extend_schema(
        summary="Get insight details",
        description="Retrieve an article using its slug.",
        tags=["Insights"]
    ),
    create=extend_schema(summary="Create insight", tags=["Insights"]),
    update=extend_schema(summary="Update insight", tags=["Insights"]),
    partial_update=extend_schema(summary="Partially update insight", tags=["Insights"]),
    destroy=extend_schema(summary="Delete insight", tags=["Insights"]),
)
class InsightViewSet(viewsets.ModelViewSet):
    queryset = Insight.objects.all()
    serializer_class = InsightSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['published_at']

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Insight.objects.all()
        return Insight.objects.filter(is_published=True)


# Inquiry / Lead Views

@extend_schema_view(
    create=extend_schema(
        summary="Submit an inquiry",
        description="Public endpoint to submit a lead or inquiry regarding properties, mentorship, or general requests.",
        tags=["Inquiries"]
    ),
    list=extend_schema(summary="List inquiries (Admin only)", tags=["Inquiries"]),
    retrieve=extend_schema(summary="Get inquiry details (Admin only)", tags=["Inquiries"]),
    update=extend_schema(summary="Update inquiry status (Admin only)", tags=["Inquiries"]),
    partial_update=extend_schema(summary="Partially update inquiry (Admin only)", tags=["Inquiries"]),
    destroy=extend_schema(summary="Delete inquiry (Admin only)", tags=["Inquiries"]),
)
class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'phone', 'message']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


# User & Auth Views

@extend_schema(
    summary="Register a new user",
    description="Registers a new user account with default role CLIENT.",
    tags=["Authentication"]
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    get=extend_schema(summary="Get authenticated profile", tags=["User Profile"]),
    put=extend_schema(summary="Update profile", tags=["User Profile"]),
    patch=extend_schema(summary="Partially update profile", tags=["User Profile"]),
    delete=extend_schema(summary="Delete account", tags=["User Profile"]),
)
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema_view(
    list=extend_schema(summary="List all users (Admin only)", tags=["Admin User Management"]),
    retrieve=extend_schema(summary="Get user details (Admin only)", tags=["Admin User Management"]),
    create=extend_schema(summary="Create user (Admin only)", tags=["Admin User Management"]),
    update=extend_schema(summary="Update user (Admin only)", tags=["Admin User Management"]),
    partial_update=extend_schema(summary="Partially update user (Admin only)", tags=["Admin User Management"]),
    destroy=extend_schema(summary="Delete user (Admin only)", tags=["Admin User Management"]),
)
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']