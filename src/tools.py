"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer
phục vụ cho MCP Server — Chủ đề: Trợ lý Tuyển dụng & Sàng lọc CV.
"""

import json
from datetime import datetime
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA
# ==============================================================================

TOOLS_SCHEMA = [
    # --------------------------------------------------------------------------
    # Tool 1: Tra cứu tiêu chí tuyển dụng theo mã hoặc tên vị trí
    # --------------------------------------------------------------------------
    {
        "name": "get_job_criteria",
        "description": (
            "Tra cứu tiêu chí tuyển dụng chi tiết của một vị trí công việc "
            "bao gồm: yêu cầu kỹ năng, số năm kinh nghiệm, bằng cấp tối thiểu "
            "và mức lương tham chiếu. Dùng khi cần đánh giá mức độ phù hợp của ứng viên."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "position_name": {
                    "type": "string",
                    "description": (
                        "Tên vị trí tuyển dụng cần tra cứu "
                        "(ví dụ: 'Software Engineer L3', 'Data Analyst', 'Backend Engineer L2')"
                    )
                },
                "position_id": {
                    "type": "string",
                    "description": (
                        "Mã định danh vị trí tuyển dụng (ví dụ: 'POS-001'). "
                        "Không bắt buộc nếu đã cung cấp position_name."
                    )
                }
            },
            "required": ["position_name"]
        }
    },

    # --------------------------------------------------------------------------
    # Tool 2: Gửi thông báo mời phỏng vấn đến ứng viên
    # --------------------------------------------------------------------------
    {
        "name": "send_interview_notification",
        "description": (
            "Gửi email thông báo mời phỏng vấn chính thức đến ứng viên đã vượt qua "
            "vòng sàng lọc CV. Thông báo bao gồm: tên ứng viên, vị trí ứng tuyển, "
            "thời gian và hình thức phỏng vấn."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_name": {
                    "type": "string",
                    "description": "Họ và tên đầy đủ của ứng viên (ví dụ: 'Trần Thị Mai')"
                },
                "candidate_email": {
                    "type": "string",
                    "description": "Địa chỉ email của ứng viên (ví dụ: 'mai.tt@email.com')"
                },
                "position_name": {
                    "type": "string",
                    "description": "Tên vị trí ứng viên ứng tuyển (ví dụ: 'Data Analyst')"
                },
                "interview_datetime": {
                    "type": "string",
                    "description": (
                        "Thời gian phỏng vấn theo định dạng 'HH:MM DD/MM/YYYY' "
                        "(ví dụ: '10:00 20/09/2026')"
                    )
                },
                "interview_format": {
                    "type": "string",
                    "description": (
                        "Hình thức phỏng vấn: 'online' (Google Meet) hoặc 'offline' (tại văn phòng). "
                        "Mặc định là 'online' nếu không chỉ định."
                    ),
                    "enum": ["online", "offline"]
                }
            },
            "required": ["candidate_name", "candidate_email", "position_name", "interview_datetime"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

# Cơ sở dữ liệu mô phỏng tiêu chí tuyển dụng
JOB_DATABASE: Dict[str, Dict[str, Any]] = {
    "software engineer l3": {
        "position_id": "POS-001",
        "position_name": "Software Engineer L3",
        "department": "Engineering",
        "required_skills": ["Python", "Java hoặc Go", "RESTful API", "Docker", "SQL"],
        "min_experience_years": 3,
        "min_education": "Đại học CNTT hoặc ngành liên quan",
        "nice_to_have": ["Kubernetes", "AWS/GCP", "Microservices"],
        "salary_range_vnd": "25.000.000 – 40.000.000",
        "headcount": 2
    },
    "data analyst": {
        "position_id": "POS-002",
        "position_name": "Data Analyst",
        "department": "Business Intelligence",
        "required_skills": ["SQL", "Python (pandas, matplotlib)", "Power BI hoặc Tableau", "Excel nâng cao"],
        "min_experience_years": 1,
        "min_education": "Đại học Thống kê, CNTT, Kinh tế hoặc ngành liên quan",
        "nice_to_have": ["Machine Learning cơ bản", "Spark", "Looker"],
        "salary_range_vnd": "15.000.000 – 25.000.000",
        "headcount": 3
    },
    "backend engineer l2": {
        "position_id": "POS-003",
        "position_name": "Backend Engineer L2",
        "department": "Engineering",
        "required_skills": ["Python hoặc Node.js", "REST API", "PostgreSQL hoặc MySQL", "Git"],
        "min_experience_years": 2,
        "min_education": "Cao đẳng hoặc Đại học CNTT",
        "nice_to_have": ["Redis", "RabbitMQ", "CI/CD"],
        "salary_range_vnd": "18.000.000 – 30.000.000",
        "headcount": 4
    },
    "product manager": {
        "position_id": "POS-004",
        "position_name": "Product Manager",
        "department": "Product",
        "required_skills": ["Quản lý roadmap sản phẩm", "Phân tích dữ liệu người dùng", "Agile/Scrum", "Viết PRD"],
        "min_experience_years": 4,
        "min_education": "Đại học Kinh tế, CNTT hoặc ngành liên quan",
        "nice_to_have": ["Technical background", "A/B Testing", "Figma"],
        "salary_range_vnd": "30.000.000 – 55.000.000",
        "headcount": 1
    }
}


def execute_get_job_criteria(position_name: str, position_id: str = None) -> str:
    """Tra cứu tiêu chí tuyển dụng theo tên vị trí"""
    key = position_name.strip().lower()

    # Tìm kiếm linh hoạt theo từ khóa
    matched = None
    for db_key, data in JOB_DATABASE.items():
        if key in db_key or db_key in key:
            matched = data
            break

    # Tìm theo position_id nếu không khớp tên
    if not matched and position_id:
        for data in JOB_DATABASE.values():
            if data.get("position_id", "").upper() == position_id.strip().upper():
                matched = data
                break

    if matched:
        return json.dumps({
            "status": "SUCCESS",
            "position_id": matched["position_id"],
            "position_name": matched["position_name"],
            "data": {
                "department": matched["department"],
                "required_skills": matched["required_skills"],
                "min_experience_years": matched["min_experience_years"],
                "min_education": matched["min_education"],
                "nice_to_have": matched["nice_to_have"],
                "salary_range_vnd": matched["salary_range_vnd"],
                "headcount": matched["headcount"]
            }
        }, ensure_ascii=False, indent=2)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": (
                f"Không tìm thấy tiêu chí tuyển dụng cho vị trí '{position_name}'. "
                "Vui lòng kiểm tra lại tên vị trí hoặc liên hệ HR để được hỗ trợ."
            )
        }, ensure_ascii=False)


def execute_send_interview_notification(
    candidate_name: str,
    candidate_email: str,
    position_name: str,
    interview_datetime: str,
    interview_format: str = "online"
) -> str:
    """Gửi thông báo mời phỏng vấn đến ứng viên"""
    # Tạo mã xác nhận giả lập
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    notification_id = f"NTF-{timestamp}-{candidate_email.split('@')[0].upper()[:6]}"

    location_info = (
        "Link Google Meet: meet.google.com/abc-defg-hij"
        if interview_format == "online"
        else "Địa điểm: Tầng 12, Tòa nhà Innovation Hub, 458 Minh Khai, Hà Nội"
    )

    return json.dumps({
        "status": "SUCCESS",
        "notification_id": notification_id,
        "recipient": {
            "name": candidate_name,
            "email": candidate_email
        },
        "interview_details": {
            "position": position_name,
            "datetime": interview_datetime,
            "format": interview_format,
            "location": location_info
        },
        "message": (
            f"✅ Đã gửi email mời phỏng vấn thành công đến {candidate_name} "
            f"({candidate_email}) cho vị trí '{position_name}' "
            f"vào lúc {interview_datetime} — Hình thức: {interview_format.upper()}."
        )
    }, ensure_ascii=False, indent=2)


# ==============================================================================
# 3. TOOL ROUTER — ÁNH XẠ TÊN TOOL → HÀM THỰC THI
# ==============================================================================

TOOL_ROUTER = {
    "get_job_criteria": execute_get_job_criteria,
    "send_interview_notification": execute_send_interview_notification
}


def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool theo tên và tham số"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except TypeError as e:
            return json.dumps({
                "status": "ARGUMENT_ERROR",
                "error": f"Tham số không hợp lệ cho tool '{tool_name}': {str(e)}"
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "status": "EXECUTION_ERROR",
                "error": str(e)
            }, ensure_ascii=False)
    return json.dumps({
        "status": "UNKNOWN_TOOL",
        "error": f"Tool '{tool_name}' không tồn tại trong hệ thống!"
    }, ensure_ascii=False)
