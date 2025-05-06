from dataclasses import dataclass


@dataclass
class AnimeInfo:
    def __init__(self, title, id_anime, scope, status, progress_current, progress_all, date_started, date_finished):
        self.title = title
        self.id_anime = id_anime
        self.scope = scope
        self.status = status
        self.progress_current = progress_current
        self.progress_all = progress_all
        self.date_finished = date_finished

    title: str
    id_anime: int
    score: str
    status: str
    progress_current: str
    progress_all: str
    date_started: str
    date_finished: str