package com.nageoffer.ai.tender.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.HashMap;
import java.util.Map;

@Data
@Configuration
@ConfigurationProperties(prefix = "ai")
public class AIProperties {

    private OpenAI openai = new OpenAI();
    private VectorStore vectorStore = new VectorStore();

    @Data
    public static class OpenAI {
        private String apiKey;
        private String model = "gpt-4";
        private Double temperature = 0.7;
    }

    @Data
    public static class VectorStore {
        private String collectionName = "user_documents";
        private String host = "localhost";
        private Integer port = 8000;
    }
}
