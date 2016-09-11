from django.core.exceptions import ValidationError
from django.forms import MultiWidget, ChoiceField, CharField, MultiValueField

class OptionalChoiceWidget(MultiWidget):
    def decompress(self,value):
        if value: #indicates we have a updating object versus new one
            if value in [x[0] for x in self.widgets[0].choices]:
                 return [value,""] # make it set the pulldown to choice
            else:
                 return ["",value] # keep pulldown to blank, set freetext
        return ["",""] # default for new object

class OptionalChoiceField(MultiValueField):
    def __init__(self, choices, max_length=80, *args, **kwargs):
        """ sets the two fields as not required but will enforce that (at least) one is set in compress """
        fields = (ChoiceField(choices=choices,required=False),
                  CharField(required=False))
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super(OptionalChoiceField,self).__init__(required=False,fields=fields,*args,**kwargs)
    def compress(self,data_list):
        """ return the choicefield value if selected or charfield value (if both empty, will throw exception """
        if not data_list:
            raise ValidationError('Need to select choice or enter text for this field')
        return data_list[0] or data_list[1]