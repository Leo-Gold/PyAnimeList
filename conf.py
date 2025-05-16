from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    DATA_FOLDER: Path = './data'

    SHIKIMORI_CLIENT_ID: str
    SHIKIMORI_CLIENT_SECRET: str

    MAL_USERNAME: str
    SHIKIMORI_USERNAME: str

    @property
    def DATA_SOURCE_SHIKIMORI(self) -> Path:
        return self.DATA_FOLDER / 'source' / 'shikimori'
    @property
    def DATA_SOURCE_MYANIMELIST(self) -> Path:
        return self.DATA_FOLDER / 'source' / 'myanimelist'

    @property
    def DATA_JSON_MYANIMELIST(self) -> Path:
        return self.DATA_FOLDER / 'json' / 'myanimelist'

    STATUS_SELECTED: list = [
        {'name': 'Currently Watching', 'id': 1, 'status': 'watching'},
        {'name': 'Completed', 'id': 2,  'status': 'completed'},
        {'name': 'On Hold', 'id': 3,  'status': 'on_hold'},
        {'name': 'Dropped', 'id': 4,  'status': 'dropped'},
        {'name': 'Plan to Watch', 'id': 6,  'status': 'planned'}
    ]

    HTML_TAG_TD: list = [
        {'class': 'td1'},
        {'class': 'td2'},
    ]

    SHIKIMORI_LIMIT: int = 1000


settings = Settings()
