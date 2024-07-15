from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'media'))
application.add_files(os.path.join(BASE_DIR, 'media'), prefix='media/')
