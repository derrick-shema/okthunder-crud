import os
import shutil
from typing import List
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, Path, UploadFile
from sqlmodel import Session, select
from ..db.session import get_session
from ..models.player import Player


router = APIRouter(prefix="/api/players", tags=["players"])

# Create player
@router.post("", response_model=Player)
async def create_player(
    first_name: str = Form(...),
    last_name: str = Form(...),
    height: str = Form(...),
    position: str = Form(...),
    image: UploadFile = File(...), 
    session: Session = Depends(get_session)
):
    image_path = f"static/images/{image.filename}"
    full_path = f"app/{image_path}"
    with open(full_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    player = Player(
        first_name=first_name,
        last_name=last_name,
        height=height,
        position=position,
        image_url=f"/{image_path}"
    )
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


# Get all players
@router.get("", response_model=List[Player])
async def get_players(session: Session = Depends(get_session)):
    players = session.exec(select(Player)).all()
    return players

# Get one player
@router.get("/{player_id}", response_model=Player)
async def get_player(player_id: int = Path(...), session: Session = Depends(get_session)):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

# Update a player
@router.put("/{player_id}", response_model=Player)
async def update_player(
    player_id: int = Path(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    height: str = Form(...),
    position: str = Form(...),
    image: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # If a new image is uploaded, replace the old one
    if image:
        # Remove old image file if exists
        if player.image_url:
            old_image_path = f"app{player.image_url}"
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        # Save new image
        image_path = f"static/images/{image.filename}"
        full_path = f"app/{image_path}"
        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        player.image_url = f"/{image_path}"

    player.first_name = first_name
    player.last_name = last_name
    player.height = height
    player.position = position

    session.add(player)
    session.commit()
    session.refresh(player)
    return player

# Delete a player
@router.delete("/{player_id}")
async def delete_player(player_id: int = Path(...), session: Session = Depends(get_session)):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    # Remove image file
    if player.image_url:
        image_path = f"app{player.image_url}"
        if os.path.exists(image_path):
            os.remove(image_path)
    session.delete(player)
    session.commit()
    return {"ok": True}