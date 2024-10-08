from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import Donation, User
from app.schemas.donation import DonationCreate, DonationRead
from app.services.crud import donation_crud
from app.services.investment import investment_service

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post('/', response_model=DonationRead)
async def create_new_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
) -> Donation:
    donation = await donation_crud.create(donation, session)
    return await investment_service.distribute_donation_among_projects(
        donation,
        session,
        user,
    )


@router.get(
    '/',
    response_model=list[DonationRead],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session: SessionDep) -> list[Donation]:
    return await donation_crud.get_list(session)


@router.get(
    '/me/donations',
    response_model=list[DonationRead],
    response_model_exclude={
        'invested_amount',
        'fully_invested',
        'close_date',
        'user_id',
    },
)
async def get_my_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
) -> list[Donation]:
    return await donation_crud.get_by_user(session=session, user=user)
