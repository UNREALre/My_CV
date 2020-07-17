# -*- coding: utf-8 -*-
from cvapp import app, db, cli
from cvapp.models import User


@app.shell_context_processor
def make_shell_context():
    """Current function will be called to create current app context when calling '$ flash shell' from CLI"""

    return {
        'db': db,
        'User': User
    }