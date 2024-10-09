from fastapi import APIRouter, status

from app.api import dependencies
from app.models import Donation
from app.schemas.donation import BaseDonationRead, DonationCreate, ExtendedDonationRead
from app.services import donation_crud, investment_service

router = APIRouter()


@router.post('/', response_model=BaseDonationRead, status_code=status.HTTP_201_CREATED)
async def create_new_donation(
    donation: DonationCreate,
    session: dependencies.Session,
    user: dependencies.CurrentUser,
) -> Donation:
    donation = await donation_crud.create(donation, session, user)
    return await investment_service.distribute_donation_among_projects(
        donation,
        session,
    )


@router.get(
    '/',
    response_model=list[ExtendedDonationRead],
    dependencies=[dependencies.current_superuser],
)
async def get_all_donations(session: dependencies.Session) -> list[Donation]:
    return await donation_crud.get_list(session)


@router.get('/my', response_model=list[BaseDonationRead])
async def get_my_donations(
    session: dependencies.Session,
    user: dependencies.CurrentUser,
) -> list[Donation]:
    return await donation_crud.get_by_user(session=session, user=user)
