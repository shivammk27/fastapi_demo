from fastapi import FastAPI, HTTPException, Path, Query
from schemas import GenreURLChoice, BandBase, BandCreate, BandWithId
from typing import Union
from typing_extensions import Annotated

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twins', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
        {'title': 'Master of Reality', 'release_date': '1971-07-21'}
    ]},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'}
]

# @app.get('/bands')
# async def bands() -> list[dict]:
#     return BANDS


@app.get('/bands')
# we have data validation built in when we return list of bands. in list of dict there is no data validation. on the other hand when we tell the end point we are returning a list of model classes end pt is going to take each field of the model and is going to apply the validation logic. Also you also get the documentation for that particular model on swagger docs
async def bands(genre: Union[GenreURLChoice, None] = None, 
                q: Annotated[Union[str, None] , Query(max_length=10)] = None) -> list[BandWithId]:
    band_list = [BandWithId(**b) for b in BANDS]
    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]

    if q:
        band_list = [ b for b in band_list if q.lower() in b.name.lower()]

    # if has_albums:
    #     band_list = [
    #         b for b in band_list if len(b.albums) > 0
    #     ]

    return band_list

# @app.get('/bands/{band_id}') # possible to change the status code you get back @app.get('/bands/{band_id}', status_code=206)
# async def band(band_id: int) -> BandWithId:
#     band = next((BandWithId(**b) for b in BANDS if b['id']==band_id), None)
#     if band is None:
#         raise HTTPException(status_code=404, detail='Band not found')
#     return band
@app.get('/bands/{band_id}') # possible to change the status code you get back @app.get('/bands/{band_id}', status_code=206)
async def band(band_id: Annotated[int, Path(title="The Band ID")]) -> BandWithId:
    band = next((BandWithId(**b) for b in BANDS if b['id']==band_id), None)
    if band is None:
        raise HTTPException(status_code=404, detail='Band not found')
    return band

# data validation and limiting path parameters example
@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre: GenreURLChoice) -> list[dict]:
    return [
        b for b in BANDS if b['genre'].lower() == genre.value
    ]


@app.post('/bands')
def create_band(band_data: BandCreate) -> BandWithId:
    id = BANDS[-1]['id'] + 1
    band = BandWithId(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band
