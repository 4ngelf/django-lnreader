import pytest
from django.db.utils import IntegrityError

# from faker import Faker
from lnreader.models import (Novel,
                             NovelAltTitle,
                             NovelCover,
                             Chapter,
                             ChapterIllustration,
                             novel_cover_path,
                             chapter_illustration_path)

# Fixtures


@pytest.fixture
def create_novel(db, faker):
    def make_novel(**kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = faker.text(
                max_nb_chars=Novel.title.field.max_length)
        if 'description' not in kwargs:
            kwargs['description'] = faker.text(
                max_nb_chars=Novel.description.field.max_length)
        if 'release_date' not in kwargs:
            kwargs['release_date'] = faker.date_between(start_date='-20y')
        if 'raws_url' not in kwargs:
            kwargs['raws_url'] = faker.uri()

        return Novel.objects.create(**kwargs)
    return make_novel


@pytest.fixture
def create_novel_alt_title(db, faker, create_novel):
    def make_novel_alt_title(**kwargs):
        if 'novel' not in kwargs:
            kwargs['novel'] = create_novel()
        if 'title' not in kwargs:
            kwargs['title'] = faker.text(
                max_nb_chars=Novel.title.field.max_length)

        return NovelAltTitle.objects.create(**kwargs)
    return make_novel_alt_title


@pytest.fixture
def create_novel_cover(db, faker, create_novel):
    def make_novel_cover(**kwargs):
        if 'novel' not in kwargs:
            kwargs['novel'] = create_novel()
        if 'cover' not in kwargs:
            # TODO
            kwargs['cover'] = 'cover TODO'

        return NovelCover.objects.create(**kwargs)
    return make_novel_cover


@pytest.fixture
def create_chapter(db, faker, create_novel):
    def make_chapter(**kwargs):
        if 'novel' not in kwargs:
            kwargs['novel'] = create_novel()
        if 'number' not in kwargs:
            kwargs['number'] = faker.random_number(digits=3)
        if 'text' not in kwargs:
            length = min(faker.random_number(digits=4), 5000)
            kwargs['text'] = faker.text(max_nb_chars=length)

        return Chapter.objects.create(**kwargs)
    return make_chapter


@pytest.fixture
def create_chapter_illustration(db, faker, create_chapter):
    def make_chapter_illustration(**kwargs):
        if 'chapter' not in kwargs:
            kwargs['chapter'] = create_chapter()
        if 'illustration' not in kwargs:
            kwargs['illustration'] = 'illustration TODO'
        if 'order' not in kwargs:
            kwargs['order'] = faker.random_number(digits=1)

        return ChapterIllustration.objects.create(**kwargs)
    return make_chapter_illustration


# Tests


@pytest.mark.django_db
def test_all_models_create():
    """Test the empty creation of all models using django.db.models.QuerySet"""
    novel = Novel.objects.create()
    NovelAltTitle.objects.create(novel=novel)
    NovelCover.objects.create(novel=novel)
    chapter = Chapter.objects.create(novel=novel, number=1)
    ChapterIllustration.objects.create(chapter=chapter, order=1)

    for model in (Novel, NovelAltTitle, NovelCover, Chapter, ChapterIllustration):
        assert model.objects.count() >= 1


@pytest.mark.django_db
def test_all_fixtures_models_create(
        create_novel,
        create_novel_alt_title,
        create_novel_cover,
        create_chapter,
        create_chapter_illustration):
    assert isinstance(create_novel(), Novel)
    assert isinstance(create_novel_alt_title(), NovelAltTitle)
    assert isinstance(create_novel_cover(), NovelCover)
    assert isinstance(create_chapter(), Chapter)
    assert isinstance(create_chapter_illustration(), ChapterIllustration)


@pytest.mark.django_db
@pytest.mark.parametrize(
    '_model',
    [NovelAltTitle, NovelCover, Chapter, ChapterIllustration]
)
def test_model_raises_on_create_without_reference(_model):
    with pytest.raises(IntegrityError):
        _model.objects.create()


def test_novel_cover_path_function(faker, create_novel_cover, uploads_path):
    novelCover = create_novel_cover()
    dummy_file = faker.file_name(extension='.png')

    expected = f'{uploads_path}/{novelCover.novel.id}/cover-{novelCover.id}.png'

    assert novel_cover_path(novelCover, dummy_file) == expected


def test_chapter_illustration_path_function(faker, create_chapter_illustration, uploads_path):
    chapterIllustration = create_chapter_illustration()
    dummy_file = faker.file_name(extension='.png')

    expected = f'{uploads_path}/{chapterIllustration.chapter.novel.id}/illustration/' \
        + f'illus-{chapterIllustration.chapter.number}-{chapterIllustration.order}.png'

    assert chapter_illustration_path(
        chapterIllustration, dummy_file) == expected
