from setuptools import setup, find_packages

setup(
    name="giftpropaganda",
    version="1.0.0",
    description="Gift Propaganda News Bot",
    python_requires=">=3.11,<3.12",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.95.2",
        "uvicorn[standard]==0.22.0",
        "sqlalchemy==2.0.15",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "psycopg2-binary==2.9.6",
        "pydantic==1.10.8",
        "feedparser==6.0.10",
        "beautifulsoup4==4.12.2",
        "python-multipart==0.0.6",
    ],
) 