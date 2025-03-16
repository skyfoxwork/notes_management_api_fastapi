from fastapi import FastAPI


app = FastAPI(title="Notes Management API", description="Project description")


@app.get("/")
async def main():
    return {"message": "ok"}
