import streamlit as st
import pandas as pd

# --- 초기 설정 ---
st.set_page_config(page_title="기어 & 역학 계산기", layout="centered")
st.markdown("""
# ⚙️ **기어 & 기초 역학 계산기**
> 직관적인 인터페이스로 기계공학과 물리 개념을 함께 학습하세요.
""")

# --- 계산 로그 초기화 ---
if "gear_logs" not in st.session_state:
    st.session_state.gear_logs = []
if "physics_logs" not in st.session_state:
    st.session_state.physics_logs = []

# --- 사이드바 메뉴 ---
menu = st.sidebar.selectbox("📂 계산기 선택", (
    "기어비 계산기",
    "등가속도 운동",
    "자유낙하 / 낙하",
    "뉴턴의 운동 법칙",
    "운동 에너지 & 위치 에너지",
    "충돌과 운동량 보존"
))

# --- 기어 계산기 ---
if menu == "기어비 계산기":
    st.subheader("🛠️ 기어 계산기")
    col1, col2 = st.columns(2)
    with col1:
        driver_teeth = st.number_input("구동 기어 톱니 수", min_value=1)
        input_rpm = st.number_input("입력 속도 (RPM)", min_value=0.0)
    with col2:
        driven_teeth = st.number_input("종속 기어 톱니 수", min_value=1)
        input_torque = st.number_input("입력 토크 (N·m)", min_value=0.0)

    if st.button("🧮 계산하기"):
        gear_ratio = driven_teeth / driver_teeth
        output_rpm = input_rpm / gear_ratio
        output_torque = input_torque * gear_ratio

        result = {
            "계산기": "기어비 계산기",
            "입력 RPM": input_rpm,
            "입력 토크 (N·m)": input_torque,
            "구동 톱니 수": driver_teeth,
            "종속 톱니 수": driven_teeth,
            "기어비": round(gear_ratio, 3),
            "출력 RPM": round(output_rpm, 2),
            "출력 토크 (N·m)": round(output_torque, 2)
        }
        st.session_state.gear_logs.append(result)
        st.session_state.physics_logs.append(result)

        st.success(f"✅ 출력 속도: **{output_rpm:.2f} RPM**")
        st.success(f"✅ 출력 토크: **{output_torque:.2f} N·m**")

    with st.expander("📘 이론 요약 노트"):
        st.markdown("""
        - **기어비** = 종속 기어 톱니 수 / 구동 기어 톱니 수
        - **출력 속도** = 입력 속도 / 기어비
        - **출력 토크** = 입력 토크 × 기어비
        """)

# --- 등가속도 운동 ---
elif menu == "등가속도 운동":
    st.subheader("🏃 등가속도 운동 계산기")
    v0 = st.number_input("초기 속도 v₀ (m/s)", value=0.0)
    a = st.number_input("가속도 a (m/s²)")
    t = st.number_input("시간 t (s)", min_value=0.0, value=0.0)

    v = v0 + a * t
    s = v0 * t + 0.5 * a * t**2

    st.success(f"✅ 최종 속도: **{v:.2f} m/s**")
    st.success(f"✅ 이동 거리: **{s:.2f} m**")

    st.session_state.physics_logs.append({
        "계산기": "등가속도 운동",
        "초기 속도 (m/s)": v0,
        "가속도 (m/s²)": a,
        "시간 (s)": t,
        "최종 속도 (m/s)": v,
        "이동 거리 (m)": s
    })

    with st.expander("📘 이론 요약 노트"):
        st.markdown("""
        - **v = v₀ + at**
        - **s = v₀t + ½at²**
        - **v² = v₀² + 2as**
        - 감속 운동도 포함됨 (a < 0)
        """)

# --- 자유낙하 ---
elif menu == "자유낙하 / 낙하":
    st.subheader("🪂 자유낙하 계산기")
    h = st.number_input("높이 h (m)", min_value=0.0)
    g = 9.8
    t = (2 * h / g) ** 0.5
    v = g * t
    st.success(f"✅ 낙하 시간: **{t:.2f} s**")
    st.success(f"✅ 충돌 속도: **{v:.2f} m/s**")

    st.session_state.physics_logs.append({
        "계산기": "자유낙하",
        "높이 (m)": h,
        "중력가속도 (m/s²)": g,
        "낙하 시간 (s)": t,
        "충돌 속도 (m/s)": v
    })

    with st.expander("📘 이론 요약 노트"):
        st.markdown("""
        - **t = √(2h/g)**
        - **v = gt**
        - 공기저항 무시
        """)

# --- 뉴턴의 운동 법칙 ---
elif menu == "뉴턴의 운동 법칙":
    st.subheader("🧲 뉴턴의 제2법칙 계산기")
    m = st.number_input("질량 m (kg)", min_value=0.0)
    a = st.number_input("가속도 a (m/s²)")
    F = m * a
    st.success(f"✅ 힘 F = **{F:.2f} N**")

    st.session_state.physics_logs.append({
        "계산기": "뉴턴 법칙",
        "질량 (kg)": m,
        "가속도 (m/s²)": a,
        "힘 F (N)": F
    })

    with st.expander("📘 이론 요약 노트"):
        st.markdown("- **F = ma**")

# --- 에너지 계산기 ---
elif menu == "운동 에너지 & 위치 에너지":
    st.subheader("⚡ 에너지 계산기")
    m = st.number_input("질량 m (kg)", min_value=0.0)
    v = st.number_input("속도 v (m/s)", min_value=0.0)
    h = st.number_input("높이 h (m)", min_value=0.0)
    KE = 0.5 * m * v**2
    PE = m * 9.8 * h
    st.success(f"✅ 운동 에너지: **{KE:.2f} J**")
    st.success(f"✅ 위치 에너지: **{PE:.2f} J**")

    st.session_state.physics_logs.append({
        "계산기": "에너지",
        "질량 (kg)": m,
        "속도 (m/s)": v,
        "높이 (m)": h,
        "운동 에너지 (J)": KE,
        "위치 에너지 (J)": PE
    })

    with st.expander("📘 이론 요약 노트"):
        st.markdown("""
        - **운동 에너지**: KE = ½mv²
        - **위치 에너지**: PE = mgh
        - g = 9.8 m/s²
        - 음수 입력은 방지되어 있습니다.
        """)

# --- 운동량 보존 ---
elif menu == "충돌과 운동량 보존":
    st.subheader("💥 운동량 보존 계산기")
    m1 = st.number_input("물체 1의 질량 (kg)", min_value=0.0)
    v1 = st.number_input("물체 1의 속도 (m/s)")
    m2 = st.number_input("물체 2의 질량 (kg)", min_value=0.0)
    v2 = st.number_input("물체 2의 속도 (m/s)")

    if m1 + m2 == 0:
        st.error("❌ 두 물체의 질량이 모두 0일 수 없습니다.")
    else:
        vf = (m1 * v1 + m2 * v2) / (m1 + m2)
        st.success(f"✅ 충돌 후 속도 (탄성 충돌 가정): **{vf:.2f} m/s**")
        st.session_state.physics_logs.append({
            "계산기": "운동량 보존",
            "물체1 질량 (kg)": m1,
            "물체1 속도 (m/s)": v1,
            "물체2 질량 (kg)": m2,
            "물체2 속도 (m/s)": v2,
            "충돌 후 속도 (m/s)": vf
        })

    with st.expander("📘 이론 요약 노트"):
        st.markdown("""
        - 총 운동량 보존: m₁v₁ + m₂v₂ = (m₁ + m₂)v
        - 외력이 없을 때 운동량은 보존됩니다.
        - 방향이 다를 경우 속도는 음수일 수 있습니다.
        """)

# --- 공통 로그 보기 ---
st.sidebar.markdown("---")
if st.sidebar.button("📊 전체 계산 로그 보기"):
    st.markdown("## 📚 전체 계산 로그")
    if st.session_state.physics_logs:
        df = pd.DataFrame(st.session_state.physics_logs)
        st.dataframe(df.style.format(precision=2), use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 전체 로그 CSV 다운로드", csv, "physics_logs.csv", "text/csv")
    else:
        st.info("아직 계산된 로그가 없습니다.")