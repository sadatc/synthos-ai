"""
Synthos Communications - Report generation and communication management
"""

from typing import Dict, List, Any
from datetime import datetime

class ReportGenerator:
    """Generates reports and manages communications for Synthverse Labs"""
    
    def __init__(self):
        self.reports = []
        self.communications = []
    
    def generate_status_report(self, operations_data: Dict, market_data: Dict, roadmap_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        report = {
            "report_id": len(self.reports) + 1,
            "type": "status_report",
            "generated": datetime.now().isoformat(),
            "summary": {
                "operations": operations_data,
                "market_intelligence": market_data,
                "strategic_roadmap": roadmap_data
            },
            "key_insights": self._extract_insights(operations_data, market_data, roadmap_data),
            "recommendations": self._generate_recommendations(operations_data, market_data, roadmap_data)
        }
        self.reports.append(report)
        return report
    
    def _extract_insights(self, ops: Dict, market: Dict, roadmap: Dict) -> List[str]:
        """Extract key insights from data"""
        insights = []
        
        if ops.get("pending_tasks", 0) > 10:
            insights.append("High task volume - consider resource allocation review")
        
        if market.get("opportunities_identified", 0) > 5:
            insights.append("Multiple market opportunities identified - prioritize evaluation")
        
        if roadmap.get("upcoming_milestones"):
            insights.append(f"{len(roadmap['upcoming_milestones'])} milestones approaching")
        
        return insights
    
    def _generate_recommendations(self, ops: Dict, market: Dict, roadmap: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if ops.get("pending_tasks", 0) > 10:
            recommendations.append("Implement task prioritization system")
        
        if market.get("opportunities_identified", 0) > 0:
            recommendations.append("Schedule opportunity evaluation meetings")
        
        if roadmap.get("high_priority_goals"):
            recommendations.append("Focus resources on high-priority strategic goals")
        
        return recommendations
    
    def log_communication(self, recipient: str, subject: str, type: str, content: str):
        """Log communication"""
        comm = {
            "id": len(self.communications) + 1,
            "recipient": recipient,
            "subject": subject,
            "type": type,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.communications.append(comm)
        return comm
    
    def get_communications_summary(self) -> Dict[str, Any]:
        """Get communications summary"""
        return {
            "total_reports": len(self.reports),
            "total_communications": len(self.communications),
            "recent_reports": self.reports[-3:] if self.reports else [],
            "recent_communications": self.communications[-5:] if self.communications else []
        }
