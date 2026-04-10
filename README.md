# Tender AI - AI-Powered Tender Document Generation System

这是一个基于Spring Boot和Spring AI的AI基础设施项目，专门用于生成投标书和其他文档。

## 功能特性

1. **LLM访问接口**
   - 支持同步和流式调用
   - 集成OpenAI GPT模型

2. **向量数据库检索**
   - 根据用户ID检索个人上传的内容
   - 使用ChromaDB作为向量存储

3. **智能内容选择**
   - 根据用户查询自动选择回答数据库知识或生成新内容

4. **文档生成**
   - 支持生成DOCX和PDF格式文档
   - 使用Apache POI和iText库

5. **投标书生成**
   - 专门的投标书生成接口
   - 基于用户历史数据和项目要求生成专业投标书

## 技术栈

- **框架**: Spring Boot 3.2.0
- **AI**: Spring AI 1.0.0-M4
- **数据库**: H2 (内存数据库)
- **向量存储**: ChromaDB
- **文档生成**: Apache POI (DOCX), iText (PDF)

## 项目结构

```
tender-ai/
├── src/main/java/com/nageoffer/ai/tender/
│   ├── TenderAiApplication.java          # 主应用类
│   ├── config/
│   │   └── AIProperties.java             # AI配置属性
│   ├── controller/
│   │   └── AIController.java             # REST API控制器
│   └── service/
│       ├── LLMService.java               # LLM服务
│       ├── VectorRetrievalService.java   # 向量检索服务
│       ├── ContentSelectionService.java  # 内容选择服务
│       ├── DocumentGenerationService.java # 文档生成服务
│       └── TenderDocumentService.java    # 投标书服务
├── src/main/resources/
│   └── application.yml                   # 配置文件
└── pom.xml                               # Maven配置
```

## API接口

### LLM接口
- `POST /api/ai/chat` - 同步聊天
- `POST /api/ai/chat/stream` - 流式聊天

### 内容查询
- `POST /api/ai/query` - 智能内容选择和回答

### 文档生成
- `POST /api/ai/generate/docx` - 生成DOCX文档
- `POST /api/ai/generate/pdf` - 生成PDF文档

### 投标书生成
- `POST /api/ai/tender/docx` - 生成投标书DOCX
- `POST /api/ai/tender/pdf` - 生成投标书PDF
- `POST /api/ai/tender/text` - 生成投标书文本

## 配置说明

在`application.yml`中配置：
- OpenAI API Key
- ChromaDB连接信息
- 模型参数

## 运行项目

1. 确保安装Java 17和Maven
2. 设置环境变量`OPENAI_API_KEY`
3. 启动ChromaDB服务（如果使用）
4. 运行命令：
   ```bash
   mvn spring-boot:run
   ```

## 使用示例

### 生成投标书
```bash
curl -X POST http://localhost:8080/api/ai/tender/text \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "projectDescription": "软件开发项目"
  }'
```

项目已完成所有要求的功能实现。
