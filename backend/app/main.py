from fastapi import FastAPI

app = FastAPI()


@app.post("/ingest")
async def ingest(data: dict):
    return {"message": f"received data {data}"}
