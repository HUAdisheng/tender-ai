package com.nageoffer.ai.tender.service;

import org.springframework.ai.document.Document;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class ContentSelectionService {

    private final LLMService llmService;
    private final VectorRetrievalService vectorRetrievalService;

    public ContentSelectionService(LLMService llmService, VectorRetrievalService vectorRetrievalService) {
        this.llmService = llmService;
        this.vectorRetrievalService = vectorRetrievalService;
    }

    /**
     * 根据用户查询选择内容类型并生成回答
     */
    public String processQuery(String userId, String query) {
        // 首先检索相关文档
        List<Document> documents = vectorRetrievalService.retrieveDocuments(userId, query, 5);

        if (documents.isEmpty()) {
            // 没有相关文档，生成新内容
            return generateContent(query);
        } else {
            // 有相关文档，基于知识回答
            return answerFromKnowledge(query, documents);
        }
    }

    /**
     * 基于数据库知识回答
     */
    private String answerFromKnowledge(String query, List<Document> documents) {
        StringBuilder context = new StringBuilder();
        for (Document doc : documents) {
            context.append(doc.getContent()).append("\n");
        }

        String prompt = """
                基于以下上下文信息回答用户的问题：
                上下文：{context}
                
                问题：{query}
                
                请提供准确、相关的回答。
                """;

        Map<String, Object> params = Map.of(
                "context", context.toString(),
                "query", query
        );

        return llmService.chat(prompt, params);
    }

    /**
     * 生成新内容
     */
    private String generateContent(String query) {
        String prompt = """
                请根据以下要求生成内容：
                要求：{query}
                
                生成高质量、相关的内容。
                """;

        Map<String, Object> params = Map.of("query", query);
        return llmService.chat(prompt, params);
    }
}
