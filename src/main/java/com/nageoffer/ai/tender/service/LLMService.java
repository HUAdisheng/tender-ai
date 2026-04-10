package com.nageoffer.ai.tender.service;

import lombok.RequiredArgsConstructor;
import org.springframework.ai.openai.OpenAiChatClient;
import org.springframework.ai.chat.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.openai.OpenAiChatOptions;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

import java.util.Map;

/**
 * Service for interacting with Large Language Models (LLMs).
 */
@Service
@RequiredArgsConstructor
public class LLMService {

    private final OpenAiChatClient chatModel;

    /**
     * 同步调用LLM
     */
    public String chat(String prompt) {
        Prompt promptObj = new Prompt(prompt);
        ChatResponse response = chatModel.call(promptObj);
        return response.getResult().getOutput().getContent();
    }

    /**
     * 同步调用LLM with options
     */
    public String chat(String prompt, Map<String, Object> options) {
        PromptTemplate template = new PromptTemplate(prompt);
        Prompt promptObj = template.create(options);
        ChatResponse response = chatModel.call(promptObj);
        return response.getResult().getOutput().getContent();
    }

    /**
     * 流式调用LLM
     */
    public Flux<String> streamChat(String prompt) {
        Prompt promptObj = new Prompt(prompt);
        return chatModel.stream(promptObj)
                .map(chatResponse -> chatResponse.getResult().getOutput().getContent());
    }

    /**
     * 流式调用LLM with options
     */
    public Flux<String> streamChat(String prompt, Map<String, Object> options) {
        PromptTemplate template = new PromptTemplate(prompt);
        Prompt promptObj = template.create(options);
        return chatModel.stream(promptObj)
                .map(chatResponse -> chatResponse.getResult().getOutput().getContent());
    }
}
