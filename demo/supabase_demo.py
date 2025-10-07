import os
from supabase import create_client, Client
import json

def demo_supabase_integration():
    """Quick demo showing Supabase integration for civic funding"""
    print("🚀 Civic Funding Intelligence Platform - Supabase Demo")
    print("=" * 50)
    
    # Mock data - Civic funding initiatives
    initiatives_data = [
        {"name": "Urban Renewal Program", "budget": 1500000, "status": "active", "region": "metropolitan", "impact_score": 92},
        {"name": "Rural Education Initiative", "budget": 800000, "status": "planning", "region": "rural", "impact_score": 88},
        {"name": "Healthcare Access Project", "budget": 1200000, "status": "active", "region": "suburban", "impact_score": 95},
        {"name": "Infrastructure Development", "budget": 2000000, "status": "completed", "region": "metropolitan", "impact_score": 90}
    ]
    
    print("📊 Civic Funding Initiatives:")
    print("-" * 40)
    for initiative in initiatives_data:
        print(f"  • {initiative['name']}")
        print(f"    Budget: ${initiative['budget']:,} | Region: {initiative['region'].title()}")
        print(f"    Status: {initiative['status'].title()} | Impact Score: {initiative['impact_score']}/100")
        print()
    
    # Analytics summary
    total_funding = sum(i["budget"] for i in initiatives_data)
    avg_impact = sum(i["impact_score"] for i in initiatives_data) / len(initiatives_data)
    
    print("📈 Funding Analytics Summary:")
    print("-" * 30)
    print(f"  Total Funding: ${total_funding:,}")
    print(f"  Initiatives: {len(initiatives_data)}")
    print(f"  Average Impact Score: {avg_impact:.1f}/100")
    print(f"  Regions Served: {len(set(i['region'] for i in initiatives_data))}")
    
    return {
        "platform": "Civic Funding Intelligence",
        "total_funding": total_funding,
        "initiatives_count": len(initiatives_data),
        "average_impact": avg_impact,
        "tech_stack": ["Supabase", "FastAPI", "React", "PostgreSQL"]
    }

if __name__ == "__main__":
    print("🔧 Setting up civic funding demo...\n")
    result = demo_supabase_integration()
    print(f"\n✅ Demo ready! {result['platform']}")
    print(f"🛠 Tech Stack: {', '.join(result['tech_stack'])}")