# from xml.dom import ValidationErr
# from rest_framework.serializers import ListSerializer,  ModelSerializer
from rest_framework import serializers
from ..models import Actor, Movie
from collections import OrderedDict

from rest_framework.exceptions import ErrorDetail, ValidationError

class CustomActorListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        super(CustomActorListSerializer, self).__init__(*args, **kwargs)
    
    validated_data = {}
    def validate(self, attrs):
        self.has_error=False
        self._validated_data=[]
        self._errors=[]
        for item in attrs:
            # if actor_name is empty or not provided raise the custom error
            if not item.get("actor_name"):
                self.has_error=True
                self._errors.append({"actor_name": "Actor Name required"})
            
            elif isinstance(item.get("actor_name"), int):
                self.has_error=True
                self._errors.append({"actor_name": "Invalid Data Type"})
            else:
                self._validated_data.append(
                    OrderedDict([(k, v) for k, v in item.items()])
                )
                self._errors.append({})
        print("self.has_error:", self.has_error)
        if self.has_error:
            raise ValidationError(self._errors)
        
        self.validated_data=attrs
        return attrs
    

    def is_valid(self, raise_exception=False):
        # This implementation is the same as the default,
        # except that we use lists, rather than dicts, as the empty case.
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self.validate(self.initial_data)
            except ValidationError as exc:
                self._validated_data = []
                self._errors = exc.detail
            else:
                self._errors = []

        # if self._errors and raise_exception:
        #     raise ValidationError(self.errors)
        print("self._errors:", self._errors)
        return not bool(self._errors)


class ActorSerializer(serializers.ModelSerializer):
    # override DRF fields
    errors = {}
    _errors = None
    validated_data = {}
    

    def validate(self, attrs):
        self._errors={}
        # if actor_name is empty or not provided raise the custom error
        if not attrs.get("actor_name"):
            self._errors.update({"actor_name": "Actor Name required"})
            raise ValidationError(self._errors)
        
        elif isinstance(attrs.get("actor_name"), int):
            self._errors.update({"actor_name": "Invalid Data Type"})
            raise ValidationError(self._errors)

        
        # set the overriden DRF serializer values
        self._errors = None
        self.validated_data = attrs
        self._validated_data=OrderedDict([(k, v) for k, v in attrs.items()])
        return attrs


    def is_valid(self, raise_exception=False):
        # This implementation is the same as the default,
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )
        if not hasattr(self, '_validated_data'):
            self.validate(self.initial_data)
        return not bool(self._errors)

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls()
        return CustomActorListSerializer(*args, **kwargs)

    class Meta:
        model = Actor
        fields = '__all__'
        list_serializer_class="CustomActorListSerializer"
       
        
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields = ['movie_name', 'created_at']
        # extra_kwargs = {
        #     'actor': {'write_only': True}
        # }