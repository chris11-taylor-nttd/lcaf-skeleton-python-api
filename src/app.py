from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .routers.greetings import router as greetings_router
from .routers.people import router as people_router

app = FastAPI()

# A default wide-open CORS configuration. This should be restricted to only the
# origins that need access to the API.
origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", response_model=None, tags=["health"])
def healthcheck() -> Response:
    """Health check endpoint for monitoring server status. This example API
    always returns a 200 OK response.
    """
    return Response(status_code=200)


# Rather than mounting sub-APIs with their own OpenAPI docs route, we'll
# use routers to publish all our routes under a single API.
app.include_router(people_router)
app.include_router(greetings_router)

# Add OpenTelemetry instrumentation, excluding the health check endpoint
FastAPIInstrumentor.instrument_app(app, excluded_urls="healthz")
