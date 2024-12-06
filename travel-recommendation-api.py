from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import boto3
import json
import uvicorn

app = FastAPI()

class TravelRequest(BaseModel):
    travel_style: str = Field(default="default", description="여행 스타일")
    destination: str = Field(default="default destination", description="목적지")
    duration: int = Field(default=1, ge=1, le=30, description="여행 기간")
    min_budget: int = Field(default=0, ge=0, description="최소 예산")
    max_budget: int = Field(default=1000, ge=0, description="최대 예산")

@app.get("/")
def read_root():
    return {"message": "여행 추천 서비스 API에 오신 것을 환영합니다. /docs에서 API 문서를 확인하세요."}

def call_claude_sonnet(prompt: str):
    try:
        client = boto3.client('bedrock-runtime', region_name="us-west-2")
        
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        body = json.dumps(request_body)
        
        response = client.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0", 
            body=body,
            contentType="application/json"
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 호출 실패: {str(e)}")

@app.post("/recommend-travel")
def recommend_travel(request: TravelRequest):
    return {
        "message": "추천된 여행 플랜입니다.",
        "travel_plan": {
            "style": request.travel_style,
            "destination": request.destination,
            "duration": request.duration,
            "budget_range": f"{request.min_budget} - {request.max_budget}"
        }
    }

@app.post("/recommend-travel-ai")
def recommend_travel_ai(request: TravelRequest):
    prompt = (
        f"사용자의 여행 스타일: {request.travel_style}, "
        f"희망 지역: {request.destination}, "
        f"여행 기간: {request.duration}일, "
        f"예산 범위: {request.min_budget}-{request.max_budget}.\n"
        "위 조건에 맞는 구체적이고 매력적인 여행 일정을 상세히 추천해 주세요."
    )
    
    try:
        ai_response = call_claude_sonnet(prompt)
        return {"ai_recommendation": ai_response}
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
