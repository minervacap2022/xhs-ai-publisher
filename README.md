# XHS AI-Powered Auto-Publisher Service
## 小红书 AI 自动化发布服务

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

### 🌟 Service Overview

An intelligent content automation service for Xiaohongshu (Little Red Book) that leverages AI to create authentic, personality-driven posts. The service features a unique persona - "Cheng Lingjiu (程零九)" - an alien cultural researcher studying Earth, providing fresh perspectives on daily news and cultural observations.

### 💡 Key Features

- **AI-Powered Content Generation**: Uses Qwen API for intelligent content creation
- **Psychological Growth System**: Implements a sophisticated personality evolution model
- **News Analysis Pipeline**: Automatically collects and analyzes trending news from multiple sources
- **Authentic Voice**: Maintains consistent personality with emotional depth and cultural sensitivity
- **Automated Publishing**: Seamless integration with Xiaohongshu platform via MCP
- **Smart Scheduling**: Configurable posting schedules with daemon mode support

### 🎭 Unique Persona System

The service features "Cheng Lingjiu" - an alien cultural researcher with:
- Dynamic psychological profile based on Big Five personality traits
- Emotional intelligence development tracking
- Cultural adaptation journey simulation
- Genuine emotional responses to world events

### 🛠️ Technical Architecture

```
┌─────────────────────────────────────┐
│         News Collection             │
│    (Jina Reader API + Sources)      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Content Analysis & Growth      │
│   (Qwen API + Psychology Engine)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        Content Generation           │
│    (Personality-Influenced AI)      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Xiaohongshu Publishing          │
│        (MCP Integration)            │
└─────────────────────────────────────┘
```

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/chengyixu/xhs-ai-publisher.git
cd xhs-ai-publisher

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### ⚙️ Configuration

1