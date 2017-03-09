import os
from django.conf import settings
from django.contrib.staticfiles.views import serve


def serve_docs(request, path):

    docs_path = os.path.join(str(settings.DOCS_DIR), path)
    if os.path.isdir(docs_path):
        path = os.path.join(path, 'index.html')
    return serve(request, path)
