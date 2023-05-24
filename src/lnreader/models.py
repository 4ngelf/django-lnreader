from __future__ import annotations
from pathlib import Path

from django.db import models


# Callable functions
UPLOADS_PATH = Path("novels/")


def novel_cover_path(novel_cover: NovelCover, filename: str) -> str:
    """Returns path to the cover illustration image file for the novel.

    Args:
        novel_cover (NovelCover): Model to track the image file.
        filename (str): Original filename given to the image.

    Returns:
        str: Returns the next format:
            '<UPLOADS_PATH>/<novel-id>/cover-<cover-id>.[png|jpg|gif]'
    """
    stem = f"cover-{novel_cover.id}"
    path = Path(
        f"{novel_cover.novel.id}/{filename}").with_stem(stem)
    return str(UPLOADS_PATH / path)


def chapter_illustration_path(chapter_illustration: ChapterIllustration, filename: str) -> str:
    """Returns path to the illustration image file for the chapter of one novel.

    Args:
        chapter_illustration (ChapterIllustration): Model to track the image file.
        filename (str): Original filename given to the image.

    Returns:
        str: Returns the next format:
            '<UPLOADS_PATH>/<novel-id>/illustration/
            illus-<chapter-number>-<illus-order>.[png|jpg|gif]'
    """
    stem = f"illus-{chapter_illustration.chapter.number}-{chapter_illustration.order}"
    path = Path(
        f"{chapter_illustration.chapter.novel.id}/illustration/{filename}").with_stem(stem)
    return str(UPLOADS_PATH / path)

# Create your models here.


class Novel(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=600, blank=True)
    release_date = models.DateField(blank=True, null=True)
    raws_url = models.URLField(verbose_name="Raws URL", blank=True,
                               help_text="URL to original page the novel was published.")

    def __str__(self):
        return f"(LN){self.title[:15]}"


class NovelAltTitle(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)


class NovelCover(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to=novel_cover_path)


class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    number = models.CharField(max_length=16, unique=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.novel}: chapter {self.number}"


class ChapterIllustration(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    illustration = models.ImageField(upload_to=chapter_illustration_path)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.chapter.novel}: illus {self.chapter.number}-{self.order}"
