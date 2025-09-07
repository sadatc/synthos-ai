"""
Synthos LinkedIn Setup Command - Interactive setup for complete control
"""

import os
import webbrowser
from typing import Dict, Any

class LinkedInSetupCommand:
    """Interactive LinkedIn setup with complete control"""
    
    def __init__(self):
        self.linkedin = None
    
    def start_setup(self) -> Dict[str, Any]:
        """Start the LinkedIn integration setup process"""
        from ..integrations.linkedin import LinkedInIntegration
        
        self.linkedin = LinkedInIntegration()
        
        return {
            "status": "setup_started",
            "message": "LinkedIn integration setup initiated",
            "next_steps": [
                "1. Create LinkedIn Developer Account at https://www.linkedin.com/developers/",
                "2. Create a new app and get Client ID and Client Secret",
                "3. Set redirect URI (e.g., http://localhost:8080/callback)",
                "4. Run: linkedin.setup_credentials(client_id, client_secret)",
                "5. Get authorization URL and complete OAuth flow"
            ],
            "setup_guide": self.linkedin.setup_complete_integration()
        }
    
    def setup_credentials(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        """Set up LinkedIn API credentials"""
        if not self.linkedin:
            self.linkedin = LinkedInIntegration()
        
        result = self.linkedin.setup_credentials(client_id, client_secret)
        
        # Generate authorization URL
        auth_url = self.linkedin.get_authorization_url("http://localhost:8080/callback")
        
        return {
            **result,
            "authorization_url": auth_url,
            "next_step": "Visit the authorization URL to get the authorization code",
            "instructions": [
                "1. Click the authorization URL below",
                "2. Log in to LinkedIn and authorize the app",
                "3. Copy the 'code' parameter from the redirect URL",
                "4. Run: linkedin.exchange_code_for_token(authorization_code, redirect_uri)"
            ]
        }
    
    def complete_oauth(self, authorization_code: str, redirect_uri: str = "http://localhost:8080/callback") -> Dict[str, Any]:
        """Complete the OAuth flow"""
        if not self.linkedin:
            return {"status": "error", "message": "LinkedIn not initialized. Run start_setup first."}
        
        result = self.linkedin.exchange_code_for_token(authorization_code, redirect_uri)
        
        if result['status'] == 'success':
            # Test the connection
            profile = self.linkedin.get_profile()
            
            return {
                **result,
                "profile_test": profile,
                "message": "LinkedIn integration complete! You now have full control.",
                "available_commands": [
                    "linkedin.get_profile() - Get your profile",
                    "linkedin.get_connections() - Get your connections", 
                    "linkedin.post_update(text) - Post an update",
                    "linkedin.analyze_network() - Analyze your network",
                    "linkedin.get_company_updates(company_id) - Get company updates"
                ]
            }
        else:
            return result
    
    def get_profile_info(self) -> Dict[str, Any]:
        """Get comprehensive profile information"""
        if not self.linkedin or not self.linkedin.access_token:
            return {"status": "error", "message": "LinkedIn not connected. Complete setup first."}
        
        profile = self.linkedin.get_profile()
        network_analysis = self.linkedin.analyze_network()
        
        return {
            "status": "success",
            "profile": profile,
            "network_analysis": network_analysis,
            "timestamp": str(datetime.now())
        }
    
    def post_synthverse_update(self, message: str) -> Dict[str, Any]:
        """Post an update about Synthverse Labs"""
        if not self.linkedin or not self.linkedin.access_token:
            return {"status": "error", "message": "LinkedIn not connected. Complete setup first."}
        
        # Add Synthverse branding
        branded_message = f"🚀 {message}\n\n#SynthverseLabs #AI #Innovation #Tech"
        
        return self.linkedin.post_update(branded_message)
    
    def get_business_insights(self) -> Dict[str, Any]:
        """Get business intelligence from LinkedIn network"""
        if not self.linkedin or not self.linkedin.access_token:
            return {"status": "error", "message": "LinkedIn not connected. Complete setup first."}
        
        analysis = self.linkedin.analyze_network()
        
        if analysis['status'] == 'success':
            insights = analysis['analysis']
            
            return {
                "status": "success",
                "business_insights": {
                    "network_size": insights['total_connections'],
                    "industry_presence": insights['top_industries'],
                    "company_connections": insights['top_companies'],
                    "professional_summary": insights['profile_summary'],
                    "recommendations": self._generate_recommendations(insights)
                }
            }
        else:
            return analysis
    
    def _generate_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate business recommendations based on network analysis"""
        recommendations = []
        
        if insights['total_connections'] < 100:
            recommendations.append("Consider expanding your network to reach 500+ connections for better business opportunities")
        
        if 'AI' not in str(insights['top_industries']):
            recommendations.append("Focus on connecting with AI/tech industry professionals to strengthen Synthverse Labs' network")
        
        if insights['total_connections'] > 200:
            recommendations.append("Leverage your strong network for Synthverse Labs partnerships and business development")
        
        return recommendations
