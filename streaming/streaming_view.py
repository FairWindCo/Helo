import os

import requests
from django.contrib.auth.views import login_required
from django.http import StreamingHttpResponse


@login_required
def download(request):
    # handle user custom user permissions
    url = 'file_url_here'
    filename = os.path.basename(url)
    r = requests.get(url, stream=True)
    response = StreamingHttpResponse(streaming_content=r)
    response['Content-Disposition'] = f'attachement; filename="{filename}"'
    return response
