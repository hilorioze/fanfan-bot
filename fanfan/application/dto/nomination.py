from typing import Optional

from pydantic import BaseModel, ConfigDict

from fanfan.application.dto.vote import VoteDTO


class NominationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    votable: bool


class VotingNominationDTO(NominationDTO):
    user_vote: Optional[VoteDTO]
