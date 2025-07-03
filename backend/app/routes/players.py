from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlmodel import Session, select
from ..db.session import get_session
from ..models.player import Player


router = APIRouter(prefix="/api/players", tags=["players"])

# Create player
@router.post("", response_model=Player)
def create_player(player: Player, session: Session = Depends(get_session)):
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

# Get all players
@router.get("", response_model=List[Player])
def get_players(session: Session = Depends(get_session)):
    players = session.exec(select(Player)).all()
    return players

# Get one player
@router.get("/{player_id}", response_model=Player)
def get_player(player_id: int = Path(...), session: Session = Depends(get_session)):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

# Update a player
@router.put("/{player_id}", response_model=Player)
def update_player(
    player_id: int = Path(...),
    updated: Player = Body(...),
    session: Session = Depends(get_session)
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player.first_name = updated.first_name
    player.last_name = updated.last_name
    player.height = updated.height
    player.position = updated.position
    player.image_url = updated.image_url
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

# Delete a player
@router.delete("/{player_id}")
def delete_player(player_id: int = Path(...), session: Session = Depends(get_session)):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    session.delete(player)
    session.commit()
    return {"ok": True}