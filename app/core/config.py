from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "rm-xxx.mysql.rds.aliyuncs.com"
    DB_PORT: int = 3306
    DB_USER: str = "cal_user"
    DB_PASS: str = "StrongPass123!"
    DB_NAME: str = "calendar_db"
    JWT_SECRET: str = "your-secret-key"
    JWT_EXPIRE: int = 3600 * 24 * 7  # 7天
    
    @property
    def DB_URL(self):
        return f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()