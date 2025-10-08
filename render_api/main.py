@"
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title='Civic Funding Intelligence API',
    description='Real-time civic funding analytics platform with authentication',
    version='2.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Data Models
class Initiative(BaseModel):
    name: str
    budget: int
    region: str
    impact: int
    status: str

class AnalyticsResponse(BaseModel):
    total_funding: int
    initiatives_count: int
    average_impact: float
    regions_served: int

class UserLogin(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: dict

# Mock user database (replace with Supabase Auth in production)
MOCK_USERS = {
    'admin@civicfunding.org': {
        'password': 'demo123',
        'name': 'Administrator',
        'role': 'admin'
    }
}

@app.get('/')
async def root():
    return {
        'message': 'Civic Funding Intelligence API v2.0',
        'status': 'active',
        'authentication': 'ready',
        'endpoints': ['/api/initiatives', '/api/analytics', '/auth/login']
    }

@app.post('/auth/login', response_model=AuthResponse)
async def login(user: UserLogin):
    # Mock authentication - replace with Supabase Auth
    if user.email in MOCK_USERS and user.password == MOCK_USERS[user.email]['password']:
        return AuthResponse(
            access_token='mock_jwt_token_here',
            user={
                'email': user.email,
                'name': MOCK_USERS[user.email]['name'],
                'role': MOCK_USERS[user.email]['role']
            }
        )
    raise HTTPException(status_code=401, detail='Invalid credentials')

@app.get('/api/initiatives', response_model=List[Initiative])
async def get_initiatives():
    initiatives = [
        {'name': 'Urban Renewal Program', 'budget': 1500000, 'region': 'Metropolitan', 'impact': 92, 'status': 'Active'},
        {'name': 'Rural Education Initiative', 'budget': 800000, 'region': 'Rural', 'impact': 88, 'status': 'Planning'},
        {'name': 'Healthcare Access Project', 'budget': 1200000, 'region': 'Suburban', 'impact': 95, 'status': 'Active'},
        {'name': 'Infrastructure Development', 'budget': 2000000, 'region': 'Metropolitan', 'impact': 90, 'status': 'Completed'}
    ]
    return initiatives

@app.get('/api/analytics', response_model=AnalyticsResponse)
async def get_analytics():
    initiatives = await get_initiatives()
    total_funding = sum(i['budget'] for i in initiatives)
    avg_impact = sum(i['impact'] for i in initiatives) / len(initiatives)
    regions = len(set(i['region'] for i in initiatives))
    
    return {
        'total_funding': total_funding,
        'initiatives_count': len(initiatives),
        'average_impact': round(avg_impact, 1),
        'regions_served': regions
    }

@app.get('/health')
async def health_check():
    return {
        'status': 'healthy',
        'version': '2.0.0',
        'services': ['api', 'authentication', 'database']
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
"@ | Out-File -FilePath "civic-funding_api/main.py" -Encoding utf8