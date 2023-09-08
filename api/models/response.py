from dataclasses import dataclass


@dataclass(slots=True)
class FileInfo:
    language: str | None
    extension: str
    size: str


@dataclass(slots=True)
class RecentDownload:
    title: str
    url: str


@dataclass(slots=True)
class URL:
    title: str
    url: str


@dataclass(slots=True)
class SearchResult:
    title: str
    authors: str
    publisher: str | None
    publish_date: str | None
    thumbnail: str | None
    path: str
    file_info: FileInfo


@dataclass(slots=True)
class Download:
    title: str
    authors: str
    description: str
    publisher: str | None
    publish_date: str | None
    thumbnail: str | None
    file_info: FileInfo
    urls: list[URL]
