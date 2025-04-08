from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/events", tags=["events"])

@router.post("", response_model=EventResponse)
async def create_event(
    event: EventCreate, 
    user: User = Depends(get_current_user)
):
    # 冲突检测
    conflict_query = select(Event).where(
        and_(
            Event.user_id == user.id,
            Event.is_deleted == False,
            or_(
                and_(Event.start_time <= event.start_time, Event.end_time > event.start_time),
                and_(Event.start_time < event.end_time, Event.end_time >= event.end_time),
                and_(event.start_time <= Event.start_time, event.end_time >= Event.end_time)
            )
        )
    )
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(conflict_query)
        if result.scalars().first():
            raise HTTPException(status_code=409, detail="时间冲突")
        
        db_event = Event(**event.dict(), user_id=user.id)
        session.add(db_event)
        await session.commit()
        await session.refresh(db_event)
        return db_event