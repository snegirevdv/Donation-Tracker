from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.services.crud import donation_crud


class InvestmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def invest(self, charity_project: CharityProject, donation: Donation) -> None:
        amount = min(charity_project.available_amount, donation.available_amount)
        donation.invested_amount += amount
        charity_project.invested_amount += amount

        if donation.available_amount == 0:
            donation.fully_invested = True
            donation.close_date = datetime.now()

        if charity_project.available_amount == 0:
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()

    async def invest_donations_to_project(
        self, charity_project: CharityProject
    ) -> bool:
        active_donations = await donation_crud.get_available_list(self.session)

        for donation in active_donations:
            async with self.session.begin():
                self.invest(charity_project, donation)

                if charity_project.fully_invested:
                    return True

        return False
