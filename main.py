import logging
import uvicorn
from fastapi import FastAPI
from src.currency.handlers import router


app = FastAPI(title='DeribitAPI-service')

app.include_router(router, prefix='/currency', tags=['currency'])


if __name__ == '__main__':
    logging.basicConfig(
        level='INFO'.upper(),
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    uvicorn.run(app, host='127.0.0.1', port=8000)

