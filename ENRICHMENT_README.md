# CSV Enrichment - Categorization & Filtering Columns

Complete documentation for the enriched unified CSV with 43 new categorization columns.

## Quick Start

### Generate Enriched CSV:

```bash
python enrich_unified_csv.py
```

This will:
- Load the unified CSV (15,011 templates)
- Apply comprehensive categorization logic
- Add 43 new columns for filtering and analysis
- Output enriched CSV with 73 total columns

## Output

**File**: `./exports/unified_templates_enriched_[timestamp].csv`
**Size**: ~50 MB
**Templates**: 15,011
**Columns**: 73 (30 original + 43 new)

---

## New Columns Reference

### Core Categories (6 columns)

#### `automation_type` (String)
**Primary automation category**

**Values**: `AI_AUTOMATION`, `DATA_SYNC`, `COMMUNICATION`, `MARKETING`, `PRODUCTIVITY`, `ECOMMERCE`, `DEVELOPMENT`, `HR`, `CUSTOMER_SUPPORT`, `ANALYTICS`, `INTEGRATION`

**Distribution**:
- AI_AUTOMATION: 62.0%
- INTEGRATION: 10.1%
- MARKETING: 7.7%
- COMMUNICATION: 7.7%
- Others: 12.5%

**Use Case**: Primary filtering and categorization

---

#### `automation_subtype` (String)
**Secondary automation category**

**Values**: `CHATBOT`, `CONTENT_GENERATION`, `SUMMARIZATION`, `LEAD_CAPTURE`, `EMAIL_AUTOMATION`, `SOCIAL_POSTING`, `DATA_SYNCHRONIZATION`, `NOTIFICATION`, `FORM_PROCESSING`, and more

**Use Case**: Granular filtering within automation types

---

#### `primary_industry` (String)
**Target industry or business function**

**Values**: `SALES`, `MARKETING`, `HR`, `IT`, `CUSTOMER_SUPPORT`, `FINANCE`, `OPERATIONS`, `HEALTHCARE`, `EDUCATION`, `ECOMMERCE`, `GENERAL_BUSINESS`

**Use Case**: Industry-specific template discovery

---

#### `use_case_tags` (JSON Array)
**Specific use cases**

**Example Values**:
```json
["lead-generation", "email-automation", "content-creation"]
```

**Common Tags**:
- lead-generation, lead-capture, lead-enrichment
- email-automation, email-marketing
- social-media-management, content-posting
- data-entry, data-sync, data-enrichment
- customer-support, ticket-management
- form-processing, survey-automation
- reporting, analytics

**Use Case**: Multi-faceted filtering and discovery

---

#### `complexity_level` (String)
**Technical complexity rating**

**Values**: `BEGINNER`, `INTERMEDIATE`, `ADVANCED`, `EXPERT`

**Distribution**:
- BEGINNER: 55.7%
- INTERMEDIATE: 21.2%
- ADVANCED: 12.1%
- EXPERT: 11.0%

**Logic**: Based on app count, code requirements, HTTP/webhooks, conditional logic

**Use Case**: Skill-based filtering

---

#### `estimated_setup_time` (String)
**Time needed to implement**

**Values**: `UNDER_5_MIN`, `5_15_MIN`, `15_30_MIN`, `30_MIN_PLUS`

**Logic**: Derived from complexity level and app count

**Use Case**: Time-based planning

---

### Metrics & Counts (2 columns)

#### `app_count` (Integer)
**Number of apps/integrations used**

**Range**: 0 to 48
**Average**: 2.9 apps per template

**Use Case**: Filter by integration complexity

---

#### `node_count` (Integer)
**Number of workflow steps/nodes**

**Range**: 1 to 100+
**Source**: Direct from n8n data, estimated for Make/Zapier

**Use Case**: Workflow complexity assessment

---

### Requirements (2 boolean columns)

#### `requires_coding` (Boolean)
**Needs programming skills**

**Logic**: Contains code, JavaScript, Python, custom functions

**% True**: ~18% of templates

---

#### `requires_api_keys` (Boolean)
**Needs API authentication**

**Logic**: Most integrations require API keys

**% True**: ~97% of templates

---

### Technology Flags (11 boolean columns)

#### `is_ai_powered` (Boolean)
**Uses AI/ML capabilities**

**Keywords**: OpenAI, ChatGPT, Claude, Gemini, AI Agent, LLM

**% True**: 62.0% (9,303 templates)

**Use Case**: Find AI-enhanced automations

---

#### `is_webhook_based` (Boolean)
**Triggered by webhooks**

**% True**: 2.7%

---

#### `is_scheduled` (Boolean)
**Runs on a schedule**

**Keywords**: schedule, daily, weekly, cron, recurring

**% True**: 17.8%

---

#### `is_realtime` (Boolean)
**Real-time processing**

**Keywords**: real-time, instant, immediately, watch

**% True**: ~15%

---

#### `has_conditional_logic` (Boolean)
**Includes if/then logic**

**Keywords**: if, conditional, filter, branch, router

**% True**: 52.7%

---

#### `has_loops` (Boolean)
**Includes iteration**

**Keywords**: loop, iterate, repeat, for each

**% True**: ~8%

---

#### `uses_llm` (Boolean)
**Uses language models**

**Keywords**: LLM, language model, chat model, completion

**% True**: ~45%

---

#### `uses_embeddings` (Boolean)
**Uses vector embeddings**

**Keywords**: embedding, vector, Pinecone, Qdrant, Weaviate

**% True**: ~5%

---

#### `uses_vision` (Boolean)
**Uses image AI**

**Keywords**: image generation, DALL-E, vision, Stable Diffusion

**% True**: ~2%

---

#### `uses_voice` (Boolean)
**Uses audio/speech AI**

**Keywords**: Whisper, voice, audio, transcribe, ElevenLabs

**% True**: ~1%

---

#### `has_memory` (Boolean)
**Has conversation memory**

**Keywords**: memory, conversation, context, history

**% True**: ~8%

---

### App Category Flags (9 boolean columns)

#### `uses_spreadsheet` (Boolean)
**Apps**: Google Sheets, Excel, Airtable
**% True**: 26.6%

#### `uses_email` (Boolean)
**Apps**: Gmail, Outlook, Mailchimp, SendGrid
**% True**: 15.9%

#### `uses_storage` (Boolean)
**Apps**: Google Drive, Dropbox, OneDrive, Box
**% True**: ~10%

#### `uses_communication` (Boolean)
**Apps**: Slack, Telegram, Discord, Teams, WhatsApp
**% True**: 17.2%

#### `uses_crm` (Boolean)
**Apps**: Salesforce, HubSpot, Pipedrive
**% True**: ~5%

#### `uses_social_media` (Boolean)
**Apps**: Facebook, Instagram, LinkedIn, Twitter, TikTok
**% True**: ~8%

#### `uses_ecommerce` (Boolean)
**Apps**: Shopify, WooCommerce, Stripe, PayPal
**% True**: ~3%

#### `uses_project_mgmt` (Boolean)
**Apps**: Trello, Asana, Jira, Notion, ClickUp
**% True**: ~7%

#### `uses_forms` (Boolean)
**Apps**: Typeform, Google Forms, Jotform
**% True**: ~4%

---

### Workflow Patterns (3 columns)

#### `integration_pattern` (String)
**Workflow architecture pattern**

**Values**:
- `SINGLE_APP`: Single app automation
- `TWO_WAY_SYNC`: Bidirectional sync between two apps
- `MULTI_STEP_WORKFLOW`: Sequential workflow (most common)
- `HUB_AND_SPOKE`: Central hub with multiple integrations
- `SIMPLE_WORKFLOW`: Basic 2-3 step automation

---

#### `primary_trigger_type` (String)
**How the workflow starts**

**Values**: `WEBHOOK`, `SCHEDULE`, `MANUAL`, `EMAIL`, `FORM_SUBMISSION`, `NEW_ROW`, `FILE_UPLOAD`, `MESSAGE`, `WATCH`

**Most Common**: WATCH (40%), SCHEDULE (18%), WEBHOOK (3%)

---

#### `primary_action_type` (String)
**Main action performed**

**Values**: `CREATE_RECORD`, `SEND_MESSAGE`, `UPDATE_DATA`, `GENERATE_CONTENT`, `SEND_EMAIL`, `POST_SOCIAL`, `CREATE_FILE`, `ANALYZE_DATA`, `PROCESS_DATA`

**Most Common**: PROCESS_DATA, CREATE_RECORD, SEND_MESSAGE

---

### Popularity Metrics (3 columns)

#### `popularity_tier` (String)
**Popularity ranking**

**Values**: `VIRAL` (top 1%), `POPULAR` (top 10%), `MODERATE` (top 50%), `NICHE` (bottom 50%), `UNKNOWN` (no data)

**Distribution**:
- VIRAL: 1.0% (147 templates)
- POPULAR: 8.7% (1,312 templates)
- MODERATE: 39.8% (5,975 templates)
- NICHE: 47.4% (7,114 templates)
- UNKNOWN: 3.1% (463 templates, mostly Zapier)

**Logic**: Percentile-based on total_views (n8n) or usage_count (Make.com)

---

#### `engagement_score` (Integer)
**0-100 normalized popularity score**

**Distribution**:
- 95: VIRAL tier
- 80: POPULAR tier
- 50: MODERATE tier
- 20: NICHE tier
- 0: UNKNOWN

---

#### `trending_potential` (String)
**Future popularity prediction**

**Values**: `HIGH`, `MEDIUM`, `LOW`

**Logic**:
- HIGH: AI-powered AND popular
- MEDIUM: AI-powered OR popular
- LOW: Neither

---

### AI-Specific Columns (3 columns)

#### `ai_use_case` (String)
**AI-specific purpose** (only for AI-powered templates)

**Values**: `CHATBOT`, `CONTENT_GENERATION`, `SUMMARIZATION`, `CLASSIFICATION`, `EXTRACTION`, `TRANSLATION`, `SENTIMENT_ANALYSIS`, `IMAGE_GENERATION`, `TRANSCRIPTION`, `EMBEDDINGS_SEARCH`, `AI_PROCESSING`

**Most Common**: CHATBOT (30%), CONTENT_GENERATION (25%)

---

#### `ai_provider` (String)
**AI service provider** (only for AI-powered templates)

**Values**: `OPENAI`, `ANTHROPIC`, `GOOGLE`, `MULTIPLE`, `OTHER`

**Distribution**:
- OPENAI: 45%
- GOOGLE: 25%
- MULTIPLE: 20%
- ANTHROPIC: 5%
- OTHER: 5%

---

#### `has_rag` (Boolean)
**Uses RAG (Retrieval Augmented Generation)**

**Keywords**: vector, embedding, Pinecone, Qdrant, semantic search

**% True**: ~5% of AI templates

---

### Business Value (3 columns)

#### `business_value_tags` (JSON Array)
**Business benefits**

**Example Values**:
```json
["time-savings", "revenue-generation", "process-optimization", "easy-to-implement"]
```

**Common Tags**:
- time-savings
- revenue-generation
- cost-savings
- process-optimization
- easy-to-implement
- scalability

---

#### `target_company_size` (String)
**Target audience size**

**Values**: `SOLOPRENEUR`, `SMB`, `MIDMARKET`, `ENTERPRISE`, `ALL`

**Logic**: Based on complexity and enterprise apps (Salesforce, Workday, SAP)

---

#### `estimated_time_saved` (String)
**Time savings per week**

**Values**: `UNDER_1HR_WEEK`, `1_5HR_WEEK`, `5_20HR_WEEK`, `20HR_PLUS_WEEK`

**Logic**: Calculated from automation type, complexity, and app count

---

### Search Enhancement (1 column)

#### `keywords` (JSON Array)
**Extracted search keywords**

**Example**: `["email", "automation", "ai", "content"]`

**Logic**: Extracts key terms from template name, removes stopwords

**Use Case**: Search optimization and related template discovery

---

## Usage Examples

### Example 1: Find AI Chatbots for Customer Support
```sql
SELECT * FROM templates
WHERE is_ai_powered = true
  AND ai_use_case = 'CHATBOT'
  AND primary_industry = 'CUSTOMER_SUPPORT'
  AND complexity_level IN ('BEGINNER', 'INTERMEDIATE')
ORDER BY engagement_score DESC
```

**Result**: ~200 templates

---

### Example 2: Beginner-Friendly Email Automations
```sql
SELECT * FROM templates
WHERE uses_email = true
  AND complexity_level = 'BEGINNER'
  AND estimated_setup_time IN ('UNDER_5_MIN', '5_15_MIN')
  AND requires_coding = false
ORDER BY popularity_tier DESC
```

**Result**: ~400 templates

---

### Example 3: High-ROI Marketing Automations
```sql
SELECT * FROM templates
WHERE automation_type = 'MARKETING'
  AND estimated_time_saved IN ('5_20HR_WEEK', '20HR_PLUS_WEEK')
  AND popularity_tier IN ('POPULAR', 'VIRAL')
  AND uses_social_media = true
```

**Result**: ~150 templates

---

### Example 4: Advanced AI with RAG
```sql
SELECT * FROM templates
WHERE is_ai_powered = true
  AND has_rag = true
  AND uses_embeddings = true
ORDER BY engagement_score DESC
```

**Result**: ~250 templates

---

### Example 5: Real-time Webhook Integrations
```sql
SELECT * FROM templates
WHERE is_webhook_based = true
  AND is_realtime = true
  AND uses_spreadsheet = true
ORDER BY app_count ASC
```

**Result**: ~80 templates

---

## Filtering Strategies

### By Skill Level
- Beginners: `complexity_level = 'BEGINNER' AND requires_coding = false`
- Intermediate: `complexity_level IN ('INTERMEDIATE', 'ADVANCED')`
- Experts: `complexity_level = 'EXPERT' OR requires_coding = true`

### By Time Constraint
- Quick wins: `estimated_setup_time = 'UNDER_5_MIN'`
- Weekend project: `estimated_setup_time IN ('15_30_MIN', '30_MIN_PLUS')`

### By Technology Stack
- AI-first: `is_ai_powered = true AND uses_llm = true`
- Traditional automation: `is_ai_powered = false`
- Multi-platform: `app_count >= 4`

### By Business Impact
- High ROI: `estimated_time_saved = '20HR_PLUS_WEEK'`
- Revenue-focused: `business_value_tags LIKE '%revenue-generation%'`
- Popular & proven: `popularity_tier IN ('VIRAL', 'POPULAR')`

---

## Statistics Summary

```
📊 ENRICHED CSV STATISTICS

Total Templates: 15,011
Total Columns: 73 (30 original + 43 new)

Automation Types:
  • AI_AUTOMATION: 62.0%
  • INTEGRATION: 10.1%
  • MARKETING: 7.7%
  • COMMUNICATION: 7.7%
  • Others: 12.5%

Complexity Distribution:
  • BEGINNER: 55.7%
  • INTERMEDIATE: 21.2%
  • ADVANCED: 12.1%
  • EXPERT: 11.0%

Technology Adoption:
  • AI-powered: 62.0%
  • Uses spreadsheets: 26.6%
  • Uses communication: 17.2%
  • Scheduled: 17.8%
  • Uses email: 15.9%
  • Has conditional logic: 52.7%

Popularity:
  • VIRAL: 1.0%
  • POPULAR: 8.7%
  • MODERATE: 39.8%
  • NICHE: 47.4%
  • UNKNOWN: 3.1%
```

---

## Regeneration

To regenerate with updated data:

```bash
# 1. Ensure you have the latest unified CSV
python create_unified_csv.py

# 2. Run enrichment
python enrich_unified_csv.py
```

The script will automatically find and use the latest unified CSV file.

---

## Column Categories Summary

| Category | Columns | Purpose |
|----------|---------|---------|
| **Core Categories** | 6 | Primary classification |
| **Metrics & Counts** | 2 | Quantitative measures |
| **Requirements** | 2 | Technical prerequisites |
| **Technology Flags** | 11 | Feature detection |
| **App Categories** | 9 | Integration types |
| **Workflow Patterns** | 3 | Architecture patterns |
| **Popularity** | 3 | Engagement metrics |
| **AI-Specific** | 3 | AI categorization |
| **Business Value** | 3 | ROI indicators |
| **Search** | 1 | Discovery enhancement |
| **TOTAL** | **43** | **Complete coverage** |

---

**Generated**: October 28, 2025
**Script**: `enrich_unified_csv.py`
**Status**: ✅ Production Ready
