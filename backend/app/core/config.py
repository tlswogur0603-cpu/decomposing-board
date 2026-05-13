# 공통 설정 관리 파일
# 환경변수를 읽어서 Python에서 쓰기 좋은 setting 객체로 만들어야 함.
# 현재 필요한 필수 설정값은 DATABASE_URL, DATABASE_URL은 str이고 없으면 서버 시작 실패
# Settings클래스를 만들고 DATABASE_URL 필드를 str로 정의 후 settings = Settings()로 객체화

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore"
    )

settings = Settings()