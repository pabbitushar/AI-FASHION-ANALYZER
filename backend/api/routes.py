from fastapi import APIRouter, UploadFile, File, HTTPException
from services.analysis_service import AnalysisService
from utils.image_utils import validate_image, load_image
from models.schemas import AnalysisResponse, AnalysisResult
from config import settings
import traceback

router = APIRouter()
service = AnalysisService()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_endpoint(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
        
    file_bytes = await file.read()
    
    is_valid, msg = validate_image(file_bytes, file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
        
    try:
        image = load_image(file_bytes)
    except Exception:
        raise HTTPException(status_code=422, detail="We couldn't get a clear read of the outfit. Try a photo where one person is clearly visible and most of the outfit is in frame.")
        
    try:
        result = service.analyze_image(image)
        return AnalysisResponse(success=True, data=result, message="Analysis complete")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Server error during analysis.")
    finally:
        # If we had temp files we would clean them up here
        pass

@router.get("/health")
def health_check():
    return {"status": "ok", "demo_mode": settings.DEMO_MODE}

@router.get("/config")
def get_config():
    return {
        "demo_mode": settings.DEMO_MODE,
        "max_image_size": settings.MAX_IMAGE_SIZE,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS
    }
