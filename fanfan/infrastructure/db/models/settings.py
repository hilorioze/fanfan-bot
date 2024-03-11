from sqlalchemy.orm import Mapped, mapped_column

from fanfan.application.dto.settings import SettingsDTO
from fanfan.infrastructure.db.models.base import Base


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True, server_default="1")
    voting_enabled: Mapped[bool] = mapped_column(server_default="False")
    announcement_timeout: Mapped[int] = mapped_column(server_default="10")
    announcement_timestamp: Mapped[float] = mapped_column(server_default="0")

    def to_dto(self) -> SettingsDTO:
        return SettingsDTO(
            voting_enabled=self.voting_enabled,
            announcement_timeout=self.announcement_timeout,
            announcement_timestamp=self.announcement_timestamp,
        )
