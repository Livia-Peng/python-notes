from docx import Document
import re
import json
import requests
from typing import List, Dict

class DocProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    # 文档解析
    def parse_docx(self, file_path: str) -> List[str]:
        """提取文档段落并过滤空行"""
        doc = Document(file_path)
        return [para.text.strip() for para in doc.paragraphs if para.text.strip()]

    # 数据清洗
    def clean_text(self, text: str) -> str:
        """多级文本清洗"""
        # 去除特殊字符
        text = re.sub(r'[^\w\u4e00-\u9fa5\s.,;:!?()-]', '', text)
        # 合并多余空格
        text = re.sub(r'\s+', ' ', text)
        # 规范标点
        text = re.sub(r'([,.;:])\s*', r'\1 ', text)
        # 更多场景化需求
        return text.strip()

    # 文本切片
    def chunk_text(self, paragraphs: List[str], max_len: int = 500) -> List[Dict]:
        """智能文本分块"""
        chunks = []
        current_chunk = []
        current_length = 0

        for para in paragraphs:
            cleaned = self.clean_text(para)
            if len(cleaned) + current_length > max_len and current_chunk:
                chunks.append({
                    "content": " ".join(current_chunk),
                    "length": current_length,
                    "labels": self._generate_labels(current_chunk)
                })
                current_chunk = []
                current_length = 0
                
            current_chunk.append(cleaned)
            current_length += len(cleaned)

        if current_chunk:
            chunks.append({
                "content": " ".join(current_chunk),
                "length": current_length,
                "labels": self._generate_labels(current_chunk)
            })
        return chunks

    # 自动标注
    def _generate_labels(self, chunk: List[str]) -> List[str]:
        """基于规则的自动标注"""
        labels = set()
        text = " ".join(chunk).lower()
        
        # 关键信息类型检测
        patterns = {
            "contact_info": r"\b(电话|邮箱|地址|联系方式)\b",
            "financial_data": r"\b(金额|成本|利润|预算)\b",
            "technical_term": r"\b(API|深度学习|模型|算法)\b",
            "sensitive_info": r"\b(身份证|密码|银行卡)\b"
        }

        for label, pattern in patterns.items():
            if re.search(pattern, text):
                labels.add(label)

        return list(labels)

    # 模型调用
    def query_model(self, prompt: str, max_tokens: int = 800) -> str:
        """调用DeepSeek R1模型"""
        payload = {
            "model": "deepseek-r1",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(
                # "https://api.deepseek.com/v1/chat/completions",
                "https://api.lkeap.cloud.tencent.com/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"API调用失败: {str(e)}"

    # 完整流程
    def process_document(self, file_path: str, query: str) -> Dict:
        # 数据解析和处理
        paragraphs = self.parse_docx(file_path)
        # print("paragraphs:\n", paragraphs, "\n")
        chunks = self.chunk_text(paragraphs)
        # print("chunks:\n", chunks, "\n")        

        # 构建上下文
        context = "\n".join([f"[片段{i+1}] {chunk['content']}" 
                           for i, chunk in enumerate(chunks[:3])])  # 取前3个片段
        
        # print("context:\n", context, "\n")
    
        # 构建增强prompt
        enhanced_prompt = f"""请基于以下文档片段回答问题：
        {context}
        
        问题：{query}
        
        要求：
        1. 使用中文回答
        2. 引用时标注片段编号
        3. 如信息不足请说明
        """
        
        # 调用模型
        response = self.query_model(enhanced_prompt)
        
        return {
            "chunks": chunks,
            "response": response,
            "stats": {
                "total_paragraphs": len(paragraphs),
                "total_chunks": len(chunks),
                "avg_chunk_length": sum(c['length'] for c in chunks) // len(chunks)
            }
        }

if __name__ == "__main__":
    # 配置参数
    API_KEY = "xxx"
    DOC_PATH = "/Users/livia/Documents/github/python-notes/files/doc.docx"

    # 输入问题
    # query = input()
    query = "请用3句话总结文档中提到的关键点"
    
    # 执行处理
    processor = DocProcessor(API_KEY)
    result = processor.process_document(DOC_PATH, query)
    
    # 保存结果
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("处理完成！结果已保存至output.json")
    print("模型回复：")
    print(result["response"])
