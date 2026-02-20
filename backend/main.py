from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os
import uuid
import time
from typing import Optional
from fastapi.concurrency import run_in_threadpool
import pdf_utils

app = FastAPI(
    title="DoubleSide API",
    description="Backend API for DoubleSide - A tool for PDF manipulation and printing preparation.",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (Frontend)
if os.path.exists("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
    app.mount("/icon.svg", StaticFiles(directory="static", html=True), name="icon")

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


class ProcessRequest(BaseModel):
    filename: str
    original_filename: Optional[str] = None
    mode: str
    start_page: int = 1
    end_page: int = 0
    password: Optional[str] = None
    reverse_order: bool = True


def cleanup_old_files():
    """Deletes files in TEMP_DIR older than 10 minutes."""
    print("Starting cleanup check...")
    now = time.time()
    cutoff = 600

    if not os.path.exists(TEMP_DIR):
        return

    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        try:
            if os.path.isfile(file_path):
                age = now - os.path.getmtime(file_path)
                if age > cutoff:
                    os.remove(file_path)
                    print(f"Deleted old file: {filename}")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")


@app.on_event("startup")
async def startup_event():
    print("Running startup cleanup...")
    await run_in_threadpool(cleanup_old_files)


@app.post("/api/upload", tags=["File Operations"])
async def upload_file(file: UploadFile = File(...)):
    await run_in_threadpool(cleanup_old_files)

    file_id = str(uuid.uuid4())
    extension = os.path.splitext(file.filename)[1]

    if extension.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    stored_filename = f"{file_id}.pdf"
    file_path = os.path.join(TEMP_DIR, stored_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": stored_filename, "original_name": file.filename}


@app.post("/api/process", tags=["PDF Processing"])
async def process_pdf(request: ProcessRequest):
    file_path = os.path.join(TEMP_DIR, request.filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        # ✅ ALWAYS capture as tuple/list
        if request.mode == "double":
            outputs = await run_in_threadpool(
                pdf_utils.process_double,
                file_path,
                request.start_page,
                request.end_page,
                request.reverse_order,
            )

        elif request.mode == "four":
            outputs = await run_in_threadpool(
                pdf_utils.process_four,
                file_path,
                request.start_page,
                request.end_page,
                request.reverse_order,
            )

        elif request.mode == "book":
            outputs = await run_in_threadpool(
                pdf_utils.process_book,
                file_path,
                request.start_page,
                request.end_page,
                request.reverse_order,
            )

        elif request.mode == "split":
            out = await run_in_threadpool(
                pdf_utils.process_split,
                file_path,
                request.start_page,
                request.end_page,
            )
            outputs = (out,)

        elif request.mode == "decrypt":
            out = await run_in_threadpool(
                pdf_utils.decrypt_pdf,
                file_path,
                request.password or "",
            )
            outputs = (out,)

        elif request.mode == "encrypt":
            if not request.password:
                raise HTTPException(status_code=400, detail="Password required for encryption")

            out = await run_in_threadpool(
                pdf_utils.encrypt_pdf,
                file_path,
                request.password,
            )
            outputs = (out,)

        else:
            raise HTTPException(status_code=400, detail="Invalid mode")

        # ✅ normalize to list
        output_files = list(outputs)

        # ---------- build response ----------
        response_files = []
        base_name = (
            os.path.splitext(request.original_filename)[0]
            if request.original_filename
            else "output"
        )

        if len(output_files) == 2:
            files_info = [
                (output_files[0], f"{base_name}_1.pdf"),
                (output_files[1], f"{base_name}_2.pdf"),
            ]
        else:
            suffix = "_processed"
            if request.mode == "split":
                suffix = "_split"
            elif request.mode == "decrypt":
                suffix = "_decrypted"
            elif request.mode == "encrypt":
                suffix = "_encrypted"

            files_info = [(output_files[0], f"{base_name}{suffix}.pdf")]

        for real_path, friendly_name in files_info:
            real_filename = os.path.basename(real_path)
            url = f"/api/download/{real_filename}?download_name={friendly_name}"
            response_files.append({"url": url, "name": friendly_name})

        return {"files": response_files}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}", tags=["File Operations"])
async def download_file(filename: str, download_name: Optional[str] = None):
    file_path = os.path.join(TEMP_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=download_name)


# SPA Catch-all route
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")

    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")

    return {"message": "Frontend not built or static directory missing"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
