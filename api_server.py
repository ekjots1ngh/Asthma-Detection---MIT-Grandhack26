"""
FastAPI backend for respiratory screening app.

Provides endpoints for audio analysis, wheeze detection, and risk assessment.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import logging
from typing import Dict
import json

from audio_analyzer import RespiratoryAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title='Respiratory Screening API',
    description='API for analyzing breathing audio and detecting asthma symptoms',
    version='1.0.0',
)

# Add CORS middleware for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Initialize analyzer
analyzer = RespiratoryAnalyzer(sr=22050)

# Guidance messages based on risk level
GUIDANCE_MESSAGES = {
    'low': {
        'title': 'Clear Breathing',
        'message': 'Clear breathing. Continue monitoring.',
        'recommendation': 'No immediate action needed. Continue regular check-ups.',
        'emoji': '✓',
    },
    'medium': {
        'title': 'Possible Wheezing',
        'message': 'Possible wheezing detected. Monitor symptoms.',
        'recommendation': 'Keep monitoring symptoms. Consider scheduling a healthcare provider consultation if symptoms persist.',
        'emoji': '⚠',
    },
    'high': {
        'title': 'Concerning Wheezing',
        'message': 'Concerning wheezing detected. Consider using rescue inhaler or seeking care.',
        'recommendation': 'Seek medical attention. Consider using rescue inhaler if available. Contact healthcare provider promptly.',
        'emoji': '⚠⚠',
    },
}


@app.get('/health')
async def health_check() -> Dict:
    """Health check endpoint for monitoring."""
    return {
        'status': 'healthy',
        'service': 'respiratory-screening-api',
        'version': '1.0.0',
    }


@app.post('/analyze-breathing')
async def analyze_breathing(file: UploadFile = File(...)) -> JSONResponse:
    """
    Analyze breathing audio for wheeze detection and risk assessment.

    Args:
        file: Audio file (WAV, MP3, or other audio format supported by librosa)

    Returns:
        JSON response with analysis results:
        {
            'wheeze_probability': float (0-1),
            'respiratory_rate': int (breaths/min),
            'risk_level': str ('low', 'medium', 'high'),
            'guidance': {
                'title': str,
                'message': str,
                'recommendation': str
            },
            'metrics': {
                'wheeze_intensity': float (0-1)
            }
        }

    Raises:
        HTTPException: If file is invalid or analysis fails
    """
    # Validate file
    if not file.filename:
        logger.warning('Upload attempted with no filename')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file provided',
        )

    # Validate file type
    allowed_extensions = {'.wav', '.mp3', '.flac', '.ogg', '.m4a'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        logger.warning(f'Invalid file type: {file_ext}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Invalid file type. Supported formats: {", ".join(allowed_extensions)}',
        )

    temp_file_path = None
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_ext,
            dir='/tmp'
        ) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        logger.info(f'Processing audio file: {file.filename}')

        # Analyze breathing
        results = analyzer.analyze(temp_file_path)

        # Get guidance message
        risk_level = results['risk_level']
        guidance = GUIDANCE_MESSAGES.get(risk_level, GUIDANCE_MESSAGES['low'])

        # Prepare response
        response_data = {
            'wheeze_probability': results['wheeze_probability'],
            'respiratory_rate': results['respiratory_rate'],
            'risk_level': results['risk_level'],
            'guidance': {
                'title': guidance['title'],
                'message': guidance['message'],
                'recommendation': guidance['recommendation'],
                'emoji': guidance['emoji'],
            },
            'metrics': {
                'wheeze_intensity': results['wheeze_intensity'],
            },
        }

        logger.info(
            f'Analysis complete: risk_level={risk_level}, '
            f'wheeze_prob={results["wheeze_probability"]:.2%}'
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response_data,
        )

    except ValueError as e:
        logger.error(f'Analysis error: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Failed to analyze audio: {str(e)}',
        )
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An unexpected error occurred during analysis',
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.debug(f'Cleaned up temp file: {temp_file_path}')
            except OSError as e:
                logger.warning(f'Failed to clean up temp file: {e}')


@app.post('/batch-analyze')
async def batch_analyze(files: list[UploadFile] = File(...)) -> JSONResponse:
    """
    Analyze multiple breathing audio files.

    Args:
        files: List of audio files to analyze

    Returns:
        JSON response with list of analysis results
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No files provided',
        )

    if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail='Maximum 10 files per request',
        )

    results = []
    for file in files:
        try:
            temp_file_path = None
            file_ext = os.path.splitext(file.filename)[1].lower()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_ext,
                dir='/tmp'
            ) as temp_file:
                temp_file_path = temp_file.name
                content = await file.read()
                temp_file.write(content)

            analysis = analyzer.analyze(temp_file_path)
            risk_level = analysis['risk_level']
            guidance = GUIDANCE_MESSAGES.get(risk_level, GUIDANCE_MESSAGES['low'])

            results.append({
                'filename': file.filename,
                'wheeze_probability': analysis['wheeze_probability'],
                'respiratory_rate': analysis['respiratory_rate'],
                'risk_level': analysis['risk_level'],
                'guidance': {
                    'title': guidance['title'],
                    'message': guidance['message'],
                },
            })

            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        except Exception as e:
            logger.error(f'Error processing {file.filename}: {str(e)}')
            results.append({
                'filename': file.filename,
                'error': str(e),
            })

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'results': results},
    )


@app.get('/info')
async def get_info() -> Dict:
    """Get information about the API and supported features."""
    return {
        'api_name': 'Respiratory Screening API',
        'version': '1.0.0',
        'description': 'Analyzes breathing audio for asthma screening',
        'endpoints': {
            'health_check': '/health',
            'analyze_single': '/analyze-breathing',
            'analyze_batch': '/batch-analyze',
            'info': '/info',
        },
        'supported_formats': ['.wav', '.mp3', '.flac', '.ogg', '.m4a'],
        'max_file_size_mb': 50,
        'max_batch_files': 10,
        'output_fields': {
            'wheeze_probability': 'float (0-1)',
            'respiratory_rate': 'int (breaths/min)',
            'risk_level': 'str (low/medium/high)',
            'guidance': 'dict with title, message, recommendation',
            'metrics': 'dict with wheeze_intensity',
        },
    }


@app.get('/risk-levels')
async def get_risk_levels() -> Dict:
    """Get information about risk levels and guidance."""
    return {
        'risk_levels': GUIDANCE_MESSAGES,
        'descriptions': {
            'low': 'Clear breathing detected - no immediate concerns',
            'medium': 'Possible wheezing detected - monitor and consider consultation',
            'high': 'Concerning wheezing detected - seek medical attention',
        },
    }


if __name__ == '__main__':
    import uvicorn

    # Run with: uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        log_level='info',
    )
