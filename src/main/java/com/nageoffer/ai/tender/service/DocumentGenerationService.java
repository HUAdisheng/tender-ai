package com.nageoffer.ai.tender.service;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;
import org.apache.poi.xwpf.usermodel.XWPFRun;
import org.springframework.stereotype.Service;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Paragraph;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

@Service
public class DocumentGenerationService {

    /**
     * 生成DOCX文档
     */
    public byte[] generateDocx(String title, String content) throws IOException {
        try (XWPFDocument document = new XWPFDocument();
             ByteArrayOutputStream out = new ByteArrayOutputStream()) {

            // 添加标题
            XWPFParagraph titleParagraph = document.createParagraph();
            XWPFRun titleRun = titleParagraph.createRun();
            titleRun.setText(title);
            titleRun.setBold(true);
            titleRun.setFontSize(16);

            // 添加内容
            XWPFParagraph contentParagraph = document.createParagraph();
            XWPFRun contentRun = contentParagraph.createRun();
            contentRun.setText(content);

            document.write(out);
            return out.toByteArray();
        }
    }

    /**
     * 生成PDF文档
     */
    public byte[] generatePdf(String title, String content) throws IOException {
        try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            PdfWriter writer = new PdfWriter(out);
            PdfDocument pdf = new PdfDocument(writer);
            Document document = new Document(pdf);

            // 添加标题
            document.add(new Paragraph(title).setBold().setFontSize(16));

            // 添加内容
            document.add(new Paragraph(content));

            document.close();
            return out.toByteArray();
        }
    }
}
