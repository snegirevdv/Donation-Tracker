"""
Module imports the base elements for the database models in the application.
These imports are required for the proper initialization and registration of db models.
"""

from app.core.db import Base  # noqa: F401
from app.models import Donation, Project, User  # noqa: F401
