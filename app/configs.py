from pydantic import BaseSettings


class Settings(BaseSettings):

    app_name: str = 'Basic API'
    app_version: str = '0.0.2'
    app_description: str = 'Basic API - Basic Struct API'

    admin_email: str = 'admin@basic.api'
    items_per_user: int = 50

    api_v1_uri = '/api/v1'

    # access_token_expire_minutes = 60 * 24 * 7
    access_token_expire_minutes = 30
    jwt_secret_key = 'eAIozClf3otBH2Dp05tqWgiIqzGK_4tLTKFkP3Lz6zM'
    algorithm = 'HS256'

    database_url = 'postgresql+asyncpg://postgres:@localhost:5432/basic_api'

    # class Config:
    #     env_file = ".env"


Settings: BaseSettings = Settings()
