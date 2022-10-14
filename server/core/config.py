from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base application settings.
    Provides environmental constants throughout the application

    Args:
        BaseSettings (pydantic.BaseSettings): BaseSettings super
        class by pydantic
    """

    METHODS_ONE: list[str]
    ICD_ONE: str

    METHODS_TWO: list[str]
    CONTRACT_TWO: str

    HOST: str
    PORT: int
    THREADS: int
    BYTES_SIZE: int

    DROPZONE: str

    class Config:
        """Configuration file which imports environment variables"""

        case_sensitive = True
        env_file = ".env"


settings = Settings()
