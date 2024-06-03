from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import numpy as np

from spaceship.config import Settings
from spaceship.routers import api, health


def make_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
    )
    app.state.settings = settings

    if settings.debug:
        app.mount('/static', StaticFiles(directory='build'), name='static')

    app.include_router(api.router, prefix='/api', tags=['api'])
    app.include_router(health.router, prefix='/health', tags=['health'])

    @app.get('/', include_in_schema=False, response_class=FileResponse)
    async def root() -> str:
        return 'build/index.html'
    
    @app.get('/m', tags=['matrix'])
    async def multiply_matrices():
        # Generate two random 10x10 matrices
        matrix_a = np.random.randint(1, 10, size=(10, 10))
        matrix_b = np.random.randint(1, 10, size=(10, 10))

        # Multiply the matrices
        product = np.dot(matrix_a, matrix_b)

        # Convert numpy arrays to lists for JSON serialization
        matrix_a_list = matrix_a.tolist()
        matrix_b_list = matrix_b.tolist()
        product_list = product.tolist()

        return {
            "matrix_a": matrix_a_list,
            "matrix_b": matrix_b_list,
            "product": product_list,
        }


    return app
