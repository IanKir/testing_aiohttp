from .views import get_document_list, get_document_detail, index, add_document, update_document


def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/document/list/', get_document_list, name='get_document_list')
    app.router.add_get('/document/new/', add_document, name='add_document')
    app.router.add_post('/document/new/', add_document, name='add_document')
    app.router.add_get('/document/{document_id}/', get_document_detail, name='get_document_detail')
    app.router.add_get('/document/{document_id}/edit', update_document, name='update_document')
    app.router.add_post('/document/{document_id}/edit', update_document, name='update_document')


