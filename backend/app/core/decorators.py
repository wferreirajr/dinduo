from fastapi import APIRouter
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse

def add_options_method(router: APIRouter):
    def decorator(cls):
        original_routes = router.routes
        router.routes = []
        for route in original_routes:
            if isinstance(route, APIRoute):
                router.add_api_route(
                    route.path,
                    route.endpoint,
                    methods=route.methods,
                    **route.kwargs
                )
                router.add_api_route(
                    route.path,
                    lambda: JSONResponse(
                        content={"message": "OK"},
                        headers={
                            "Access-Control-Allow-Origin": "http://localhost:3000",
                            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                            "Access-Control-Allow-Headers": "Content-Type, Authorization",
                        },
                    ),
                    methods=["OPTIONS"],
                )
            else:
                router.routes.append(route)
        return cls
    return decorator
