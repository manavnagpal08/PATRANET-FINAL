# Unified corporate styling for PATRANET Document Processing Suite

CUSTOM_CSS_LOGGED_IN = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
        padding-top: 1.5rem;
    }
    
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        border-color: #cbd5e1;
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
    }
    
    .top-banner {
        background: #ffffff;
        color: #0f172a;
        padding: 1.75rem 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2563eb;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }
    
    .top-banner h1 {
        color: #0f172a !important;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .top-banner p {
        margin: 0.25rem 0 0 0;
        font-size: 0.95rem;
        color: #475569;
    }
    
    /* Clean Light Theme Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        color: #0f172a !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span {
        color: #0f172a !important;
    }
    
    .user-profile-card {
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .user-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #0f172a;
    }
    
    .user-role {
        font-size: 0.75rem;
        color: #475569;
    }
</style>
"""

CUSTOM_CSS_LOGGED_OUT = """
<style>
    /* Hide the entire sidebar when logged out */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    .login-container {
        max-width: 450px;
        margin: 5rem auto 1.5rem auto;
        padding: 2.5rem;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        color: #0f172a;
    }
    
    .login-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        font-size: 0.9rem;
        color: #475569;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
"""
