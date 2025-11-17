import os
import sys

# Add the Blog directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
blog_dir = os.path.join(current_dir, 'Blog')
sys.path.insert(0, current_dir)
sys.path.insert(0, blog_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')

try:
    from django.core.wsgi import get_wsgi_application
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable?"
    ) from exc

application = get_wsgi_application()
app = application
