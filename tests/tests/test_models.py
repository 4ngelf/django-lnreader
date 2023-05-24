import pytest

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
            kwargs['title'] = faker.text(max_nb_chars=Novel.title.max_length)
        if 'description' not in kwargs:
            kwargs['description'] = faker.text(
                max_nb_chars=Novel.description.max_length)
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
            kwargs['title'] = faker.text(max_nb_chars=Novel.title.max_length)

        return NovelAltTitle.objects.create(**kwargs)
    return make_novel_alt_title


@pytest.fixture
def create_novel_cover(db, faker, create_novel):
    def make_novel_cover(**kwargs):
        if 'novel' not in kwargs:
            kwargs['novel'] = create_novel()
        if 'cover' not in kwargs:
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
    novel = Novel.objects.create()
    NovelAltTitle.objects.create(novel=novel)
    NovelCover.objects.create(novel=novel)
    chapter = Chapter.objects.create(novel=novel, number=1)
    ChapterIllustration.objects.create(chapter=chapter, order=1)

    for model in (Novel, NovelAltTitle, NovelCover, Chapter, ChapterIllustration):
        assert model.objects.count() >= 1


@pytest.mark.django_db
def test_novel_create(create_novel):
    novel = create_novel
    assert isinstance(novel, Novel)
