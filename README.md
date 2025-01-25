[# zoo_project](https://zoo-ticket-booking-8ca399c8e3fd.herokuapp.com/)



1:Configured the Django settings for development and production.
Added middleware, database configuration, and static file settings.
Configured authentication and custom user models.
# Database configuration
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }
    
    # Static files
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

 
2: Static Files Handling

 Added WhiteNoise middleware to handle static files in production.
Used the collectstatic command to gather static files into the staticfiles folder.

      # Middleware to handle static files
      MIDDLEWARE = [
          'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file handling
          # Other middleware...
      ]
      
      # Static file configuration
      STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
      STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



3: Custom User Model (models.py in blog app)

 Created a custom user model for better flexibility in handling user data.

     from django.contrib.auth.models import AbstractUser
    
    class CustomUser(AbstractUser):
        profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


4: Image Resizing for Profile Pictures (models.py in blog app)

Used the save method in the CustomUser model to resize images to a maximum of 300x300 pixels using the PIL library.

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

            
5:Post Ownership (views.py in blog app)

Restricted update and delete actions on blog posts to the original author using test_func in PostUpdateView and PostDeleteView.

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        
6:Database Migration

Ran Django migrations to set up the database schema on Heroku.
    
    heroku run python manage.py makemigrations --app <zoo_project.wsig> 
    heroku run python manage.py migrate --app <zoo_project.wsig>

7:Deployment Configuration (Procfile and runtime.txt)

Set up the Procfile to run the app on Heroku.
Specified the Python version in runtime.txt.


Procfile:web: gunicorn zoo_project.wsgi
runtime.txt:python-3.9.16

