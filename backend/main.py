from fastapi import FastAPI
from generator import generate_answer
import os
import uvicorn

print("Starting minimal FastAPI app...")

app = FastAPI()


@app.get("/")
def root():
    return {"status": "alive"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("Launching Uvicorn on port:", port)
    uvicorn.run(app, host="0.0.0.0", port=port)
