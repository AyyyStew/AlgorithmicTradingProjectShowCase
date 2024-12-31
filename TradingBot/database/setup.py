from .database import engine, get_session
from .models import Base
from .models import Order


def setup_db():
    Base.metadata.create_all(engine)
