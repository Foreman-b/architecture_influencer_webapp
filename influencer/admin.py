from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Property, MentorshipProgram, Testimonial, Inquiry, Insight


admin.site.site_header = "Architecture Influencer Admin"
admin.site.site_title = "AI Portal"
admin.site.index_title = "Management Dashboard"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'username', 'phone_number', 'avatar', 'bio')}),
        (_('Permissions & Role'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'location', 'price', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured', 'created_at')
    search_fields = ('title', 'location', 'tagline', 'architectural_highlights', 'comfort_features')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_featured')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Overview', {
            'fields': ('title', 'slug', 'tagline', 'status', 'is_featured')
        }),
        ('Location & Pricing', {
            'fields': ('location', 'price')
        }),
        ('Brand Specs (Architecture + Comfort)', {
            'fields': ('architectural_highlights', 'comfort_features')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
    )


@admin.register(MentorshipProgram)
class MentorshipProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'program_type', 'duration', 'is_open_for_application', 'order')
    list_filter = ('program_type', 'is_open_for_application')
    search_fields = ('title', 'description', 'key_takeaways')
    list_editable = ('is_open_for_application', 'order')
    ordering = ('order', 'title')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_or_title', 'category', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'role_or_title', 'quote')
    list_editable = ('is_featured',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'intent', 'is_processed', 'created_at')
    list_filter = ('intent', 'is_processed', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'message')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at', 'user', 'full_name', 'email', 'phone', 'intent', 'message')
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_processed', 'mark_as_unprocessed']

    @admin.action(description="Mark selected inquiries as Processed")
    def mark_as_processed(self, request, queryset):
        queryset.update(is_processed=True)

    @admin.action(description="Mark selected inquiries as Unprocessed")
    def mark_as_unprocessed(self, request, queryset):
        queryset.update(is_processed=False)


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    date_hierarchy = 'published_at'