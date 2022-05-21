# from xml.dom import ValidationErr
# from rest_framework.serializers import ListSerializer,  ModelSerializer
from rest_framework import serializers
from ..models import Actor, Movie
from collections import OrderedDict

from rest_framework.exceptions import ErrorDetail, ValidationError

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields = ['id', 'movie_name','rating', 'created_at']


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
    movies = MovieSerializer(many=True)
    # override DRF fieldsactor
    errors = {}
    _errors = None
    validated_data = {}
    

    def validate(self, attrs):
        self._errors=[]
        # if actor_name is empty or not provided raise the custom error
        if not attrs.get("actor_name"):
            self._errors.append({"actor_name": "Actor Name required"})
            raise ValidationError(self._errors)
        
        elif isinstance(attrs.get("actor_name"), int):
            self._errors.append({"actor_name": "Invalid Data Type"})
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
    
    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        # print("actors:", validated_data)
        actor = Actor.objects.create(**validated_data)
        for movie in movies_data:
            Movie.objects.create(actor=actor, **movie)
        return actor
    
    def update(self, instance, validated_data):
        movies_data=validated_data.pop('movies')
        for movie in movies_data:
            movie_pk=movie.pop('id', None)
            if isinstance(movie_pk, int):
                try:
                    existing_movie=Movie.objects.get(id=movie_pk)
                    for key, value in movie.items():
                        setattr(existing_movie, key, value)
                    existing_movie.save()
                except Movie.DoesNotExist:
                    raise ValidationError(
                        [{
                            "movies_id": "Movies ID {} Does not Exist!!!".format(movie_pk)
                        }]
                    )
            else:
                raise ValidationError(
                    [{
                        "movies_id": "Invalid DataType(id), Valid Datatype is: {}".format('Number')
                    }]
                )



        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


        
