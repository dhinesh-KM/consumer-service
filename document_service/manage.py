#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


<<<<<<< HEAD

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'document_service.settings.settings')
=======
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'document_service.settings')
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
<<<<<<< HEAD
    
=======
>>>>>>> cc9e5c6c578cf89656384fb8c303b19d52df6201
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
