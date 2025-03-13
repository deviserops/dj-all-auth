def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'