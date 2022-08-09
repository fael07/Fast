from Fast.sheets.app import DjangoApp
from Fast.sheets.shortcuts import create_archives
from ..comand import BasicCommand
from django.conf import settings
from pathlib import Path
from directory_tree import display_tree


    


class Command(BasicCommand):

    help = 'Command for create fast app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('--use_folders', '-f', action='store_true')
        parser.add_argument('app_folder', type=str, default=settings.DEFAULT_APPS_FOLDER)
    
    def handle(self, *args, **options):
        # create folder
        app_folder = self.get_app_folder(options)
        new_app_path = Path(settings.BASE_DIR, app_folder, options['app_name'])
        new_app_path.mkdir()
        self.create_app_folders(new_app_path, options)
        self.create_app_archives(new_app_path, options)
        app = DjangoApp(str(settings.BASE_DIR), f'{app_folder}/{options["app_name"]}', options['app_name'], settings.PROJECT_NAME)
        app.create_url_archive()
        app.start_files()
        app.import_for_model()
        app.config_app(app_folder)
        app.register_app(app_folder)
        display_tree(str(new_app_path))
        self.show_actions([
            'create app - https://docs.djangoproject.com/en/4.0/ref/django-admin/#startapp', 
            'register app in settings.INSTALLED_APPS - https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-INSTALLED_APPS',
        ])

    
    def create_app_folders(self, app_path: Path, options: dict):
        more_folders = ['app/models', 'app/views'] if options['use_folders'] else []
        folders = [
            'app',
            'app/migrations',
            'app/tests',
            'actions',
            'actions/functions',
            'actions/objects',
            *more_folders,
        ]
        for folder in folders:
            new_path = Path(app_path, folder)
            new_path.mkdir()

    def create_app_archives(self, app_path: Path, options: dict):
        more_folders = ['app/models/__init__.py', 'app/views/__init__.py'] if options['use_folders'] else ['app/models.py', 'views.py',]
        create_archives(app_path, [
            '__init__.py',
            'actions/functions/__init__.py',
            'actions/objects/__init__.py',
            'urls.py',
            'app/__init__.py',
            'app/admin.py',
            'app/tests/models_t.py',
            'app/tests/views_t.py',
            'app/migrations/__init__.py',
            'app/tests/__init__.py',
            *more_folders,
        ])


        

        