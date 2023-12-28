from fastapi import APIRouter, Depends

from src.social_network.schemas.countries import CountrySchema
from src.social_network.services.countries import CountriesService

router = APIRouter(
    prefix='/countries',
    tags=['countries'],
)


@router.get('', response_model=list[CountrySchema])
def get_countries(service: CountriesService = Depends()):
    return service.get_countries()
