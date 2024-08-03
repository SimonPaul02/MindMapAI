from fastapi.staticfiles import StaticFiles
from fastapi import Response
from starlette.exceptions import HTTPException
import logging

logger = logging.getLogger("app")


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            response = await super().get_response(path, scope)
            logger.info(response)
            if response.status_code == 404:
                response = await super().get_response(".", scope)
        except HTTPException as e:
            if e.status_code == 404:
                response = await super().get_response(".", scope)
            else:
                raise e
        return response

    def file_response(self, *args, **kwargs) -> Response:
        resp: Response = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cross-Origin-Embedder-Policy", "require-corp")
        resp.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        resp.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        resp.headers.setdefault("Permissions-Policy", "interest-cohort=()")
        return resp
