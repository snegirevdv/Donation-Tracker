from datetime import datetime
from typing import TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BaseDonateModel, CharityProject, Donation

ModelType = TypeVar('ModelType', bound=BaseDonateModel)


class InvestmentService:
    async def _get_available_list(
        self,
        entity: ModelType,
        session: AsyncSession,
    ) -> list[ModelType]:
        query = select(entity).where(entity.fully_invested is False)
        result = await session.scalars(query)
        return result.all()

    def _invest(self, project: CharityProject, donation: Donation) -> None:
        amount = min(project.available_amount, donation.available_amount)
        donation.invested_amount += amount
        project.invested_amount += amount

        if donation.available_amount == 0:
            donation.fully_invested = True
            donation.close_date = func.now()

        if project.available_amount == 0:
            project.fully_invested = True
            project.close_date = func.now()

    async def _invest_between_entities(
        self,
        source: ModelType,
        target_list: list[ModelType],
        session: AsyncSession,
    ) -> ModelType:
        async with session.begin():
            for target_obj in target_list:
                self._invest(source, target_obj)

                if source.fully_invested:
                    break

            await session.refresh(source)
            await session.commit()

        return source

    async def invest_donations_to_project(
        self,
        project: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        available_donations = await self._get_available_list(Donation, session)
        return await self._invest_between_entities(
            project,
            available_donations,
            session,
        )

    async def distribute_donation_among_projects(
        self,
        donation: Donation,
        session: AsyncSession,
    ) -> Donation:
        active_projects = await self._get_available_list(CharityProject, session)
        return await self._invest_between_entities(donation, active_projects, session)


investment_service = InvestmentService()
