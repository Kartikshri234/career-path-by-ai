#!/usr/bin/env python
<<<<<<< HEAD
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
=======
import os
import sys

def main():
>>>>>>> 85979af9c9ab7ae4dc87a2ca7b9ae268d7bb6f8b
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careercompass.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

<<<<<<< HEAD

=======
>>>>>>> 85979af9c9ab7ae4dc87a2ca7b9ae268d7bb6f8b
if __name__ == '__main__':
    main()
