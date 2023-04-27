from __future__ import annotations
from pathlib import Path

from django.db import models


# Callable functions
UPLOADS_PATH = Path("novels/")


def novel_cover_path(instance: NovelCover, filename: str) -> str:
    stem = f"cover-{instance.id}"
    path = Path(
        f"{instance.novel.id}/{filename}").with_stem(stem)
    return str(UPLOADS_PATH / path)


def chapter_illustration_path(instance: ChapterIllustration, filename: str) -> str:
    stem = f"illus-{instance.chapter.number}-{instance.order}"
    path = Path(
        f"{instance.chapter.novel.id}/illustration/{filename}").with_stem(stem)
    return str(UPLOADS_PATH / path)

# Create your models here.


class Novel(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=600, blank=True)
    release_date = models.DateField(blank=True)
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
    number = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.novel}: chapter {self.number}"


class ChapterIllustration(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    illustration = models.ImageField(upload_to=chapter_illustration_path)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.chapter.novel}: illus {self.chapter.number}-{self.order}"
