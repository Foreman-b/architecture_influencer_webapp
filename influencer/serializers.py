from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Property, MentorshipProgram, Testimonial, Inquiry, Insight
from drf_spectacular.utils import extend_schema_field

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'phone_number', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', User.Role.CLIENT),
            phone_number=validated_data.get('phone_number', ''),
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'role_display', 'phone_number', 'avatar', 'bio']
        read_only_fields = ['id', 'email', 'role']


# Property Serializer

class PropertySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 
            'title', 
            'slug', 
            'tagline', 
            'location', 
            'price', 
            'status', 
            'status_display',
            'architectural_highlights', 
            'comfort_features', 
            'cover_image', 
            'is_featured', 
            'created_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at']


# Mentorship Program Serializer

class MentorshipProgramSerializer(serializers.ModelSerializer):
    program_type_display = serializers.CharField(source='get_program_type_display', read_only=True)
    key_takeaways_list = serializers.SerializerMethodField()

    class Meta:
        model = MentorshipProgram
        fields = [
            'id', 
            'title', 
            'program_type', 
            'program_type_display', 
            'description', 
            'key_takeaways', 
            'key_takeaways_list', 
            'duration', 
            'is_open_for_application', 
            'order'
        ]
        read_only_fields = ['id']
    
    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_key_takeaways_list(self, obj):
        if obj.key_takeaways:
            return [item.strip() for item in obj.key_takeaways.split('\n') if item.strip()]
        return []


# Testimonial Serializer

class TestimonialSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'role_or_title', 'category', 'category_display', 'quote', 'avatar', 'is_featured']
        read_only_fields = ['id']


# Inquiry / Lead Serializer

class InquirySerializer(serializers.ModelSerializer):
    intent_display = serializers.CharField(source='get_intent_display', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Inquiry
        fields = [
            'id', 
            'user', 
            'user_email', 
            'full_name', 
            'email', 
            'phone', 
            'intent', 
            'intent_display', 
            'message', 
            'is_processed', 
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'is_processed', 'created_at']


# Insight / Article Serializer

class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = ['id', 'title', 'slug', 'summary', 'content', 'featured_image', 'is_published', 'published_at']
        read_only_fields = ['id', 'slug', 'published_at']