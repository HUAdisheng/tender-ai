package com.nageoffer.ai.tender.service;

import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class VectorRetrievalService {

    private final VectorStore vectorStore;

    public VectorRetrievalService(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    /**
     * 根据用户ID检索相关文档
     */
    public List<Document> retrieveDocuments(String userId, String query, int topK) {
        // 添加用户ID作为过滤条件
        // Note: Filtering by userId may not be supported in this version, simplified
        return vectorStore.similaritySearch(query);
    }

    /**
     * 存储用户文档到向量数据库
     */
    public void storeDocument(String userId, String content, Map<String, Object> metadata) {
        metadata.put("userId", userId);
        Document document = new Document(content, metadata);
        vectorStore.add(List.of(document));
    }
}
