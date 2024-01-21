import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from fanfan.application.dto.achievement import AchievementDTO, FullAchievementDTO
from fanfan.infrastructure.db.models.base import Base

if typing.TYPE_CHECKING:
    from fanfan.infrastructure.db.models import ReceivedAchievement


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

    user_received: Mapped["ReceivedAchievement"] = relationship(
        lazy="noload", viewonly=True
    )

    def to_dto(self) -> AchievementDTO:
        return AchievementDTO.model_validate(self)

    def to_full_dto(self) -> FullAchievementDTO:
        return FullAchievementDTO.model_validate(self)

    def __str__(self):
        return self.title
