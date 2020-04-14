from .views import get_document_list, get_document_detail, index


def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/document/list/', get_document_list, name='get_document_list')
    app.router.add_get('/document/{document_id}/', get_document_detail, name='get_document_detail')
