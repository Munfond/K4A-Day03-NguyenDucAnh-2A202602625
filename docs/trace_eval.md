# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Đức Anh  
> **Mã Sinh Viên / Mã Học viên:** 2A202602625  
> **Chủ đề Lựa chọn:** Trợ lý Tuyển dụng & Sàng lọc CV: Tra cứu tiêu chí tuyển dụng vị trí và gửi thông báo lịch phỏng vấn.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **5** / 5 | ✅ **Điểm tối đa.** Bài toán yêu cầu chuỗi suy luận nhiều bước rõ ràng và nối tiếp nhau: **(1)** Nhận yêu cầu tìm ứng viên → **(2)** Gọi tool tra cứu tiêu chí vị trí (kỹ năng, kinh nghiệm, bằng cấp yêu cầu) → **(3)** Phân tích & so sánh thông tin CV ứng viên với tiêu chí → **(4)** Đưa ra phán quyết sàng lọc (đạt / không đạt) → **(5)** Nếu đạt, gọi tool gửi thông báo lịch phỏng vấn. Agent không thể bỏ qua bất kỳ bước nào mà không ảnh hưởng đến kết quả cuối. |
| **2. Tool Interaction** | **5** / 5 | ✅ **Điểm tối đa.** Hệ thống bắt buộc phải tương tác với ít nhất **2 công cụ ngoài** qua MCP Server: **(a)** Tool `get_job_criteria` — tra cứu tiêu chí tuyển dụng từ CSDL nhân sự (yêu cầu kỹ năng, kinh nghiệm, mức lương...); **(b)** Tool `send_interview_notification` — gửi email/thông báo lịch phỏng vấn đến ứng viên. Không có tool nào, Agent chỉ là chatbot thông thường, không thể hoàn thành bài toán. |
| **3. Dynamic Decision** | **4** / 5 | ✅ **Điểm cao.** Quyết định của Agent ở mỗi bước phụ thuộc hoàn toàn vào kết quả quan sát bước trước: nếu tool `get_job_criteria` trả về *"vị trí không tồn tại"* → Agent dừng và báo lỗi (không gửi thông báo); nếu CV ứng viên không đủ điểm kinh nghiệm → Agent từ chối thay vì mời phỏng vấn. Trừ 1 điểm vì luồng rẽ nhánh chưa quá phức tạp (chủ yếu là Đạt/Không đạt, chưa có nhiều kịch bản trung gian). |
| **4. Long Horizon Goal** | **4** / 5 | ✅ **Điểm cao.** Agent phải duy trì ngữ cảnh xuyên suốt toàn bộ phiên làm việc: ghi nhớ *vị trí tuyển dụng đang xét*, *tiêu chí đã tra cứu*, *danh sách ứng viên đã sàng lọc* qua nhiều lượt gọi tool liên tiếp. Trong kịch bản sàng lọc nhiều CV cùng lúc, Agent phải giữ mục tiêu "hoàn thành danh sách ứng viên đủ điều kiện" mà không bị lạc hướng. Trừ 1 điểm vì mỗi phiên tuyển dụng thường có thời gian xử lý không quá dài. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | 🏆 *Tổng điểm **18/20 > 12/20**: Bài toán **RẤT PHÙ HỢP** triển khai Agentic System. Đây là use-case lý tưởng với đầy đủ đặc trưng: chuỗi suy luận đa bước, phụ thuộc tool ngoài, quyết định động theo context và mục tiêu dài hạn.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "tool_name": "academic_query",
    "arguments": {
      "student_id": "SV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026001",
      "data": {
        "full_name": "Nguyễn Văn An",
        "gpa": 3.85
      }
    },
    "latency_ms": 120.5
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ ] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** ___ / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** ___ lượt.
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
