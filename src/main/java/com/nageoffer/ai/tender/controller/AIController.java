package com.nageoffer.ai.tender.controller;

import com.nageoffer.ai.tender.config.response.Response;
import com.nageoffer.ai.tender.service.*;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
public class AIController {

    private final LLMService llmService;
    private final ContentSelectionService contentSelectionService;
    private final DocumentGenerationService documentGenerationService;
    private final TenderDocumentService tenderDocumentService;

    public AIController(LLMService llmService,
                       ContentSelectionService contentSelectionService,
                       DocumentGenerationService documentGenerationService,
                       TenderDocumentService tenderDocumentService) {
        this.llmService = llmService;
        this.contentSelectionService = contentSelectionService;
        this.documentGenerationService = documentGenerationService;
        this.tenderDocumentService = tenderDocumentService;
    }

    /**
     * 同步LLM调用
     */
    @PostMapping("/chat")
    public Response<String> chat(@RequestBody Map<String, String> request) {
        String prompt = request.get("prompt");
        String response = llmService.chat(prompt);
        return Response.success(response);
    }

    /**
     * 流式LLM调用
     */
    @PostMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> streamChat(@RequestBody Map<String, String> request) {
        String prompt = request.get("prompt");
        return llmService.streamChat(prompt);
    }

    /**
     * 内容选择和回答
     */
    @PostMapping("/query")
    public Response<String> processQuery(@RequestBody Map<String, String> request) {
        String userId = request.get("userId");
        String query = request.get("query");
        String response = contentSelectionService.processQuery(userId, query);
        return Response.success(response);
    }

    /**
     * 生成DOCX文档
     */
    @PostMapping("/generate/docx")
    public Response<byte[]> generateDocx(@RequestBody Map<String, String> request) throws Exception {
        String title = request.get("title");
        String content = request.get("content");
        byte[] document = documentGenerationService.generateDocx(title, content);
        return Response.success(document);
    }

    /**
     * 生成PDF文档
     */
    @PostMapping("/generate/pdf")
    public Response<byte[]> generatePdf(@RequestBody Map<String, String> request) throws Exception {
        String title = request.get("title");
        String content = request.get("content");
        byte[] document = documentGenerationService.generatePdf(title, content);
        return Response.success(document);
    }

    /**
     * 生成投标书DOCX
     */
    @PostMapping("/tender/docx")
    public Response<byte[]> generateTenderDocx(@RequestBody Map<String, String> request) throws Exception {
        String userId = request.get("userId");
        String projectDescription = request.get("projectDescription");
        String requirements = request.get("requirements");
        byte[] document = tenderDocumentService.generateTenderDocx(userId, projectDescription, requirements);
        return Response.success(document);
    }

    /**
     * 生成投标书PDF
     */
    @PostMapping("/tender/pdf")
    public Response<byte[]> generateTenderPdf(@RequestBody Map<String, String> request) throws Exception {
        String userId = request.get("userId");
        String projectDescription = request.get("projectDescription");
        String requirements = request.get("requirements");
        byte[] document = tenderDocumentService.generateTenderPdf(userId, projectDescription, requirements);
        return Response.success(document);
    }

    /**
     * 生成投标书文本
     */
    @PostMapping("/tender/text")
    public Response<String> generateTenderText(@RequestBody Map<String, String> request) {
        String userId = request.get("userId");
        String projectDescription = request.get("projectDescription");
        String content = tenderDocumentService.generateTenderText(userId, projectDescription);
        return Response.success(content);
    }
}
