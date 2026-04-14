from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image
from piet_interpreter import PietInterpreter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_piet(file: UploadFile = File(...), codel_size: int = Form(1)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    interpreter = PietInterpreter(image, codel_size)
    result = interpreter.execute()
    
    return {
        "status": "success",
        "output": result["output"],
        "trace": result["trace"],
        "error": result.get("error")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
