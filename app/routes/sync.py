class SyncRequest(BaseModel):
    last_sync: datetime
    device_id: str
    events: List[EventSync]

class SyncResponse(BaseModel):
    server_time: datetime
    changes: List[EventSync]
    conflicts: List[ConflictItem]

@router.post("/sync")
async def handle_sync(sync_data: SyncRequest, user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:
        # 获取服务器端变更
        server_changes = await session.execute(
            select(Event).where(
                Event.user_id == user.id,
                Event.updated_at > sync_data.last_sync
            )
        )
        
        # 处理客户端变更
        client_changes = []
        for event in sync_data.events:
            db_event = await session.get(Event, event.id)
            if not db_event:
                # 新建事件
                new_event = Event(**event.dict(), user_id=user.id)
                session.add(new_event)
                client_changes.append(new_event)
            elif db_event.updated_at < event.updated_at:
                # 更新事件
                for key, value in event.dict().items():
                    setattr(db_event, key, value)
                client_changes.append(db_event)
        
        await session.commit()
        return SyncResponse(
            server_time=datetime.utcnow(),
            changes=client_changes,
            conflicts=detect_conflicts(server_changes, client_changes)
        )