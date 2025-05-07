from dataclasses import dataclass


@dataclass
class AnimeInfo:
    id_anime: str
    title: str
    scope: str
    status: str
    progress_current: str
    progress_all: str
    date_started: str = None
    date_finished: str = None
