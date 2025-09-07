"""
Synthos Market Intelligence - Market analysis and competitive intelligence
"""

from typing import Dict, List, Any
from datetime import datetime

class MarketIntelligence:
    """Handles market analysis and competitive intelligence for Synthverse Labs"""
    
    def __init__(self):
        self.market_data = []
        self.competitors = []
        self.trends = []
        self.opportunities = []
    
    def add_competitor(self, name: str, description: str, strengths: List[str], weaknesses: List[str]):
        """Add competitor analysis"""
        competitor = {
            "name": name,
            "description": description,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "last_updated": datetime.now().isoformat()
        }
        self.competitors.append(competitor)
        return competitor
    
    def add_market_trend(self, trend: str, impact: str, timeframe: str):
        """Add market trend analysis"""
        trend_entry = {
            "trend": trend,
            "impact": impact,
            "timeframe": timeframe,
            "identified": datetime.now().isoformat()
        }
        self.trends.append(trend_entry)
        return trend_entry
    
    def identify_opportunity(self, opportunity: str, market_size: str, competition_level: str):
        """Identify new market opportunity"""
        opportunity_entry = {
            "opportunity": opportunity,
            "market_size": market_size,
            "competition_level": competition_level,
            "identified": datetime.now().isoformat(),
            "status": "evaluating"
        }
        self.opportunities.append(opportunity_entry)
        return opportunity_entry
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get market intelligence summary"""
        return {
            "total_competitors": len(self.competitors),
            "active_trends": len(self.trends),
            "opportunities_identified": len(self.opportunities),
            "recent_trends": self.trends[-3:] if self.trends else [],
            "top_opportunities": [o for o in self.opportunities if o["status"] == "evaluating"][:3]
        }
