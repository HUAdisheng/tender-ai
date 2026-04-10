package com.nageoffer.ai.tender.service;

import org.springframework.ai.document.Document;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class TenderDocumentService {

    private final LLMService llmService;
    private final VectorRetrievalService vectorRetrievalService;
    private final DocumentGenerationService documentGenerationService;

    public TenderDocumentService(LLMService llmService,
                                VectorRetrievalService vectorRetrievalService,
                                DocumentGenerationService documentGenerationService) {
        this.llmService = llmService;
        this.vectorRetrievalService = vectorRetrievalService;
        this.documentGenerationService = documentGenerationService;
    }

    /**
     * 生成投标书文本内容
     */
    public String generateTenderContent(String userId, String projectDescription, String requirements) {
        // 检索用户相关文档作为上下文
        List<Document> userDocs = vectorRetrievalService.retrieveDocuments(userId, projectDescription, 10);

        StringBuilder context = new StringBuilder();
        for (Document doc : userDocs) {
            context.append(doc.getContent()).append("\n");
        }

        String prompt = """
                基于以下用户信息和项目要求，生成一份专业的投标书内容：
                
                用户历史信息：
                {context}
                
                项目描述：{projectDescription}
                具体要求：{requirements}
                
                请生成包含以下部分的投标书：
                1. 项目理解与分析
                2. 技术方案
                3. 实施计划
                4. 团队介绍
                5. 报价与优势
                6. 承诺与保证
                
                确保内容专业、详细、有说服力。
                """;

        Map<String, Object> params = Map.of(
                "context", context.toString(),
                "projectDescription", projectDescription,
                "requirements", requirements
        );

        return llmService.chat(prompt, params);
    }

    /**
     * 生成投标书DOCX文档
     */
    public byte[] generateTenderDocx(String userId, String projectDescription, String requirements) throws Exception {
        String content = generateTenderContent(userId, projectDescription, requirements);
        return documentGenerationService.generateDocx("投标书 - " + projectDescription, content);
    }

    /**
     * 生成投标书PDF文档
     */
    public byte[] generateTenderPdf(String userId, String projectDescription, String requirements) throws Exception {
        String content = generateTenderContent(userId, projectDescription, requirements);
        return documentGenerationService.generatePdf("投标书 - " + projectDescription, content);
    }

    /**
     * 生成投标书文本（简化版）
     */
    public String generateTenderText(String userId, String projectDescription) {
        List<Document> userDocs = vectorRetrievalService.retrieveDocuments(userId, projectDescription, 5);

        StringBuilder context = new StringBuilder();
        for (Document doc : userDocs) {
            context.append(doc.getContent()).append("\n");
        }

        String prompt = """
                基于用户信息生成投标书文本：
                
                用户信息：{context}
                项目：{projectDescription}
                
                生成简洁的投标书文本。
                """;

        Map<String, Object> params = Map.of(
                "context", context.toString(),
                "projectDescription", projectDescription
        );

        return llmService.chat(prompt, params);
    }
}
