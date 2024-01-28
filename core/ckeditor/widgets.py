from ckeditor.widgets import CKEditorWidget


class DarkCKEditorWidget(CKEditorWidget):

    class Media:
        css = {
            'all': ('/static/css/ckeditor-dark-theme.css',)
        }
