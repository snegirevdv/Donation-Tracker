from typing import TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BaseDonateModel, Project, Donation

ModelType = TypeVar('ModelType', bound=BaseDonateModel)


class InvestmentService:
    """Provides investment logic using SQL Alchemy queries."""

    async def _get_available_list(
        self,
        model: type[ModelType],
        session: AsyncSession,
    ) -> list[ModelType]:
        query = select(model).where(model.fully_invested == False)
        result = await session.scalars(query)
        return result.all()

    def _invest(self, project: Project, donation: Donation) -> None:
        amount = min(project.available_amount, donation.available_amount)
        donation.invested_amount += amount
        project.invested_amount += amount

        if donation.fully_invested:
            donation.close_date = func.now()

        if project.fully_invested:
            project.close_date = func.now()

    async def _invest_between_entities(
        self,
        source: ModelType,
        target_list: list[ModelType],
        session: AsyncSession,
    ) -> ModelType:
        for target_obj in target_list:
            self._invest(source, target_obj)

            if source.fully_invested:
                break

        session.add(source)
        await session.commit()
        await session.refresh(source)
        return source

    async def invest_donations_to_project(
        self,
        project: Project,
        session: AsyncSession,
    ) -> Project:
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
        active_projects = await self._get_available_list(Project, session)
        print(active_projects)
        return await self._invest_between_entities(donation, active_projects, session)


investment_service = InvestmentService()
