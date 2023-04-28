import pytest

from lnreader.models import Novel, NovelAltTitle, NovelCover, Chapter, ChapterIllustration


@pytest.mark.django_db
def test_novel_create():
    Novel.objects.create()
    assert Novel.objects.count() >= 1


@pytest.mark.django_db
def test_novel_title_is_empty():
    Novel.objects.create()
    assert Novel.objects.first().title == ""


@pytest.mark.django_db
def test_new_novel_title_is_empty():
    title = "Book 1"
    Novel.objects.create(title=title)
    assert Novel.objects.first().title == title


@pytest.mark.django_db
def test_all_create():
    novel = Novel.objects.create(title="Book 1")
    novelalt = NovelAltTitle.objects.create(novel=novel, title="book n1")
    NovelCover.objects.create(novel=novel)
    chapter = Chapter.objects.create(novel=novel, number=1)
    ChapterIllustration.objects.create(chapter=chapter, order=1)

    for model in (Novel, NovelAltTitle, NovelCover, Chapter, ChapterIllustration):
        assert model.objects.count() >= 1
