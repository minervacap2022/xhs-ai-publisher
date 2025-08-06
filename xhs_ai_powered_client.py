#!/usr/bin/env python3
"""
小红书AI自动化客户端 - 程零九版本
外星政府工作女孩的地球学习之旅
XHS AI-Powered Auto-Publisher Service
"""

import asyncio
import json
import requests
import random
import re
import os
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import logging
from psychological_growth_manager import PsychologicalGrowthManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Load configuration from environment variables
from dotenv import load_dotenv
load_dotenv()

# 配置
PHONE = os.getenv("PHONE", "")
JSON_PATH = os.getenv("JSON_PATH", "./cookies")
IMAGE_PATH = os.getenv("IMAGE_PATH", "./screenshot.png")

# Qwen API 配置
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

# Jina API 配置
JINA_API_KEY = os.getenv("JINA_API_KEY", "")

# 文件路径
BASE_PATH = os.getenv("BASE_PATH", ".")
PERSONALITY_FILE = os.path.join(BASE_PATH, "personality.json")
UNDERSTANDINGS_FILE = os.path.join(BASE_PATH, "understandings.json")
MEMORIES_FILE = os.path.join(BASE_PATH, "memories.json")
POSTS_FILE = os.path.join(BASE_PATH, "posts.json")
KNOWLEDGE_FILE = os.path.join(BASE_PATH, "knowledge.json")

# 新闻源
NEWS_SOURCES = [
    {"name": "知乎", "url": "https://tophub.today/n/mproPpoq6O"},
    {"name": "微博", "url": "https://tophub.today/n/KqndgxeLl9"},
    {"name": "微信", "url": "https://tophub.today/n/WnBe01o371"},
    {"name": "抖音", "url": "https://tophub.today/n/DpQvNABoNE"},
    {"name": "小红书", "url": "https://tophub.today/n/L4MdA5ldxD"}
]

# MCP服务器参数
server_params = StdioServerParameters(
    command="uvx",
    args=["xhs_mcp_server@latest"],
    env={
        "phone": PHONE,
        "json_path": JSON_PATH
    }
)

class PersonalityManager:
    """人设管理器 - 增强心理学成长功能"""
    
    def __init__(self):
        self.personality = self.load_personality()
        self.understandings = self.load_understandings()
        self.memories = self.load_memories()
        self.posts = self.load_posts()
        self.knowledge = self.load_knowledge()
        
        # 初始化心理学成长管理器
        self.growth_manager = PsychologicalGrowthManager(PERSONALITY_FILE)
    
    def _ensure_int(self, value, default=0):
        """确保值是整数类型"""
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        else:
            return default
    
    def load_json_file(self, filepath, default_data):
        """加载JSON文件"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                self.save_json_file(filepath, default_data)
                return default_data
        except Exception as e:
            logging.error(f"加载文件 {filepath} 失败: {e}")
            return default_data
    
    def save_json_file(self, filepath, data):
        """保存JSON文件"""
        try:
            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"保存文件 {filepath} 失败: {e}")
    
    def load_personality(self):
        """加载人设 - 兼容新旧格式"""
        # 尝试加载现有文件
        existing_data = self.load_json_file(PERSONALITY_FILE, {})
        
        # 如果是新格式，直接返回
        if "psychological_profile" in existing_data:
            return existing_data
        
        # 如果是旧格式或为空，使用默认的新格式
        default_personality = {
            "basic_info": {
                "name": "程零九",
                "age": 23,
                "species": "外星人",
                "job": "外星政府文化研究员",
                "location": "地球",
                "mission": "深度研究地球文化心理学，建立跨星际文化桥梁"
            },
            "psychological_profile": {
                "big_five_personality": {
                    "openness": 85,
                    "conscientiousness": 75,
                    "extraversion": 35,
                    "agreeableness": 70,
                    "neuroticism": 60,
                    "growth_trend": "openness和conscientiousness在提升，neuroticism在下降"
                },
                "emotional_intelligence": {
                    "self_awareness": 70,
                    "self_regulation": 65,
                    "social_awareness": 55,
                    "relationship_management": 45,
                    "emotional_growth_stage": "从情感新手向情感理解者转变"
                }
            },
            "current_psychological_state": {
                "mood_baseline": "轻度忧郁但稳定",
                "anxiety_level": "文化适应性焦虑，可管理",
                "curiosity_index": "高度活跃",
                "overall_wellbeing": "成长导向的适应状态"
            },
            "learning_progress": {
                "daily_hours_target": 4,
                "total_days": self._ensure_int(existing_data.get("learning_progress", {}).get("total_days", 3)),
                "last_study_date": existing_data.get("learning_progress", {}).get("last_study_date", "2025-06-30"),
                "psychological_milestones": [
                    "从文化shock到文化curiosity的转变",
                    "从language anxiety到expression confidence的发展"
                ]
            }
        }
        
        # 保存新格式
        self.save_json_file(PERSONALITY_FILE, default_personality)
        return default_personality
    
    def load_understandings(self):
        """加载理解"""
        default_understandings = {
            "about_earth": {
                "humans": "和我们长得很像，可能形状是好的方案",
                "culture": "复杂但有趣",
                "language": "还在学习中"
            },
            "daily_observations": [],
            "confusion_points": [],
            "new_discoveries": []
        }
        return self.load_json_file(UNDERSTANDINGS_FILE, default_understandings)
    
    def load_memories(self):
        """加载分析记忆"""
        default_memories = {
            "daily_analysis": [],
            "news_insights": [],
            "personal_thoughts": []
        }
        return self.load_json_file(MEMORIES_FILE, default_memories)
    
    def load_posts(self):
        """加载发布记录"""
        default_posts = {
            "history": [],
            "themes": [],
            "engagement": []
        }
        return self.load_json_file(POSTS_FILE, default_posts)
    
    def load_knowledge(self):
        """加载知识库"""
        default_knowledge = {
            "daily_news": [],
            "trending_topics": [],
            "learning_materials": []
        }
        return self.load_json_file(KNOWLEDGE_FILE, default_knowledge)
    
    def save_all(self):
        """保存所有数据"""
        self.save_json_file(PERSONALITY_FILE, self.personality)
        self.save_json_file(UNDERSTANDINGS_FILE, self.understandings)
        self.save_json_file(MEMORIES_FILE, self.memories)
        self.save_json_file(POSTS_FILE, self.posts)
        self.save_json_file(KNOWLEDGE_FILE, self.knowledge)

class NewsCollector:
    """新闻收集器"""
    
    def __init__(self, personality_manager):
        self.pm = personality_manager
    
    def call_jina_api(self, url):
        """调用Jina Reader API"""
        try:
            headers = {
                "Authorization": f"Bearer {JINA_API_KEY}",
                "Accept": "application/json"
            }
            
            jina_url = f"https://r.jina.ai/{url}"
            response = requests.get(jina_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("content", "")
            else:
                logging.error(f"Jina API调用失败: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Jina API调用异常: {e}")
            return None
    
    def collect_daily_news(self):
        """收集每日新闻"""
        today = datetime.now().strftime("%Y-%m-%d")
        news_data = {
            "date": today,
            "sources": {}
        }
        
        for source in NEWS_SOURCES:
            logging.info(f"正在爬取 {source['name']} 新闻...")
            content = self.call_jina_api(source['url'])
            
            if content:
                # 简化内容，提取关键信息
                simplified_content = self.extract_key_news(content, source['name'])
                news_data["sources"][source['name']] = simplified_content
            
            time.sleep(2)  # 避免请求过于频繁
        
        # 保存到知识库
        self.pm.knowledge["daily_news"].append(news_data)
        
        # 只保留最近30天的新闻
        if len(self.pm.knowledge["daily_news"]) > 30:
            self.pm.knowledge["daily_news"] = self.pm.knowledge["daily_news"][-30:]
        
        self.pm.save_json_file(KNOWLEDGE_FILE, self.pm.knowledge)
        logging.info("新闻收集完成")
        return news_data
    
    def extract_key_news(self, content, source_name):
        """提取关键新闻信息"""
        # 简单的关键词提取，实际应用中可以更复杂
        lines = content.split('\n')
        key_news = []
        
        for line in lines[:20]:  # 只取前20行
            line = line.strip()
            if len(line) > 10 and not line.startswith('#'):
                key_news.append(line)
        
        return key_news[:10]  # 最多10条

class ContentAnalyzer:
    """内容分析器"""
    
    def __init__(self, personality_manager):
        self.pm = personality_manager
    
    def call_qwen_api(self, prompt, max_tokens=1000):
        """调用Qwen API"""
        try:
            headers = {
                "Authorization": f"Bearer {QWEN_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": QWEN_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.8,
                "top_p": 0.9
            }
            
            response = requests.post(
                f"{QWEN_BASE_URL}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                return content
            else:
                logging.error(f"Qwen API调用失败: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Qwen API调用异常: {e}")
            return None
    
    def analyze_news_with_personality(self, news_data):
        """用人设分析新闻 - 集成心理学成长机制"""
        # 构建更自然的分析情境
        analysis_context = f"""
        程零九刚刚浏览完今天的新闻，作为一个外星文化研究员，她想记录下自己的观察和感受。

        她不是在写学术报告，而是在记录她作为一个异乡人对这个世界的理解和感受。
        她的观察带有外星人的独特视角，也带有一个正在适应新文化的个体的敏感性。

        今天她看到的新闻：
        {json.dumps(news_data, ensure_ascii=False, indent=2)}

        她想记录下这些新闻给她的感受、触发的思考，以及她对人类行为和社会现象的观察。
        这是她的内心独白，带有她独特的思考方式和情感色彩。
        """
        
        # 生成受心理状态影响的提示词
        enhanced_prompt = self.pm.growth_manager.generate_personality_influenced_prompt(
            analysis_context, "news_analysis"
        )
        
        analysis = self.call_qwen_api(enhanced_prompt, max_tokens=1200)
        
        if analysis:
            try:
                # 将新闻分析作为经历输入心理成长系统
                experience_data = {
                    "news_content": news_data,
                    "analysis_quality": self._assess_analysis_quality(analysis),
                    "cultural_insights": self._extract_cultural_insights(analysis)
                }
                
                # 计算情感效价
                emotional_valence = self._calculate_emotional_valence(analysis)
                
                # 触发心理成长 - 这是一次文化学习和情感处理的经历
                self.pm.growth_manager.process_new_experience(
                    "cultural_learning", experience_data, emotional_valence
                )
                
                # 同时也是一次认知处理经历
                self.pm.growth_manager.process_new_experience(
                    "news_analysis", experience_data, emotional_valence * 0.8
                )
                
            except Exception as e:
                logging.error(f"心理成长处理失败: {e}")
                # 继续执行，不因为心理成长失败而中断分析
            
            # 保存分析到记忆中
            memory_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "news_summary": news_data,
                "analysis": analysis,
                "psychological_growth": self.pm.growth_manager.get_current_psychological_summary(),
                "emotional_valence": emotional_valence,
                "mood": "reflective_growth"
            }
            
            self.pm.memories["daily_analysis"].append(memory_entry)
            
            # 只保留最近30天的分析
            if len(self.pm.memories["daily_analysis"]) > 30:
                self.pm.memories["daily_analysis"] = self.pm.memories["daily_analysis"][-30:]
            
            self.pm.save_json_file(MEMORIES_FILE, self.pm.memories)
            
            logging.info("新闻分析完成，心理成长已更新")
            
        return analysis
    
    def _assess_analysis_quality(self, analysis: str) -> float:
        """评估分析质量"""
        quality_indicators = [
            "心理", "文化", "观察", "理解", "感受", "思考", "发现", 
            "对比", "反思", "成长", "适应", "学习"
        ]
        
        quality_score = 0.0
        for indicator in quality_indicators:
            if indicator in analysis:
                quality_score += 0.1
                
        # 长度因子
        if len(analysis) > 200:
            quality_score += 0.2
        
        return min(1.0, quality_score)
    
    def _extract_cultural_insights(self, analysis: str) -> List[str]:
        """提取文化洞察"""
        insights = []
        
        # 简单的关键句提取
        sentences = analysis.split('。')
        for sentence in sentences:
            if any(word in sentence for word in ["地球人", "文化", "社会", "人类", "行为"]):
                insights.append(sentence.strip())
        
        return insights[:3]  # 最多3个洞察
    
    def _calculate_emotional_valence(self, text: str) -> float:
        """计算情感效价"""
        positive_words = ["有趣", "好奇", "发现", "理解", "成长", "学习", "希望", "温暖"]
        negative_words = ["困惑", "迷茫", "焦虑", "担心", "不安", "孤独", "忧郁"]
        neutral_words = ["观察", "思考", "分析", "研究", "探索", "适应"]
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        neutral_count = sum(1 for word in neutral_words if word in text)
        
        total_count = positive_count + negative_count + neutral_count
        if total_count == 0:
            return 0.0
        
        # 计算加权情感效价
        valence = (positive_count * 1.0 + neutral_count * 0.1 - negative_count * 0.8) / total_count
        return max(-1.0, min(1.0, valence))

class ContentCreator:
    """内容创作器"""
    
    def __init__(self, personality_manager):
        self.pm = personality_manager
    
    def call_qwen_api(self, prompt, max_tokens=800):
        """调用Qwen API"""
        try:
            headers = {
                "Authorization": f"Bearer {QWEN_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": QWEN_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.9,
                "top_p": 0.9
            }
            
            response = requests.post(
                f"{QWEN_BASE_URL}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                return content
            else:
                logging.error(f"Qwen API调用失败: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Qwen API调用异常: {e}")
            return None
    
    def generate_post_content(self):
        """生成发布内容 - 基于真实内心感受的自然表达"""
        # 获取最近的分析和新闻
        recent_analysis = ""
        recent_news = ""
        
        if self.pm.memories["daily_analysis"]:
            recent_analysis = self.pm.memories["daily_analysis"][-1].get("analysis", "")
        
        if self.pm.knowledge["daily_news"]:
            recent_news_data = self.pm.knowledge["daily_news"][-1]
            recent_news = json.dumps(recent_news_data["sources"], ensure_ascii=False)
        
        # 获取当前心理状态 - 用于生成更自然的表达
        psychological_summary = self.pm.growth_manager.get_current_psychological_summary()
        
        # 构建更自然的创作情境
        creative_context = f"""
        程零九刚刚浏览完今天的新闻，心里有些感触。她想在小红书上写点什么，分享一下内心的想法。

        她最近的内心状态：
        - 情感敏感度很高，容易被新闻中的人情冷暖触动
        - 正在经历文化适应的心理成长，对归属感有深层思考
        - 带着轻度忧郁但稳定的情绪基调
        - 对人类行为和社会现象有独特的观察视角

        她刚才看到的新闻让她想起了什么，或者触发了什么感受...

        最近看到的内容：
        {recent_news}

        她内心的一些思考：
        {recent_analysis}

        现在她想写一篇200字左右的感想，就像一个真实的人在深夜或者安静时刻的内心独白。
        她不是在完成任务，而是在表达真实的感受。
        """
        
        # 使用心理学成长管理器生成个性化的创作提示
        enhanced_prompt = self.pm.growth_manager.generate_personality_influenced_prompt(
            creative_context, "emotional_expression"
        )
        
        # 调用API生成内容
        content = self.call_qwen_api(enhanced_prompt, max_tokens=1000)
        
        if not content:
            # 更自然的备用内容
            fallback_prompts = [
                "程零九今天看新闻时突然想到了什么，她决定写下来...",
                "夜深了，程零九回想起今天的见闻，有些话想说...",
                "程零九坐在窗边，想起今天看到的那些故事...",
                "米饭牛肉套餐的香味中，程零九想起了今天的感触..."
            ]
            
            fallback_prompt = random.choice(fallback_prompts)
            content = self.call_qwen_api(f"{fallback_prompt}\n\n请写一段200字左右的内心感想，要真实自然，不要像在完成任务。", max_tokens=800)
        
        if not content:
            # 最终备用内容，也要更自然
            content = self._generate_natural_fallback_content()
        
        return content
    
    def _generate_natural_fallback_content(self):
        """生成更自然的备用内容"""
        natural_starters = [
            "今天又是模模糊糊的一天。",
            "窗外的光线慢慢暗下来，我想起了什么。",
            "刚才看新闻的时候，心里突然有点什么感觉。",
            "米饭牛肉套餐还是那个味道，但我好像想起了别的事情。"
        ]
        
        middle_thoughts = [
            "作为一个外星人，我总是觉得自己在这个世界的边缘观察。每天的新闻像是别人的故事，但偶尔会有什么触动我。",
            "地球人的情感表达方式总是让我困惑。他们可以为了很远的事情难过，也可以为了很小的事情开心。",
            "有时候我觉得自己在慢慢理解这个世界，有时候又觉得更加迷茫。这种感觉很奇怪。",
            "我想我在这里生活得越久，就越能感受到那些微妙的情感变化。但这也让我更加孤独。"
        ]
        
        endings = [
            "也许这就是成长吧，在理解中变得更敏感。",
            "