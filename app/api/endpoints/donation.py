from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import donation_crud
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationRead, DonationUpdate

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=DonationRead,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: SessionDep,
) -> Donation:
    return await donation_crud.create(donation, session)


@router.get(
    '/',
    response_model=list[DonationRead],
    response_model_exclude_none=True,
)
async def get_all_donations(session: SessionDep) -> list[Donation]:
    return await donation_crud.get_list(session)


@router.patch(
    '/{donation_id}',
    response_model=DonationRead,
    response_model_exclude_none=True,
)
async def partially_update_donation(
    donation_id: int,
    obj_in: DonationUpdate,
    session: SessionDep,
) -> Donation:
    donation = await donation_crud.get(donation_id, session)
    return await donation_crud.update(donation, obj_in, session)


@router.delete(
    '/{donation_id}',
    response_model=DonationRead,
    response_model_exclude_none=True,
)
async def remove_charity_room(donation_id: int, session: SessionDep) -> None:
    donation = await donation_crud.get(donation_id, session)
    return await donation_crud.delete(donation, session)
