#!/usr/bin/env python
"""
Enrich unified CSV with categorization and filtering columns
- Adds 40+ new columns for advanced filtering and analysis
- Categorizes templates by type, industry, complexity, and features
- Calculates popularity metrics and business value indicators
"""
import csv
import json
import re
from datetime import datetime
from collections import Counter
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)


# ============================================================================
# KEYWORD MAPPINGS AND PATTERNS
# ============================================================================

AI_KEYWORDS = [
    'openai', 'chatgpt', 'gpt-3', 'gpt-4', 'claude', 'anthropic',
    'gemini', 'ai agent', 'llm', 'language model', 'chat model',
    'completion', 'palm', 'bard', 'ai', 'artificial intelligence'
]

CODE_KEYWORDS = ['code', 'javascript', 'python', 'function', 'script']

HTTP_KEYWORDS = ['http request', 'api call', 'rest api', 'webhook']

SPREADSHEET_APPS = ['google sheets', 'sheets', 'excel', 'airtable', 'spreadsheet']

EMAIL_APPS = ['gmail', 'email', 'outlook', 'mailchimp', 'sendgrid', 'mailgun']

STORAGE_APPS = ['google drive', 'drive', 'dropbox', 'onedrive', 'box', 'storage']

COMMUNICATION_APPS = ['slack', 'telegram', 'discord', 'teams', 'microsoft teams', 'whatsapp', 'messenger']

CRM_APPS = ['salesforce', 'hubspot', 'pipedrive', 'crm', 'zoho crm']

SOCIAL_MEDIA_APPS = ['facebook', 'instagram', 'linkedin', 'twitter', 'tiktok', 'youtube', 'pinterest', 'social']

ECOMMERCE_APPS = ['shopify', 'woocommerce', 'stripe', 'paypal', 'square', 'ecommerce']

PROJECT_MGMT_APPS = ['trello', 'asana', 'jira', 'notion', 'clickup', 'monday', 'project']

FORMS_APPS = ['typeform', 'google forms', 'forms', 'jotform', 'survey']


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def contains_any(text, keywords):
    """Check if text contains any of the keywords (case-insensitive)"""
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)


def count_apps(apps_used_str):
    """Count number of apps from apps_used string"""
    if not apps_used_str:
        return 0
    # Split by comma or semicolon
    apps = [a.strip() for a in apps_used_str.replace(';', ',').split(',') if a.strip()]
    return len(apps)


def calculate_percentile(values, target_value):
    """Calculate percentile of target value in list of values"""
    if not values or target_value is None:
        return None
    values_sorted = sorted([v for v in values if v is not None])
    if not values_sorted:
        return None
    try:
        target = float(target_value)
        smaller_count = sum(1 for v in values_sorted if float(v) <= target)
        return (smaller_count / len(values_sorted)) * 100
    except:
        return None


# ============================================================================
# CATEGORIZATION FUNCTIONS
# ============================================================================

def determine_automation_type(row):
    """Determine primary automation type"""
    apps = row.get('apps_used', '').lower()
    desc = row.get('description', '').lower()
    name = row.get('name', '').lower()
    combined = f"{apps} {desc} {name}"

    # Check for AI
    if contains_any(combined, AI_KEYWORDS):
        return 'AI_AUTOMATION'

    # Check for marketing
    if contains_any(combined, ['marketing', 'campaign', 'ads', 'lead']) or \
       contains_any(apps, SOCIAL_MEDIA_APPS):
        return 'MARKETING'

    # Check for communication
    if contains_any(apps, COMMUNICATION_APPS) or contains_any(combined, ['message', 'chat', 'notification']):
        return 'COMMUNICATION'

    # Check for e-commerce
    if contains_any(apps, ECOMMERCE_APPS) or contains_any(combined, ['order', 'product', 'shop', 'payment']):
        return 'ECOMMERCE'

    # Check for data sync
    if 'sync' in combined or 'backup' in combined or 'export' in combined or 'import' in combined:
        return 'DATA_SYNC'

    # Check for productivity
    if contains_any(apps, PROJECT_MGMT_APPS) or contains_any(combined, ['task', 'project', 'calendar', 'schedule']):
        return 'PRODUCTIVITY'

    # Check for HR
    if contains_any(combined, ['hr', 'hiring', 'recruitment', 'employee', 'applicant']):
        return 'HR'

    # Check for customer support
    if contains_any(combined, ['support', 'ticket', 'helpdesk', 'customer service']):
        return 'CUSTOMER_SUPPORT'

    # Check for analytics
    if contains_any(combined, ['analytics', 'report', 'dashboard', 'metrics']):
        return 'ANALYTICS'

    # Check for development
    if contains_any(combined, CODE_KEYWORDS) or contains_any(combined, HTTP_KEYWORDS):
        return 'DEVELOPMENT'

    # Default
    return 'INTEGRATION'


def determine_automation_subtype(row, automation_type):
    """Determine secondary automation category"""
    apps = row.get('apps_used', '').lower()
    desc = row.get('description', '').lower()
    name = row.get('name', '').lower()
    combined = f"{apps} {desc} {name}"

    if automation_type == 'AI_AUTOMATION':
        if 'chatbot' in combined or 'chat' in combined:
            return 'CHATBOT'
        elif 'content' in combined or 'generation' in combined or 'writing' in combined:
            return 'CONTENT_GENERATION'
        elif 'summary' in combined or 'summarize' in combined:
            return 'SUMMARIZATION'
        elif 'classification' in combined or 'categoriz' in combined:
            return 'CLASSIFICATION'
        elif 'extraction' in combined or 'extract' in combined:
            return 'EXTRACTION'
        else:
            return 'AI_PROCESSING'

    elif automation_type == 'MARKETING':
        if 'lead' in combined:
            return 'LEAD_CAPTURE'
        elif 'email' in combined:
            return 'EMAIL_AUTOMATION'
        elif 'social' in combined or 'post' in combined:
            return 'SOCIAL_POSTING'
        elif 'campaign' in combined:
            return 'CAMPAIGN_MANAGEMENT'
        else:
            return 'MARKETING_AUTOMATION'

    elif automation_type == 'DATA_SYNC':
        if 'backup' in combined:
            return 'DATA_BACKUP'
        elif 'sync' in combined:
            return 'DATA_SYNCHRONIZATION'
        elif 'scraping' in combined or 'scrape' in combined:
            return 'DATA_SCRAPING'
        else:
            return 'DATA_TRANSFER'

    elif automation_type == 'COMMUNICATION':
        if 'notification' in combined or 'alert' in combined:
            return 'NOTIFICATION'
        elif 'message' in combined:
            return 'MESSAGING'
        else:
            return 'COMMUNICATION_FLOW'

    elif automation_type == 'CUSTOMER_SUPPORT':
        if 'ticket' in combined:
            return 'TICKET_MANAGEMENT'
        else:
            return 'SUPPORT_AUTOMATION'

    elif automation_type == 'PRODUCTIVITY':
        if contains_any(apps, FORMS_APPS) or 'form' in combined:
            return 'FORM_PROCESSING'
        elif 'file' in combined or 'document' in combined:
            return 'FILE_MANAGEMENT'
        elif 'task' in combined:
            return 'TASK_MANAGEMENT'
        else:
            return 'WORKFLOW_AUTOMATION'

    else:
        return 'GENERAL_AUTOMATION'


def determine_primary_industry(row):
    """Determine primary industry/use case"""
    apps = row.get('apps_used', '').lower()
    desc = row.get('description', '').lower()
    name = row.get('name', '').lower()
    combined = f"{apps} {desc} {name}"

    if contains_any(combined, ['sales', 'crm', 'deal', 'pipeline']) or contains_any(apps, CRM_APPS):
        return 'SALES'
    elif contains_any(combined, ['marketing', 'campaign', 'lead', 'seo']) or contains_any(apps, SOCIAL_MEDIA_APPS):
        return 'MARKETING'
    elif contains_any(combined, ['hr', 'hiring', 'recruitment', 'employee', 'payroll']):
        return 'HR'
    elif contains_any(combined, ['it', 'devops', 'infrastructure', 'server']) or contains_any(combined, CODE_KEYWORDS):
        return 'IT'
    elif contains_any(combined, ['support', 'ticket', 'customer service', 'helpdesk']):
        return 'CUSTOMER_SUPPORT'
    elif contains_any(combined, ['finance', 'accounting', 'invoice', 'payment', 'expense']):
        return 'FINANCE'
    elif contains_any(combined, ['operations', 'inventory', 'supply chain', 'logistics']):
        return 'OPERATIONS'
    elif contains_any(combined, ['healthcare', 'medical', 'patient', 'health']):
        return 'HEALTHCARE'
    elif contains_any(combined, ['education', 'learning', 'student', 'course', 'training']):
        return 'EDUCATION'
    elif contains_any(apps, ECOMMERCE_APPS) or contains_any(combined, ['ecommerce', 'shop', 'order', 'product']):
        return 'ECOMMERCE'
    else:
        return 'GENERAL_BUSINESS'


def extract_use_case_tags(row):
    """Extract specific use case tags"""
    apps = row.get('apps_used', '').lower()
    desc = row.get('description', '').lower()
    name = row.get('name', '').lower()
    combined = f"{apps} {desc} {name}"

    tags = []

    # Lead generation/management
    if 'lead' in combined:
        if 'generat' in combined:
            tags.append('lead-generation')
        if 'capture' in combined:
            tags.append('lead-capture')
        if 'enrich' in combined or 'qualif' in combined:
            tags.append('lead-enrichment')

    # Email automation
    if contains_any(apps, EMAIL_APPS):
        if 'automat' in combined:
            tags.append('email-automation')
        if 'marketing' in combined:
            tags.append('email-marketing')

    # Social media
    if contains_any(apps, SOCIAL_MEDIA_APPS):
        tags.append('social-media-management')
        if 'post' in combined:
            tags.append('content-posting')

    # Data operations
    if 'data' in combined:
        if 'entry' in combined:
            tags.append('data-entry')
        if 'sync' in combined:
            tags.append('data-sync')
        if 'enrich' in combined:
            tags.append('data-enrichment')

    # Content
    if 'content' in combined:
        if 'creat' in combined or 'generat' in combined:
            tags.append('content-creation')
        if 'publish' in combined:
            tags.append('content-publishing')

    # Forms
    if contains_any(apps, FORMS_APPS) or 'form' in combined:
        tags.append('form-processing')
        if 'survey' in combined:
            tags.append('survey-automation')

    # Reporting
    if 'report' in combined or 'analytics' in combined:
        tags.append('reporting')
        if 'dashboard' in combined:
            tags.append('dashboard')

    # File management
    if 'file' in combined or 'document' in combined:
        tags.append('file-management')
        if 'generat' in combined:
            tags.append('document-generation')

    # Calendar/scheduling
    if 'calendar' in combined or 'meeting' in combined or 'appointment' in combined:
        tags.append('calendar-management')
        if 'schedul' in combined:
            tags.append('meeting-scheduling')

    # Customer support
    if 'ticket' in combined:
        tags.append('ticket-management')
    if 'support' in combined:
        tags.append('customer-support')

    return json.dumps(tags) if tags else ''


def determine_complexity_level(row):
    """Determine template complexity level"""
    app_count = count_apps(row.get('apps_used', ''))
    apps_lower = row.get('apps_used', '').lower()
    desc_lower = row.get('description', '').lower()

    has_code = contains_any(apps_lower, CODE_KEYWORDS)
    has_http = contains_any(apps_lower, HTTP_KEYWORDS)
    has_webhook = 'webhook' in apps_lower or 'gateway' in apps_lower
    has_conditional = 'if' in desc_lower or 'conditional' in desc_lower or 'filter' in desc_lower

    # Calculate complexity score
    complexity_score = 0
    complexity_score += app_count * 10
    if has_code: complexity_score += 30
    if has_http: complexity_score += 20
    if has_webhook: complexity_score += 15
    if has_conditional: complexity_score += 10

    if complexity_score <= 30:
        return 'BEGINNER'
    elif complexity_score <= 60:
        return 'INTERMEDIATE'
    elif complexity_score <= 90:
        return 'ADVANCED'
    else:
        return 'EXPERT'


def estimate_setup_time(complexity_level, app_count):
    """Estimate setup time based on complexity"""
    if complexity_level == 'BEGINNER' and app_count <= 2:
        return 'UNDER_5_MIN'
    elif complexity_level == 'BEGINNER' or (complexity_level == 'INTERMEDIATE' and app_count <= 3):
        return '5_15_MIN'
    elif complexity_level == 'INTERMEDIATE' or (complexity_level == 'ADVANCED' and app_count <= 4):
        return '15_30_MIN'
    else:
        return '30_MIN_PLUS'


def determine_integration_pattern(app_count, apps_used, name_desc):
    """Determine workflow integration pattern"""
    if app_count == 1:
        return 'SINGLE_APP'
    elif app_count == 2 and 'sync' in name_desc.lower():
        return 'TWO_WAY_SYNC'
    elif app_count >= 5:
        # Check if hub-and-spoke (one central app with many connections)
        return 'HUB_AND_SPOKE'
    elif app_count >= 3:
        return 'MULTI_STEP_WORKFLOW'
    else:
        return 'SIMPLE_WORKFLOW'


def detect_trigger_type(row):
    """Detect primary trigger type"""
    desc = row.get('description', '').lower()
    apps = row.get('apps_used', '').lower()
    name = row.get('name', '').lower()
    combined = f"{desc} {apps} {name}"

    if 'webhook' in combined or 'gateway' in apps:
        return 'WEBHOOK'
    elif 'schedule' in combined or 'daily' in combined or 'weekly' in combined or 'cron' in combined:
        return 'SCHEDULE'
    elif contains_any(apps, FORMS_APPS) or 'form' in combined or 'submission' in combined:
        return 'FORM_SUBMISSION'
    elif contains_any(apps, EMAIL_APPS) and ('new email' in combined or 'incoming email' in combined):
        return 'EMAIL'
    elif 'new row' in combined or 'new record' in combined:
        return 'NEW_ROW'
    elif 'file' in combined or 'upload' in combined:
        return 'FILE_UPLOAD'
    elif 'message' in combined or contains_any(apps, COMMUNICATION_APPS):
        return 'MESSAGE'
    elif 'manual' in combined:
        return 'MANUAL'
    else:
        return 'WATCH'


def detect_action_type(row):
    """Detect primary action type"""
    desc = row.get('description', '').lower()
    apps = row.get('apps_used', '').lower()
    name = row.get('name', '').lower()
    combined = f"{desc} {apps} {name}"

    if 'create' in combined or 'add' in combined:
        return 'CREATE_RECORD'
    elif 'update' in combined or 'edit' in combined:
        return 'UPDATE_DATA'
    elif 'send' in combined and contains_any(apps, EMAIL_APPS):
        return 'SEND_EMAIL'
    elif 'send' in combined or 'post' in combined and contains_any(apps, COMMUNICATION_APPS):
        return 'SEND_MESSAGE'
    elif 'generate' in combined or 'create content' in combined:
        return 'GENERATE_CONTENT'
    elif 'post' in combined and contains_any(apps, SOCIAL_MEDIA_APPS):
        return 'POST_SOCIAL'
    elif 'file' in combined:
        return 'CREATE_FILE'
    elif 'analyze' in combined or 'report' in combined:
        return 'ANALYZE_DATA'
    else:
        return 'PROCESS_DATA'


def detect_ai_use_case(row):
    """Detect AI-specific use case"""
    desc = row.get('description', '').lower()
    apps = row.get('apps_used', '').lower()
    name = row.get('name', '').lower()
    combined = f"{desc} {apps} {name}"

    if 'chatbot' in combined or 'chat' in combined:
        return 'CHATBOT'
    elif 'content' in combined or 'writing' in combined or 'blog' in combined:
        return 'CONTENT_GENERATION'
    elif 'summary' in combined or 'summarize' in combined:
        return 'SUMMARIZATION'
    elif 'classif' in combined or 'categoriz' in combined:
        return 'CLASSIFICATION'
    elif 'extract' in combined:
        return 'EXTRACTION'
    elif 'translate' in combined or 'translation' in combined:
        return 'TRANSLATION'
    elif 'sentiment' in combined:
        return 'SENTIMENT_ANALYSIS'
    elif 'image' in combined or 'dall-e' in combined or 'midjourney' in combined:
        return 'IMAGE_GENERATION'
    elif 'transcri' in combined or 'whisper' in combined or 'audio' in combined:
        return 'TRANSCRIPTION'
    elif 'embedding' in combined or 'vector' in combined or 'semantic' in combined:
        return 'EMBEDDINGS_SEARCH'
    else:
        return 'AI_PROCESSING'


def detect_ai_provider(apps_used):
    """Detect AI provider"""
    apps_lower = apps_used.lower()

    providers = []
    if 'openai' in apps_lower or 'gpt' in apps_lower or 'chatgpt' in apps_lower:
        providers.append('OPENAI')
    if 'anthropic' in apps_lower or 'claude' in apps_lower:
        providers.append('ANTHROPIC')
    if 'google' in apps_lower or 'gemini' in apps_lower or 'palm' in apps_lower:
        providers.append('GOOGLE')

    if len(providers) > 1:
        return 'MULTIPLE'
    elif len(providers) == 1:
        return providers[0]
    else:
        return 'OTHER'


def determine_target_company_size(row, complexity_level):
    """Determine target company size"""
    apps = row.get('apps_used', '').lower()
    desc = row.get('description', '').lower()
    combined = f"{apps} {desc}"

    # Enterprise indicators
    enterprise_apps = ['salesforce', 'workday', 'sap', 'oracle', 'servicenow']
    if contains_any(combined, enterprise_apps):
        return 'ENTERPRISE'

    # SMB indicators
    smb_apps = ['quickbooks', 'xero', 'mailchimp']
    if contains_any(combined, smb_apps):
        return 'SMB'

    # Solopreneur indicators
    if complexity_level == 'BEGINNER' and count_apps(row.get('apps_used', '')) <= 2:
        return 'SOLOPRENEUR'

    # Default based on complexity
    if complexity_level in ['BEGINNER', 'INTERMEDIATE']:
        return 'SMB'
    elif complexity_level == 'ADVANCED':
        return 'MIDMARKET'
    else:
        return 'ALL'


def estimate_time_saved(automation_type, complexity_level, app_count):
    """Estimate time saved per week"""
    # Base time savings
    base_savings = {
        'BEGINNER': 1,
        'INTERMEDIATE': 3,
        'ADVANCED': 8,
        'EXPERT': 15
    }

    time_value = base_savings.get(complexity_level, 3)

    # Adjust for automation type
    if automation_type in ['AI_AUTOMATION', 'MARKETING', 'CUSTOMER_SUPPORT']:
        time_value *= 1.5
    elif automation_type in ['DATA_SYNC', 'INTEGRATION']:
        time_value *= 1.2

    # Adjust for number of apps (more apps = more time saved)
    if app_count >= 5:
        time_value *= 1.3

    if time_value < 1:
        return 'UNDER_1HR_WEEK'
    elif time_value < 5:
        return '1_5HR_WEEK'
    elif time_value < 20:
        return '5_20HR_WEEK'
    else:
        return '20HR_PLUS_WEEK'


# ============================================================================
# MAIN ENRICHMENT FUNCTION
# ============================================================================

def enrich_template(row, all_views, all_usage):
    """Enrich a single template with new categorization columns"""
    enriched = row.copy()

    # Parse existing fields
    apps_used = row.get('apps_used', '')
    description = row.get('description', '')
    name = row.get('name', '')
    total_views = row.get('total_views', '')
    usage_count = row.get('usage_count', '')
    nodes_used = row.get('nodes_used', '')

    # Calculate app count
    app_count = count_apps(apps_used)
    enriched['app_count'] = app_count

    # Calculate node count (use existing or estimate)
    try:
        node_count = int(nodes_used) if nodes_used else max(app_count, 1)
    except:
        node_count = max(app_count, 1)
    enriched['node_count'] = node_count

    # Core categorization
    automation_type = determine_automation_type(row)
    enriched['automation_type'] = automation_type
    enriched['automation_subtype'] = determine_automation_subtype(row, automation_type)
    enriched['primary_industry'] = determine_primary_industry(row)
    enriched['use_case_tags'] = extract_use_case_tags(row)

    # Complexity
    complexity_level = determine_complexity_level(row)
    enriched['complexity_level'] = complexity_level
    enriched['estimated_setup_time'] = estimate_setup_time(complexity_level, app_count)
    enriched['requires_coding'] = contains_any(apps_used, CODE_KEYWORDS)
    enriched['requires_api_keys'] = app_count > 0  # Most integrations need API keys

    # Technology flags
    enriched['is_ai_powered'] = contains_any(f"{apps_used} {description} {name}", AI_KEYWORDS)
    enriched['is_webhook_based'] = 'webhook' in apps_used.lower() or 'gateway' in apps_used.lower()
    enriched['is_scheduled'] = contains_any(f"{description} {name}", ['schedule', 'daily', 'weekly', 'cron', 'recurring'])
    enriched['is_realtime'] = contains_any(f"{description} {name}", ['real-time', 'instant', 'immediately', 'watch'])
    enriched['has_conditional_logic'] = contains_any(f"{description} {name}", ['if', 'conditional', 'filter', 'branch', 'router'])
    enriched['has_loops'] = contains_any(f"{description} {name}", ['loop', 'iterate', 'repeat', 'for each'])
    enriched['uses_llm'] = contains_any(apps_used, ['llm', 'language model', 'chat model', 'completion'])
    enriched['uses_embeddings'] = contains_any(apps_used, ['embedding', 'vector', 'pinecone', 'qdrant', 'weaviate'])
    enriched['uses_vision'] = contains_any(f"{apps_used} {description}", ['image generation', 'dall-e', 'vision', 'image analysis', 'stable diffusion'])
    enriched['uses_voice'] = contains_any(f"{apps_used} {description}", ['whisper', 'voice', 'audio', 'transcribe', 'speech', 'eleven'])
    enriched['has_memory'] = contains_any(apps_used, ['memory', 'conversation', 'context', 'history'])

    # App category flags
    enriched['uses_spreadsheet'] = contains_any(apps_used, SPREADSHEET_APPS)
    enriched['uses_email'] = contains_any(apps_used, EMAIL_APPS)
    enriched['uses_storage'] = contains_any(apps_used, STORAGE_APPS)
    enriched['uses_communication'] = contains_any(apps_used, COMMUNICATION_APPS)
    enriched['uses_crm'] = contains_any(apps_used, CRM_APPS)
    enriched['uses_social_media'] = contains_any(apps_used, SOCIAL_MEDIA_APPS)
    enriched['uses_ecommerce'] = contains_any(apps_used, ECOMMERCE_APPS)
    enriched['uses_project_mgmt'] = contains_any(apps_used, PROJECT_MGMT_APPS)
    enriched['uses_forms'] = contains_any(apps_used, FORMS_APPS)

    # Integration pattern and triggers
    enriched['integration_pattern'] = determine_integration_pattern(app_count, apps_used, f"{name} {description}")
    enriched['primary_trigger_type'] = detect_trigger_type(row)
    enriched['primary_action_type'] = detect_action_type(row)

    # Popularity metrics
    try:
        if total_views:
            views_val = int(total_views)
            percentile = calculate_percentile(all_views, views_val)
        elif usage_count:
            usage_val = int(usage_count)
            percentile = calculate_percentile(all_usage, usage_val)
        else:
            percentile = None

        if percentile is not None:
            if percentile >= 99:
                enriched['popularity_tier'] = 'VIRAL'
                enriched['engagement_score'] = 95
            elif percentile >= 90:
                enriched['popularity_tier'] = 'POPULAR'
                enriched['engagement_score'] = 80
            elif percentile >= 50:
                enriched['popularity_tier'] = 'MODERATE'
                enriched['engagement_score'] = 50
            else:
                enriched['popularity_tier'] = 'NICHE'
                enriched['engagement_score'] = 20
        else:
            enriched['popularity_tier'] = 'UNKNOWN'
            enriched['engagement_score'] = 0
    except:
        enriched['popularity_tier'] = 'UNKNOWN'
        enriched['engagement_score'] = 0

    # Trending potential
    is_ai = enriched['is_ai_powered']
    is_popular = enriched['popularity_tier'] in ['VIRAL', 'POPULAR']
    if is_ai and is_popular:
        enriched['trending_potential'] = 'HIGH'
    elif is_ai or is_popular:
        enriched['trending_potential'] = 'MEDIUM'
    else:
        enriched['trending_potential'] = 'LOW'

    # AI-specific fields
    if enriched['is_ai_powered']:
        enriched['ai_use_case'] = detect_ai_use_case(row)
        enriched['ai_provider'] = detect_ai_provider(apps_used)
        enriched['has_rag'] = contains_any(apps_used, ['vector', 'embedding', 'pinecone', 'qdrant', 'semantic'])
    else:
        enriched['ai_use_case'] = ''
        enriched['ai_provider'] = ''
        enriched['has_rag'] = False

    # Business value
    value_tags = []
    if automation_type in ['AI_AUTOMATION', 'MARKETING', 'PRODUCTIVITY']:
        value_tags.append('time-savings')
    if automation_type in ['MARKETING', 'SALES', 'ECOMMERCE']:
        value_tags.append('revenue-generation')
    if automation_type in ['DATA_SYNC', 'INTEGRATION']:
        value_tags.append('process-optimization')
    if complexity_level in ['BEGINNER', 'INTERMEDIATE']:
        value_tags.append('easy-to-implement')
    enriched['business_value_tags'] = json.dumps(value_tags) if value_tags else ''

    enriched['target_company_size'] = determine_target_company_size(row, complexity_level)
    enriched['estimated_time_saved'] = estimate_time_saved(automation_type, complexity_level, app_count)

    # Keywords extraction (basic - extract key terms from name)
    keywords = []
    name_words = re.findall(r'\b\w+\b', name.lower())
    stopwords = ['and', 'the', 'a', 'to', 'from', 'with', 'for', 'in', 'on', 'at', 'of']
    keywords = [w for w in name_words if len(w) > 3 and w not in stopwords][:10]
    enriched['keywords'] = json.dumps(keywords) if keywords else ''

    return enriched


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    logging.info("=" * 80)
    logging.info("  ENRICHING UNIFIED CSV WITH CATEGORIZATION COLUMNS")
    logging.info("=" * 80)
    logging.info("")

    # Load unified CSV
    input_file = './exports/unified_templates_20251028_114032.csv'

    logging.info(f"📥 Loading unified CSV: {input_file}")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        # Try to find the latest unified file
        import glob
        unified_files = glob.glob('./exports/unified_templates_*.csv')
        if unified_files:
            input_file = max(unified_files)  # Get most recent
            logging.info(f"Using latest unified file: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        else:
            logging.error("❌ No unified CSV file found!")
            return 1

    logging.info(f"✅ Loaded {len(rows):,} templates")
    logging.info("")

    # Collect all views and usage for percentile calculation
    logging.info("📊 Calculating popularity metrics...")
    all_views = []
    all_usage = []
    for row in rows:
        try:
            if row.get('total_views'):
                all_views.append(int(row['total_views']))
        except:
            pass
        try:
            if row.get('usage_count'):
                all_usage.append(int(row['usage_count']))
        except:
            pass

    logging.info(f"   • {len(all_views):,} templates have view counts")
    logging.info(f"   • {len(all_usage):,} templates have usage counts")
    logging.info("")

    # Enrich each template
    logging.info("🔄 Enriching templates...")
    enriched_rows = []

    for i, row in enumerate(rows, 1):
        if i % 1000 == 0:
            logging.info(f"   Processed {i:,}/{len(rows):,} templates ({i/len(rows)*100:.1f}%)")

        try:
            enriched = enrich_template(row, all_views, all_usage)
            enriched_rows.append(enriched)
        except Exception as e:
            logging.error(f"   Error enriching template {row.get('platform_id', 'unknown')}: {e}")
            enriched_rows.append(row)  # Keep original if enrichment fails

    logging.info(f"✅ Enriched {len(enriched_rows):,} templates")
    logging.info("")

    # Write enriched CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'./exports/unified_templates_enriched_{timestamp}.csv'

    logging.info(f"💾 Writing enriched CSV: {output_file}")

    # Get all fieldnames (original + new)
    if enriched_rows:
        fieldnames = list(enriched_rows[0].keys())

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(enriched_rows)

        import os
        file_size = os.path.getsize(output_file)
        file_size_mb = file_size / (1024 * 1024)

        logging.info(f"✅ Enriched CSV created successfully!")
        logging.info(f"   File: {output_file}")
        logging.info(f"   Size: {file_size_mb:.2f} MB")
        logging.info(f"   Templates: {len(enriched_rows):,}")
        logging.info(f"   Columns: {len(fieldnames)} (30 original + {len(fieldnames) - 30} new)")
        logging.info("")

        # Generate statistics
        logging.info("📊 Enrichment Statistics:")

        # Count by automation type
        automation_types = Counter(row['automation_type'] for row in enriched_rows if row.get('automation_type'))
        logging.info(f"   Automation Types:")
        for atype, count in automation_types.most_common(10):
            pct = (count / len(enriched_rows)) * 100
            logging.info(f"      • {atype}: {count:,} ({pct:.1f}%)")

        # AI stats
        ai_count = sum(1 for row in enriched_rows if row.get('is_ai_powered') == True)
        logging.info(f"   AI-Powered: {ai_count:,} ({ai_count/len(enriched_rows)*100:.1f}%)")

        # Complexity stats
        complexity_counts = Counter(row['complexity_level'] for row in enriched_rows if row.get('complexity_level'))
        logging.info(f"   Complexity Levels:")
        for level in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']:
            count = complexity_counts.get(level, 0)
            pct = (count / len(enriched_rows)) * 100
            logging.info(f"      • {level}: {count:,} ({pct:.1f}%)")

        logging.info("")
        logging.info("=" * 80)
        logging.info("  ENRICHMENT COMPLETE")
        logging.info("=" * 80)

        return 0

    else:
        logging.error("❌ No templates to write!")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
