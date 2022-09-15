from rest_framework import serializers
from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


class CreateUserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать me в качестве имени пользователя'
            )
        return data

    class Meta:
        fields = ('username', 'email')
        model = User


class LoginUserSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class MeUserSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        fields = (
            'id', 'name',
            'year', 'rating',
            'description', 'genre',
            'category'
        )
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class CurrentTitleDefault(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        return serializer_field.context[
            'request'
        ].parser_context['kwargs']['title_id']


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(required=True, min_value=1, max_value=10)
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    text = serializers.CharField(required=True)
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        model = Review
        fields = (
            'id', 'text',
            'author', 'score',
            'pub_date', 'title'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Нельзя дважды написать отзыв'
            )
        ]


class CurrentCommentDefault(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        return serializer_field.context[
            'request'
        ].parser_context['kwargs']['review_id']


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(default=serializers.CurrentUserDefault(),
                              slug_field='username', read_only=True)
    review = serializers.HiddenField(default=CurrentCommentDefault())

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')
