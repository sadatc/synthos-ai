#!/usr/bin/env python3
"""
Synthos LinkedIn Setup for Dr. Sadat Chowdhury
Principal Investigator, Synthverse Labs
"""

import os
import sys
import webbrowser
from synthos_ai.integrations.linkedin import LinkedInIntegration
from synthos_ai.commands.linkedin_setup import LinkedInSetupCommand

def main():
    print("🎯 Synthos LinkedIn Integration Setup")
    print("=" * 50)
    print("Setting up LinkedIn integration for:")
    print("👤 Dr. Sadat Chowdhury")
    print("🏢 Principal Investigator, Synthverse Labs")
    print("🔗 Profile: https://www.linkedin.com/in/sadatchowdhury/")
    print("=" * 50)
    
    # Initialize LinkedIn setup
    linkedin_setup = LinkedInSetupCommand()
    
    # Start setup process
    setup_info = linkedin_setup.start_setup()
    
    print("\n📋 Setup Steps:")
    for i, step in enumerate(setup_info['setup_guide']['setup_steps'], 1):
        print(f"{i}. {step['action']}")
        if 'url' in step:
            print(f"   🔗 {step['url']}")
        print(f"   📝 {step['description']}")
        print()
    
    # Get credentials from user
    print("🔑 LinkedIn API Credentials Setup")
    print("-" * 30)
    
    client_id = input("Enter your LinkedIn Client ID: ").strip()
    client_secret = input("Enter your LinkedIn Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Error: Both Client ID and Client Secret are required")
        return
    
    # Setup credentials
    print("\n⚙️ Setting up credentials...")
    cred_result = linkedin_setup.setup_credentials(client_id, client_secret)
    
    if cred_result['status'] == 'credentials_set':
        print("✅ Credentials set successfully!")
        
        # Get authorization URL
        auth_url = cred_result['authorization_url']
        print(f"\n🔗 Authorization URL:")
        print(auth_url)
        
        # Ask if user wants to open browser
        open_browser = input("\n🌐 Open authorization URL in browser? (y/n): ").strip().lower()
        if open_browser == 'y':
            webbrowser.open(auth_url)
            print("✅ Browser opened with authorization URL")
        
        print("\n📝 Next Steps:")
        print("1. Log in to LinkedIn and authorize the app")
        print("2. Copy the 'code' parameter from the redirect URL")
        print("3. Paste it below to complete the setup")
        
        # Get authorization code
        auth_code = input("\n🔐 Enter the authorization code: ").strip()
        
        if auth_code:
            print("\n🔄 Completing OAuth flow...")
            oauth_result = linkedin_setup.complete_oauth(auth_code)
            
            if oauth_result['status'] == 'success':
                print("🎉 LinkedIn integration complete!")
                print("\n📊 Your Profile Information:")
                if 'profile_test' in oauth_result and oauth_result['profile_test']['status'] == 'success':
                    profile = oauth_result['profile_test']['profile']
                    print(f"👤 Name: {profile.get('firstName', '')} {profile.get('lastName', '')}")
                    print(f"💼 Headline: {profile.get('headline', '')}")
                    print(f"🏢 Industry: {profile.get('industryName', '')}")
                    print(f"📍 Location: {profile.get('locationName', '')}")
                
                print("\n🚀 Available Commands:")
                for cmd in oauth_result['available_commands']:
                    print(f"   • {cmd}")
                
                # Get business insights
                print("\n📈 Getting business insights...")
                insights = linkedin_setup.get_business_insights()
                
                if insights['status'] == 'success':
                    bi = insights['business_insights']
                    print(f"🔗 Network Size: {bi['network_size']} connections")
                    print(f"🏭 Top Industries: {', '.join(bi['industry_presence'][:5])}")
                    print(f"🏢 Top Companies: {', '.join(bi['company_connections'][:5])}")
                    
                    print("\n💡 Recommendations:")
                    for rec in bi['recommendations']:
                        print(f"   • {rec}")
                
                print("\n✅ LinkedIn integration is now ready for Synthverse Labs operations!")
                
            else:
                print(f"❌ OAuth failed: {oauth_result.get('error', 'Unknown error')}")
        else:
            print("❌ No authorization code provided")
    else:
        print(f"❌ Credential setup failed: {cred_result}")

if __name__ == "__main__":
    main()
