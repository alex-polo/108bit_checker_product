from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

from .annotations import string_256


# Base: DeclarativeMeta = declarative_base()

class Base(DeclarativeBase):
    type_annotation_map = {
        string_256: String(256)
    }
