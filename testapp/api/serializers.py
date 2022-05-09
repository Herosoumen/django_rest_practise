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
        print("coming here........")
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

    


# class CustomValidationError(ValidationError):
    # def __init__(self, detail=None, code=None):
    #     print("detail:", detail)
    #     print("code:", code)
        # if detail is None:
        #     detail = self.default_detail
        # if code is None:
        #     code = self.default_code

        
        # # For validation failures, we may collect many errors together,
        # # so the details should always be coerced to a list if not already.
        # if isinstance(detail, tuple):
        #     detail = list(detail)
        # elif not isinstance(detail, dict) and not isinstance(detail, list):
        #     detail = [detail]

        # self.detail = _get_error_details(detail, code)


class ActorSerializer(serializers.ModelSerializer):
    # override DRF fields
    # errors = {}
    # _errors = None
    # validated_data = {}
    
    # def __new__(cls, *args, **kwargs):
    #     # We override this method in order to automatically create
    #     # `ListSerializer` classes instead when `many=True` is set.
    #     print("cls:", cls)
    #     print("kwargs.pop('many', False):", kwargs.pop('many'))
    #     if kwargs.pop('many', False):
    #         return cls.many_init(*args, **kwargs)
    #     return super().__new__(cls, *args, **kwargs)

    # def validate(self, attrs):
    #     self._errors={}
    #     # if actor_name is empty or not provided raise the custom error
    #     if not attrs.get("actor_name"):
    #         self._errors.update({"actor_name": "Actor Name required"})
    #         raise ValidationError(self._errors)
        
    #     elif isinstance(attrs.get("actor_name"), int):
    #         self._errors.update({"actor_name": "Invalid Data Type"})
    #         raisecd ValidationError(self._errors)

        
        # # set the overriden DRF serializer values
        # self._errors = None
        # self.validated_data = attrs
        # self._validated_data=OrderedDict([(k, v) for k, v in attrs.items()])
        # return attrs


    # def is_valid(self, raise_exception=False):
    #     # This implementation is the same as the default,
    #     assert hasattr(self, 'initial_data'), (
    #         'Cannot call `.is_valid()` as no `data=` keyword argument was '
    #         'passed when instantiating the serializer instance.'
    #     )
    #     if not hasattr(self, '_validated_data'):
    #         self.validate(self.initial_data)
    #     return not bool(self._errors)

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls()
        return CustomActorListSerializer(*args, **kwargs)

    class Meta:
        model = Actor
        fields = '__all__'
        list_serializer_class="CustomActorListSerializer"
       
        
      
 # def validate_actor_name(self, attrs):
    #     print("attrs:", attrs)
    #     if not attrs:
    #         raise serializers.ValidationError("Blog post is not about Django")
    #     return attrs

    # def validate(self, attrs):
    #     print("attrs:", attrs)
    #     if not attrs:
    #         raise serializers.ValidationError("Blog post is not about Django")
    #     return attrs


