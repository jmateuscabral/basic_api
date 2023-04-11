from pydantic import BaseSettings
from os import environ


class Settings(BaseSettings):

    app_name: str = 'Basic API'
    app_version: str = '0.0.2'
    app_description: str = 'Astro API - Controladoria-Geral do Estado do Piauí'

    admin_email: str = 'jmateus@sefaz.pi.gov.br'
    items_per_user: int = 50

    api_v1_uri = '/api/v1'

    # Uma Semana = Minutos * Horas * Dias
    access_token_expire_minutes = 60 * 24 * 7
    jwt_secret_key: str = environ.get('astro_jwt_secret_key')
    algorithm_jwt: str = environ.get('astro_algorithm_jwt')

    database_url: str = environ.get('astro_database_url')

    # class Config:
    #     env_file = ".env"


Settings: BaseSettings = Settings()
