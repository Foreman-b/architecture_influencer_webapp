from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin / Influencer'
        MENTEE = 'MENTEE', 'Mentee'
        INVESTOR = 'INVESTOR', 'Investor'
        CLIENT = 'CLIENT', 'Client'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, help_text="Short bio for mentees or investors")

    # Authenticate with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class Property(models.Model):
    class StatusChoices(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        INVESTED = 'INVESTED', 'Invested / Sold'
        UNDER_DEVELOPMENT = 'DEVELOPMENT', 'Under Development'

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=255, help_text="e.g., Ultra-modern eco-villa with integrated smart layout")
    location = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.AVAILABLE)
    
    # Core Brand Pillars
    architectural_highlights = models.TextField(help_text="Key design & structural specifications")
    comfort_features = models.TextField(help_text="Ergonomic & luxury lifestyle features")
    
    cover_image = models.ImageField(upload_to='properties/covers/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class MentorshipProgram(models.Model):
    class ProgramType(models.TextChoices):
        ONE_ON_ONE = '1ON1', '1-on-1 Executive Mentorship'
        COHORT = 'COHORT', 'Group Cohort'
        MASTERCLASS = 'MASTERCLASS', 'Masterclass / Workshop'

    title = models.CharField(max_length=200)
    program_type = models.CharField(max_length=20, choices=ProgramType.choices, default=ProgramType.COHORT)
    description = models.TextField()
    key_takeaways = models.TextField(help_text="Separate bullet points with line breaks")
    duration = models.CharField(max_length=50, help_text="e.g., 8 Weeks, 1-Day Intensive")
    is_open_for_application = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Ordering position on landing page display")

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    class Category(models.TextChoices):
        MENTEE = 'MENTEE', 'Mentee'
        INVESTOR = 'INVESTOR', 'Investor / Client'
        PEER = 'PEER', 'Industry Peer'

    name = models.CharField(max_length=100)
    role_or_title = models.CharField(max_length=150, help_text="e.g., Real Estate Investor / Mentee Alum")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.MENTEE)
    quote = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"



class Inquiry(models.Model):
    class IntentChoices(models.TextChoices):
        MENTORSHIP = 'MENTORSHIP', 'Mentorship Program'
        INVESTMENT = 'INVESTMENT', 'Real Estate / Investment Inquiry'
        SPEAKING = 'SPEAKING', 'Speaking / Media Request'
        GENERAL = 'GENERAL', 'General Contact'

    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='inquiries'
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    intent = models.CharField(max_length=20, choices=IntentChoices.choices, default=IntentChoices.GENERAL)
    message = models.TextField()
    
    # CRM status tracking
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.get_intent_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class Insight(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(max_length=300, help_text="Short card snippet for frontend preview")
    content = models.TextField()
    featured_image = models.ImageField(upload_to='insights/')
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

