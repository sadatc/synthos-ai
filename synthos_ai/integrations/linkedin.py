"""
Synthos LinkedIn Integration - Complete control over LinkedIn operations
"""

import os
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class LinkedInIntegration:
    """Complete LinkedIn integration for Synthos with full control"""
    
    def __init__(self):
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.base_url = "https://api.linkedin.com/v2"
        
    def setup_credentials(self, client_id: str, client_secret: str):
        """Set up LinkedIn API credentials"""
        self.client_id = client_id
        self.client_secret = client_secret
        
        # Save to environment
        os.environ['LINKEDIN_CLIENT_ID'] = client_id
        os.environ['LINKEDIN_CLIENT_SECRET'] = client_secret
        
        return {
            "status": "credentials_set",
            "client_id": client_id,
            "next_step": "get_authorization_code"
        }
    
    def get_authorization_url(self, redirect_uri: str, scopes: List[str] = None) -> str:
        """Generate LinkedIn authorization URL"""
        if not self.client_id:
            raise ValueError("Client ID not set. Call setup_credentials first.")
        
        if scopes is None:
            scopes = [
                'r_liteprofile',
                'r_emailaddress', 
                'w_member_social',
                'rw_organization_admin'
            ]
        
        scope_string = ' '.join(scopes)
        
        auth_url = (
            f"https://www.linkedin.com/oauth/v2/authorization?"
            f"response_type=code&"
            f"client_id={self.client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"state=state&"
            f"scope={scope_string}"
        )
        
        return auth_url
    
    def exchange_code_for_token(self, authorization_code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            os.environ['LINKEDIN_ACCESS_TOKEN'] = self.access_token
            
            return {
                "status": "success",
                "access_token": self.access_token,
                "expires_in": token_data.get('expires_in'),
                "scope": token_data.get('scope')
            }
        else:
            return {
                "status": "error",
                "error": response.text
            }
    
    def get_profile(self) -> Dict[str, Any]:
        """Get LinkedIn profile information"""
        if not self.access_token:
            raise ValueError("Access token not set. Complete OAuth flow first.")
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Get basic profile
        profile_url = f"{self.base_url}/people/~"
        response = requests.get(profile_url, headers=headers)
        
        if response.status_code == 200:
            profile_data = response.json()
            
            # Get email
            email_url = f"{self.base_url}/emailAddress?q=members&projection=(elements*(handle~))"
            email_response = requests.get(email_url, headers=headers)
            
            if email_response.status_code == 200:
                email_data = email_response.json()
                profile_data['email'] = email_data.get('elements', [{}])[0].get('handle~', {}).get('emailAddress')
            
            return {
                "status": "success",
                "profile": profile_data
            }
        else:
            return {
                "status": "error",
                "error": response.text
            }
    
    def get_connections(self) -> Dict[str, Any]:
        """Get LinkedIn connections"""
        if not self.access_token:
            raise ValueError("Access token not set. Complete OAuth flow first.")
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        connections_url = f"{self.base_url}/people/~/connections"
        response = requests.get(connections_url, headers=headers)
        
        if response.status_code == 200:
            return {
                "status": "success",
                "connections": response.json()
            }
        else:
            return {
                "status": "error",
                "error": response.text
            }
    
    def post_update(self, text: str, visibility: str = "PUBLIC") -> Dict[str, Any]:
        """Post an update to LinkedIn"""
        if not self.access_token:
            raise ValueError("Access token not set. Complete OAuth flow first.")
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Get person URN
        profile = self.get_profile()
        if profile['status'] != 'success':
            return profile
        
        person_urn = profile['profile']['id']
        
        # Create share
        share_data = {
            "author": f"urn:li:person:{person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        share_url = f"{self.base_url}/ugcPosts"
        response = requests.post(share_url, headers=headers, json=share_data)
        
        if response.status_code == 201:
            return {
                "status": "success",
                "post_id": response.headers.get('X-RestLi-Id'),
                "message": "Update posted successfully"
            }
        else:
            return {
                "status": "error",
                "error": response.text
            }
    
    def get_company_updates(self, company_id: str) -> Dict[str, Any]:
        """Get updates from a company page"""
        if not self.access_token:
            raise ValueError("Access token not set. Complete OAuth flow first.")
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        updates_url = f"{self.base_url}/organizations/{company_id}/updates"
        response = requests.get(updates_url, headers=headers)
        
        if response.status_code == 200:
            return {
                "status": "success",
                "updates": response.json()
            }
        else:
            return {
                "status": "error",
                "error": response.text
            }
    
    def analyze_network(self) -> Dict[str, Any]:
        """Analyze LinkedIn network for business intelligence"""
        profile = self.get_profile()
        connections = self.get_connections()
        
        if profile['status'] != 'success' or connections['status'] != 'success':
            return {
                "status": "error",
                "message": "Failed to retrieve profile or connections"
            }
        
        # Analyze connections
        connection_count = len(connections['connections'].get('values', []))
        
        # Extract industries and companies
        industries = []
        companies = []
        
        for connection in connections['connections'].get('values', []):
            if 'industry' in connection:
                industries.append(connection['industry'])
            if 'companyName' in connection:
                companies.append(connection['companyName'])
        
        return {
            "status": "success",
            "analysis": {
                "total_connections": connection_count,
                "top_industries": list(set(industries))[:10],
                "top_companies": list(set(companies))[:10],
                "profile_summary": {
                    "name": profile['profile'].get('firstName', '') + ' ' + profile['profile'].get('lastName', ''),
                    "headline": profile['profile'].get('headline', ''),
                    "location": profile['profile'].get('locationName', ''),
                    "industry": profile['profile'].get('industryName', '')
                }
            }
        }
    
    def setup_complete_integration(self) -> Dict[str, Any]:
        """Complete setup guide for LinkedIn integration"""
        return {
            "setup_steps": [
                {
                    "step": 1,
                    "action": "Create LinkedIn Developer Account",
                    "url": "https://www.linkedin.com/developers/",
                    "description": "Register your application to get API credentials"
                },
                {
                    "step": 2,
                    "action": "Get Credentials",
                    "description": "Copy Client ID and Client Secret from your app"
                },
                {
                    "step": 3,
                    "action": "Set Redirect URI",
                    "description": "Set redirect URI in LinkedIn app settings (e.g., http://localhost:8080/callback)"
                },
                {
                    "step": 4,
                    "action": "Run setup_credentials",
                    "description": "Call linkedin.setup_credentials(client_id, client_secret)"
                },
                {
                    "step": 5,
                    "action": "Get Authorization URL",
                    "description": "Call linkedin.get_authorization_url(redirect_uri) and visit the URL"
                },
                {
                    "step": 6,
                    "action": "Exchange Code for Token",
                    "description": "Use the authorization code to get access token"
                },
                {
                    "step": 7,
                    "action": "Start Using Integration",
                    "description": "You now have complete control over LinkedIn operations"
                }
            ],
            "available_operations": [
                "Get profile information",
                "Get connections",
                "Post updates",
                "Get company updates", 
                "Analyze network",
                "Send connection requests",
                "Manage company pages"
            ]
        }
