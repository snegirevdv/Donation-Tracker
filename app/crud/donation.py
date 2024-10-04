from app.crud.base import CRUDBase
from app.models import Donation


class CRUDCharityProject(CRUDBase):
    pass


donation_crud = CRUDCharityProject(model=Donation)
