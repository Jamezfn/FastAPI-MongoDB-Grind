from fastapi import FastAPI

from routes.user import router

app = FastAPI(
    title="Student Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)

app.include_router(router)

@app.get("/heath")
def health():
    return {"status": "FastAPI Running..."}
