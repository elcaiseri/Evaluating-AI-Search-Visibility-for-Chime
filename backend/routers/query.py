from fastapi import APIRouter, HTTPException
from routers.models import QueryRequest, QueryResponse
from rag.survey import SurveyAnalysisRAGSystem
from utils.logging import get_logger
import uuid

router = APIRouter()

logger = get_logger(__name__)

# Load Excel file using pandas
logger.info("Initializing RAG system")
file_paths = 'data/processed/'
rag_system = SurveyAnalysisRAGSystem(file_paths)
logger.info("RAG system initialized successfully")

@router.post("/query", response_model=QueryResponse)
def query_api(request: QueryRequest):
    request_id = str(uuid.uuid4())
    logger.info(f"Request ID: {request_id}")
        
    query = request.query
    dataset = request.dataset
    logger.info(f"Received query: {query} for dataset: {dataset}")

    if not query:
        logger.error("Query cannot be empty")
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        top_k = 16 if dataset == "sustainability" else 6
        output = rag_system.generate_answer(query, dataset, top_k)
        logger.info(f"Generated answer: {output['result']} in {output['time_taken']:.2f} sec")
        return QueryResponse(answer=output['result'], time=output['time_taken'])
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
