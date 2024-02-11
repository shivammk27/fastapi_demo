## any kind of data that we have in the application as well as model classes that define structure of that data
from datetime import date
from enum import Enum
from pydantic import BaseModel, validator

class GenreURLChoice(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'

class GenreChoice(Enum):
    ROCK = 'Rock'
    ELECTRONIC = 'Electronic'
    METAL = 'Metal'
    HIP_HOP = 'Hip-Hop'

class Album(BaseModel):
    title: str
    release_date: date

class BandBase(BaseModel):
    name: str
    genre: GenreChoice
    albums: list[Album] = [] ## defaulting it to empty list bcs some bands might not have an album yet

class BandCreate(BandBase):
    @validator('genre', pre=True)
    def title_case_genre(cls, value):
        return value.title()

class BandWithId(BandBase):
    id: int