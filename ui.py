"""
🎨 STREAMLIT DASHBOARD — Trợ lý Tuyển dụng & Sàng lọc CV
Giao diện chat tích hợp hiển thị Waterfall Trace Log từng bước ReAct.
"""

import sys
import os
import json
import time
import streamlit as st

# Thêm src/ vào Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from dotenv import load_dotenv
load_dotenv()

from mcp_server import MCPAcademicServer
from prompts import REACT_AGENT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Trợ lý Tuyển dụng AI",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CUSTOM CSS
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Nền tổng thể ── */
    .stApp { background: #0f1117; }
    section[data-testid="stSidebar"] { background: #161b27; border-right: 1px solid #1e2535; }

    /* ── Header ── */
    .hero-header {
        background: linear-gradient(135deg, #1a1f35 0%, #0f3460 50%, #16213e 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0,120,255,0.15);
    }
    .hero-header h1 { color: #ffffff; font-size: 1.8rem; font-weight: 700; margin: 0; }
    .hero-header p  { color: #8892a4; margin: 6px 0 0 0; font-size: 0.95rem; }

    /* ── Badge provider ── */
    .provider-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 10px;
    }
    .badge-gemini { background: #0d3b7a; color: #60a5fa; border: 1px solid #1d4ed8; }
    .badge-mock   { background: #2d1b4e; color: #c084fc; border: 1px solid #7c3aed; }

    /* ── Chat messages ── */
    .chat-user {
        background: linear-gradient(135deg, #1e3a5f, #1a2744);
        border: 1px solid #2563eb44;
        border-radius: 16px 16px 4px 16px;
        padding: 14px 18px;
        margin: 8px 60px 8px 0;
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .chat-agent {
        background: linear-gradient(135deg, #1a2744, #162035);
        border: 1px solid #334155;
        border-radius: 16px 16px 16px 4px;
        padding: 14px 18px;
        margin: 8px 0 8px 60px;
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .chat-label { font-size: 0.75rem; font-weight: 600; margin-bottom: 6px; }
    .label-user  { color: #60a5fa; }
    .label-agent { color: #34d399; }

    /* ── Trace steps ── */
    .trace-step {
        border-left: 3px solid #334155;
        padding: 10px 16px;
        margin: 6px 0;
        border-radius: 0 10px 10px 0;
        background: #161b27;
        font-size: 0.875rem;
    }
    .trace-thought { border-left-color: #f59e0b; }
    .trace-action  { border-left-color: #3b82f6; }
    .trace-obs     { border-left-color: #10b981; }
    .trace-final   { border-left-color: #a78bfa; }
    .trace-label   { font-weight: 600; font-size: 0.78rem; margin-bottom: 4px; }
    .label-thought { color: #f59e0b; }
    .label-action  { color: #3b82f6; }
    .label-obs     { color: #10b981; }
    .label-final   { color: #a78bfa; }

    /* ── Metric cards ── */
    .metric-card {
        background: #161b27;
        border: 1px solid #1e2535;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #60a5fa; }
    .metric-label { font-size: 0.8rem; color: #64748b; margin-top: 2px; }

    /* ── Job cards sidebar ── */
    .job-card {
        background: #1e2535;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 8px;
        font-size: 0.82rem;
        color: #94a3b8;
    }
    .job-card strong { color: #e2e8f0; font-size: 0.88rem; }
    .job-badge { color: #34d399; font-weight: 600; }

    /* ── Inputs ── */
    .stTextInput input, .stTextArea textarea {
        background: #1e2535 !important;
        border: 1px solid #2d3748 !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s !important;
    }
    .stButton button:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(37,99,235,0.4) !important; }

    /* Ẩn hamburger và footer mặc định */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []          # [{role, content, traces}]
if "provider" not in st.session_state:
    st.session_state.provider = None
if "mcp_server" not in st.session_state:
    st.session_state.mcp_server = None
if "total_calls" not in st.session_state:
    st.session_state.total_calls = 0
if "total_tool_calls" not in st.session_state:
    st.session_state.total_tool_calls = 0

# ==============================================================================
# KHỞI TẠO PROVIDER & MCP SERVER (cache)
# ==============================================================================
@st.cache_resource(show_spinner=False)
def init_agent():
    provider   = get_llm_provider()
    mcp_server = MCPAcademicServer()
    return provider, mcp_server

provider, mcp_server = init_agent()
provider_name = provider.__class__.__name__

# ==============================================================================
# REACT AGENT (chạy từng bước, yield trace)
# ==============================================================================
def run_react_agent_stream(user_query: str):
    """Chạy ReAct loop và trả về danh sách trace steps."""
    tools_list  = mcp_server.list_tools()
    trace_steps = []
    final_answer = ""

    for step in range(1, MAX_ITERATIONS + 1):
        step_start = time.time()
        llm_response = provider.generate_with_tools(
            user_query, tools_list, system_prompt=REACT_AGENT_SYSTEM_PROMPT
        )
        latency = round((time.time() - step_start) * 1000, 1)

        thought = llm_response.get("thought", "Đang suy luận...")
        trace_steps.append({"type": "thought", "step": step, "content": thought, "latency_ms": latency})

        if llm_response.get("type") == "text":
            final_answer = llm_response.get("content", "")
            trace_steps.append({"type": "final", "step": step, "content": final_answer, "latency_ms": latency})
            break

        elif llm_response.get("type") == "tool_call":
            tool_name  = llm_response.get("tool_name", "")
            arguments  = llm_response.get("arguments", {})
            args_str   = json.dumps(arguments, ensure_ascii=False)

            trace_steps.append({
                "type": "action", "step": step,
                "content": f"`{tool_name}({args_str})`",
                "tool_name": tool_name, "latency_ms": latency
            })

            mcp_result = mcp_server.call_tool(tool_name, arguments)
            obs_data   = mcp_result.get("result", {})

            trace_steps.append({
                "type": "obs", "step": step,
                "content": json.dumps(obs_data, ensure_ascii=False, indent=2),
                "status": obs_data.get("status", "")
            })

            st.session_state.total_tool_calls += 1

            # =========================================================
            # BẢN VÁ LỖI ĐA BƯỚC (MULTI-STEP REASONING)
            # Thay vì break, ta nối kết quả tool vào prompt để Gemini suy luận tiếp!
            # =========================================================
            user_query += (
                f"\n\n[KẾT QUẢ TỪ TOOL '{tool_name}']: {json.dumps(obs_data, ensure_ascii=False)}\n"
                f"=> HỆ THỐNG YÊU CẦU: Hãy đọc kết quả trên. Nếu cần sàng lọc CV, hãy so sánh thông tin ứng viên với tiêu chí. "
                f"Nếu đủ điều kiện, hãy tiếp tục gọi tool 'send_interview_notification'. "
                f"Nếu không đủ điều kiện, hoặc nếu đã hoàn tất toàn bộ quy trình, hãy trả lời bằng văn bản (type='text')."
            )

            # (Chặn loop vô hạn nếu đang dùng MockOfflineProvider)
            if "Mock" in provider.__class__.__name__:
                final_answer = f"✅ [Mock Provider] Đã giả lập gọi tool {tool_name}. (Chế độ Mock không hỗ trợ suy luận đa bước liên hoàn)."
                trace_steps.append({"type": "final", "step": step + 1, "content": final_answer})
                break

    st.session_state.total_calls += 1
    return final_answer, trace_steps

# ==============================================================================
# RENDER TRACE LOG
# ==============================================================================
def render_trace(trace_steps: list):
    icons   = {"thought": "🧠", "action": "🛠️", "obs": "👁️", "final": "🏁"}
    labels  = {"thought": "Thought", "action": "Action → Tool Call", "obs": "Observation", "final": "Final Answer"}
    css_cls = {"thought": "trace-thought label-thought",
               "action":  "trace-action  label-action",
               "obs":     "trace-obs     label-obs",
               "final":   "trace-final   label-final"}

    for s in trace_steps:
        t       = s["type"]
        icon    = icons.get(t, "•")
        label   = labels.get(t, t)
        content = s["content"]
        cls     = css_cls.get(t, "")
        latency = f" <span style='color:#475569;font-size:0.72rem'>({s['latency_ms']} ms)</span>" if "latency_ms" in s else ""
        step_n  = s.get("step", "")

        if t == "obs":
            # JSON collapsible
            with st.expander(f"{icon} **Step {step_n} — {label}** (status: {s.get('status','')})", expanded=False):
                st.code(content, language="json")
        else:
            safe_content = content.replace("<", "&lt;").replace(">", "&gt;")
            trace_cls  = cls.split()[0]
            label_cls  = cls.split()[1] if len(cls.split()) > 1 else ""
            st.markdown(f"""
            <div class="trace-step {trace_cls}">
                <div class="trace-label {label_cls}">{icon} Step {step_n} — {label}{latency}</div>
                <div>{safe_content}</div>
            </div>""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown("### 🤝 Recruitment Agent")

    badge_cls  = "badge-gemini" if "Gemini" in provider_name else "badge-mock"
    badge_name = "Gemini API ✓" if "Gemini" in provider_name else "Mock Offline"
    st.markdown(f'<span class="provider-badge {badge_cls}">🔌 {badge_name}</span>', unsafe_allow_html=True)

    st.divider()

    # Metric cards
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{st.session_state.total_calls}</div>
            <div class="metric-label">Lượt chat</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{st.session_state.total_tool_calls}</div>
            <div class="metric-label">Tool calls</div></div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 📂 Vị trí tuyển dụng")

    jobs = [
        ("POS-001", "Software Engineer L3", "3 năm", "25–40M"),
        ("POS-002", "Data Analyst",          "1 năm", "15–25M"),
        ("POS-003", "Backend Engineer L2",   "2 năm", "18–30M"),
        ("POS-004", "Product Manager",       "4 năm", "30–55M"),
    ]
    for pid, pname, exp, salary in jobs:
        st.markdown(f"""<div class="job-card">
            <strong>{pname}</strong><br>
            <span style="color:#6b7280">{pid}</span> &nbsp;•&nbsp;
            <span class="job-badge">≥{exp}</span> &nbsp;•&nbsp;
            <span style="color:#fbbf24">{salary} VNĐ</span>
        </div>""", unsafe_allow_html=True)



    if st.button("🗑️ Xoá lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_calls = 0
        st.session_state.total_tool_calls = 0
        st.rerun()

# ==============================================================================
# MAIN CONTENT
# ==============================================================================
st.markdown("""
<div class="hero-header">
    <h1>🤝 Trợ lý Tuyển dụng & Sàng lọc CV</h1>
    <p>ReAct Agent tích hợp MCP Server — Tra cứu tiêu chí tuyển dụng & Gửi thông báo phỏng vấn</p>
</div>
""", unsafe_allow_html=True)

# Tabs: Chat | Trace Log
tab_chat, tab_trace = st.tabs(["💬 Chat", "🔍 Waterfall Trace Log"])

# ── Tab Chat ──────────────────────────────────────────────────────────────────
with tab_chat:
    # Hiển thị lịch sử hội thoại
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""<div class="chat-user">
                <div class="chat-label label-user">👤 Bạn</div>
                {msg["content"]}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="chat-agent">
                <div class="chat-label label-agent">🤖 Agent</div>
                {msg["content"]}
            </div>""", unsafe_allow_html=True)

    # Input
    user_input = st.chat_input(
        "Nhập câu hỏi về tuyển dụng... (VD: Tiêu chí vị trí Data Analyst?)",
    )

    if user_input and user_input.strip():
        # Hiển thị tin nhắn user
        st.markdown(f"""<div class="chat-user">
            <div class="chat-label label-user">👤 Bạn</div>
            {user_input}
        </div>""", unsafe_allow_html=True)

        # Chạy Agent với spinner
        with st.spinner("🧠 Agent đang suy luận..."):
            final_answer, trace_steps = run_react_agent_stream(user_input)

        # Hiển thị câu trả lời
        st.markdown(f"""<div class="chat-agent">
            <div class="chat-label label-agent">🤖 Agent</div>
            {final_answer}
        </div>""", unsafe_allow_html=True)

        # Lưu vào session
        st.session_state.messages.append({"role": "user",  "content": user_input})
        st.session_state.messages.append({"role": "agent", "content": final_answer, "traces": trace_steps})
        st.rerun()

# ── Tab Trace Log ──────────────────────────────────────────────────────────────
with tab_trace:
    agent_msgs = [m for m in st.session_state.messages if m["role"] == "agent" and m.get("traces")]

    if not agent_msgs:
        st.info("💡 Chưa có trace log. Hãy gửi một câu hỏi ở tab **Chat** để xem luồng suy luận ReAct!", icon="ℹ️")
    else:
        # Chọn lượt chat để xem trace
        options = {f"Lượt {i+1}: {m['content'][:60]}...": m for i, m in enumerate(agent_msgs)}
        selected_label = st.selectbox("🔎 Chọn lượt chat để xem Waterfall Trace:", list(options.keys()))
        selected_msg   = options[selected_label]

        st.markdown("---")
        st.markdown("#### 🌊 Waterfall Trace Log — Luồng suy luận ReAct")
        render_trace(selected_msg["traces"])
