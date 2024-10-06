from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationRead
from app.services.crud import donation_crud

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
