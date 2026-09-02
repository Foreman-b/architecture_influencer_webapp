from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .views import (
    PropertyViewSet,
    MentorshipProgramViewSet,
    TestimonialViewSet,
    InsightViewSet,
    InquiryViewSet,
    AdminUserViewSet,
    RegisterView,
    UserProfileView,
)

app_name = 'influencer'
# Register ViewSets with the DefaultRouter
router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'mentorships', MentorshipProgramViewSet, basename='mentorship')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'insights', InsightViewSet, basename='insight')
router.register(r'inquiries', InquiryViewSet, basename='inquiry')
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')

urlpatterns = [
    # OpenAPI 3.0 Schema and API Documentation
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # SimpleJWT & Custom Auth Endpoints
    path('api/v1/auth/register', RegisterView.as_view(), name='auth_register'),
    path('api/v1/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/profile', UserProfileView.as_view(), name='auth_profile'),

    # API ViewSets Routes
    path('api/v1/', include(router.urls)),
]