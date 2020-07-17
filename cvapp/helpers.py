# -*- coding: utf-8 -*-
import os
from config import project_root
from cvapp.models import Settings
from werkzeug.utils import secure_filename


def css_js_update_time(for_public=False):
    """Возвращает словарь с временем обновлений статики. Если for_public - то обходим паблик статику."""

    if for_public:
        static = {
            'public/css/custom.css': 0,
        }
    else:
        static = {
            'admin/css/custom.css': 0,
            'admin/css/bootstrap.min.css': 0,
        }

    for path, time in static.items():
        static[path] = os.path.getmtime(os.path.join(project_root, 'cvapp/static', path))

    return static


def get_settings():
    db_settings = Settings.query.all()
    settings = {}
    for setting in db_settings:
        settings[setting.param_name] = setting.param_value

    return settings


def save_uploaded_file(upload_folder, form_file):
    """Saves files uploaded from admin area"""

    filename = secure_filename(form_file.data.filename)
    file_path = os.path.join(project_root, upload_folder, filename)
    form_file.data.save(file_path)

    return filename
