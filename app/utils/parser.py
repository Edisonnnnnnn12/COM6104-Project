from dateutil import parser
import re

time_patterns = [
    (r"(?P<value>\d+)天后", lambda m: timedelta(days=int(m.group("value")))),
    (r"下(?P<weekday>[一二三四五六日])", handle_next_weekday),
    (r"(?P<hour>\d{1,2})点(?:(?P<minute>\d{1,2})分)?", handle_time)
]

def parse_datetime(text: str, base_date: datetime = None) -> datetime:
    base_date = base_date or datetime.now()
    
    # 先尝试标准库解析
    try:
        return parser.parse(text, fuzzy=True)
    except:
        pass
    
    # 自定义模式匹配
    for pattern, handler in time_patterns:
        match = re.search(pattern, text)
        if match:
            delta = handler(match, base_date)
            return base_date + delta
    
    raise ValueError("无法解析时间")

def handle_next_weekday(match, base_date):
    weekday_map = {"一":0, "二":1, "三":2, "四":3, "五":4, "六":5, "日":6}
    target_day = weekday_map[match.group("weekday")]
    days_ahead = (target_day - base_date.weekday() + 7) % 7
    return timedelta(days=days_ahead)