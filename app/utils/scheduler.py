class CalendarViewType(str, Enum):
    day = "day"
    week = "week"
    month = "month"

@router.get("/view/{view_type}")
async def get_calendar_view(
    view_type: CalendarViewType,
    date: datetime = Query(default=datetime.now()),
    user: User = Depends(get_current_user)
):
    start_time, end_time = calculate_time_range(view_type, date)
    
    query = select(Event).where(
        and_(
            Event.user_id == user.id,
            Event.start_time >= start_time,
            Event.end_time <= end_time,
            Event.is_deleted == False
        )
    ).order_by(Event.start_time)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(query)
        return result.scalars().all()

def calculate_time_range(view_type: CalendarViewType, date: datetime):
    if view_type == CalendarViewType.day:
        start = date.replace(hour=0, minute=0, second=0)
        end = start + timedelta(days=1)
    elif view_type == CalendarViewType.week:
        start = date - timedelta(days=date.weekday())
        end = start + timedelta(weeks=1)
    else:  # month
        start = date.replace(day=1, hour=0, minute=0, second=0)
        if date.month == 12:
            end = date.replace(year=date.year+1, month=1, day=1)
        else:
            end = date.replace(month=date.month+1, day=1)
    return start, end