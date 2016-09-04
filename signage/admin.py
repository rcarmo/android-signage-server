from django.contrib import admin

from django import forms, utils
from .models import Playlist, Alert
import json

class JSONEditorWidget(forms.Widget):
    html_template = """
        <div id='%(name)s_editor_holder'></div>
        <script type="text/javascript">
            var element = document.getElementById('%(name)s_editor_holder');
            var schema = JSON.parse('%(schema)s')
            var %(name)s_editor = new JSONEditor(element,
                {
                    schema: schema
                });
            %(name)s_editor.on('change', function() {
                    document.getElementById('id_%(name)s').value = JSON.stringify(%(name)s_editor.getValue());
                });
        </script>
        <textarea readonly class="vLargeTextField" cols="40" id="id_%(name)s" name="%(name)s" rows="10">%(value)s</textarea>
    """

    def __init__(self, attrs=None, formats=None, defaults=None):
        self.formats = formats
        self.defaults = defaults
        super(JSONEditorWidget, self).__init__(attrs)

    def build_schema(self, name, json_obj, inputs):
        inputs['title'] = name
        if isinstance(json_obj, list):
            inputs['type'] = 'array'
            inputs['uniqueItems'] = True
            default = []
            for key, value in enumerate(json_obj):
                default.append(value)
            inputs['default'] = default
            if self.formats and name in self.formats.keys():
                inputs['items'] = self.formats[name]
        elif isinstance(json_obj, dict):
            inputs['type'] = 'object'
            properties = {}
            for key, value in json_obj.items():
                properties[key] = self.build_schema(key, value, {})
            inputs['properties'] = properties
        elif isinstance(json_obj, (int)):
            inputs['type'] = 'integer'
            inputs['default'] = json_obj
        elif isinstance(json_obj, (basestring)):
            inputs['type'] = 'string'
            inputs['default'] = json_obj
        return inputs

    def render(self, name, value, attrs=None):
        if isinstance(value, basestring):  # Edit existing instance
            value = json.loads(value)
            schema = self.build_schema(name, value, {})
        else:  # Create a new instance
            schema = self.build_schema(name, self.defaults, {})

        result = self.html_template % {
            'name': name,
            'value': json.dumps(value),
            'schema': json.dumps(schema)
        }
        return utils.safestring.mark_safe(result)

class PlaylistForm(forms.ModelForm):
    playlist_default = [
        {'item': 'http://pixels.camp', 'duration': 5}
    ]
    playlist_format = {
        'type': 'array',
        'title': 'assets',
        'format': 'table',
        'items': {
            'type': 'object',
            'properties': {'item': {'type': 'string' },
            'duration': { 'type': 'integer' }}
        }
    }
    playlist = forms.CharField(widget=JSONEditorWidget(formats=playlist_format, defaults=playlist_default))
    
    class Meta:
        model = Playlist
        fields = '__all__'

# Register your models here.

class PlaylistAdmin(admin.ModelAdmin):
    form = PlaylistForm

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL')

        js = (static_url + 'admin/js/jsoneditor.min.js',
              static_url + 'admin/js/jsoneditor_init.js')
        css = {
            #'all': (static_url + 'admin/css/bootstrap.min.css',)
        }
admin.site.register(Playlist, PlaylistAdmin)
