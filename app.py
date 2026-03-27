import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Moving Motivators | CHAMPFROGS",
    page_icon="🎯",
    layout="wide",
)

# ── Datos ────────────────────────────────────────────────────────────────────

MOTIVATORS = [
    {
        "id": "curiosity",
        "letter": "C",
        "name": "Curiosidad",
        "description": "Tengo muchas cosas para investigar y pensar",
        "color": "#F5A623",
        "text_color": "#000000",
    },
    {
        "id": "honor",
        "letter": "H",
        "name": "Honor",
        "description": "Me siento orgulloso/a de que mis valores personales se reflejen en cómo trabajo",
        "color": "#1ABC9C",
        "text_color": "#ffffff",
    },
    {
        "id": "acceptance",
        "letter": "A",
        "name": "Aceptación",
        "description": "Las personas a mi alrededor aprueban lo que hago y quién soy",
        "color": "#8E44AD",
        "text_color": "#ffffff",
    },
    {
        "id": "mastery",
        "letter": "M",
        "name": "Maestría",
        "description": "Mi trabajo desafía mi competencia pero aún está dentro de mis habilidades",
        "color": "#E91E8C",
        "text_color": "#ffffff",
    },
    {
        "id": "power",
        "letter": "P",
        "name": "Poder",
        "description": "Hay suficiente espacio para influir en lo que sucede a mi alrededor",
        "color": "#F1C40F",
        "text_color": "#000000",
    },
    {
        "id": "freedom",
        "letter": "F",
        "name": "Libertad",
        "description": "Soy independiente de otros con mi trabajo y mis responsabilidades",
        "color": "#E74C3C",
        "text_color": "#ffffff",
    },
    {
        "id": "relatedness",
        "letter": "R",
        "name": "Relación",
        "description": "Tengo buenos contactos sociales con las personas en mi trabajo",
        "color": "#27AE60",
        "text_color": "#ffffff",
    },
    {
        "id": "order",
        "letter": "O",
        "name": "Orden",
        "description": "Hay suficientes reglas y políticas para un entorno estable",
        "color": "#FF7675",
        "text_color": "#ffffff",
    },
    {
        "id": "goal",
        "letter": "G",
        "name": "Meta",
        "description": "Mi propósito en la vida se refleja en el trabajo que hago",
        "color": "#2C3E50",
        "text_color": "#ffffff",
    },
    {
        "id": "status",
        "letter": "S",
        "name": "Estatus",
        "description": "Mi posición es buena y reconocida por las personas que trabajan conmigo",
        "color": "#FD79A8",
        "text_color": "#000000",
    },
]

MOTIVATOR_MAP = {m["id"]: m for m in MOTIVATORS}

# ── CSS personalizado ─────────────────────────────────────────────────────────

st.markdown(
    """
<style>
    .main { padding-top: 1rem; }

    .phase-indicator {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
    }
    .phase-step {
        flex: 1;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        font-size: 13px;
        background: #f0f0f0;
        color: #888;
        border: 2px solid transparent;
    }
    .phase-step.active {
        background: #1a73e8;
        color: white;
        border-color: #1a73e8;
    }
    .phase-step.done {
        background: #e8f5e9;
        color: #2e7d32;
        border-color: #81c784;
    }

    .card-wrapper {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        margin-bottom: 6px;
    }
    .card-header {
        padding: 8px 6px;
        text-align: center;
        font-weight: 700;
        font-size: 12px;
        line-height: 1.2;
        min-height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .card-body {
        background: #fafafa;
        padding: 8px 6px;
        font-size: 10px;
        color: #444;
        text-align: center;
        min-height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-left: 1px solid #e0e0e0;
        border-right: 1px solid #e0e0e0;
    }
    .card-footer {
        padding: 5px 4px;
        text-align: center;
        font-weight: 700;
        font-size: 12px;
        color: white;
    }
    .card-rank {
        background: rgba(0,0,0,0.15);
        padding: 3px 6px;
        font-size: 10px;
        text-align: center;
        font-weight: 700;
    }

    .pos-positive { background-color: #27AE60; }
    .pos-neutral   { background-color: #7F8C8D; }
    .pos-negative  { background-color: #E74C3C; }

    .legend-box {
        display: flex;
        gap: 16px;
        align-items: center;
        padding: 10px 16px;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        font-weight: 500;
    }
    .dot {
        width: 14px; height: 14px;
        border-radius: 50%;
        display: inline-block;
    }

    .summary-card {
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 8px;
    }
    .sum-improve { background: #e8f5e9; border-left: 4px solid #27AE60; }
    .sum-worsen  { background: #fdecea; border-left: 4px solid #E74C3C; }
    .sum-same    { background: #eceff1; border-left: 4px solid #7F8C8D; }

    div[data-testid="stButton"] > button {
        border-radius: 6px;
        font-size: 13px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ── Estado de sesión ──────────────────────────────────────────────────────────


def init_state():
    if "order" not in st.session_state:
        st.session_state.order = [m["id"] for m in MOTIVATORS]
    if "current" not in st.session_state:
        st.session_state.current = {m["id"]: 0 for m in MOTIVATORS}
    if "desired" not in st.session_state:
        st.session_state.desired = {m["id"]: 0 for m in MOTIVATORS}
    if "phase" not in st.session_state:
        st.session_state.phase = 1


# ── Callbacks ─────────────────────────────────────────────────────────────────


def move_card(idx, direction):
    """Swap card at idx with neighbor (direction: -1=left, +1=right)."""
    order = list(st.session_state.order)
    target = idx + direction
    if 0 <= target < len(order):
        order[idx], order[target] = order[target], order[idx]
        st.session_state.order = order


def change_position(phase_key, mid, delta):
    positions = dict(st.session_state[phase_key])
    positions[mid] = max(-1, min(1, positions[mid] + delta))
    st.session_state[phase_key] = positions


def set_phase(n):
    st.session_state.phase = n


def reset_all():
    for key in ["order", "current", "desired", "phase"]:
        st.session_state.pop(key, None)


# ── Componentes visuales ──────────────────────────────────────────────────────

POS_CONFIG = {
    1:  {"label": "Positivo", "symbol": "▲", "class": "pos-positive"},
    0:  {"label": "Neutro",   "symbol": "●", "class": "pos-neutral"},
    -1: {"label": "Negativo", "symbol": "▼", "class": "pos-negative"},
}


def render_card(m, rank=None, position=None, phase_key=None):
    """Render a motivator card inside a Streamlit column."""
    rank_html = (
        f'<div class="card-rank" style="background:{m["color"]}; color:{m["text_color"]}; opacity:0.8;">'
        f"#{rank}</div>"
        if rank is not None
        else ""
    )

    footer_html = ""
    if position is not None:
        cfg = POS_CONFIG[position]
        footer_html = (
            f'<div class="card-footer {cfg["class"]}">'
            f'{cfg["symbol"]} {cfg["label"]}</div>'
        )

    st.markdown(
        f"""
<div class="card-wrapper">
  {rank_html}
  <div class="card-header" style="background:{m['color']}; color:{m['text_color']};">
    {m['name']}
  </div>
  <div class="card-body">{m['description']}</div>
  {footer_html}
</div>""",
        unsafe_allow_html=True,
    )

    # Botones de reorden (fase 1)
    if phase_key is None and rank is not None:
        idx = rank - 1
        c1, c2 = st.columns(2)
        with c1:
            st.button(
                "◀",
                key=f"left_{idx}",
                on_click=move_card,
                args=(idx, -1),
                disabled=idx == 0,
                use_container_width=True,
                help="Más importante",
            )
        with c2:
            st.button(
                "▶",
                key=f"right_{idx}",
                on_click=move_card,
                args=(idx, 1),
                disabled=idx == len(st.session_state.order) - 1,
                use_container_width=True,
                help="Menos importante",
            )

    # Botones de posición (fases 2 y 3)
    if phase_key is not None:
        c1, c2 = st.columns(2)
        with c1:
            st.button(
                "▲",
                key=f"{phase_key}_up_{m['id']}",
                on_click=change_position,
                args=(phase_key, m["id"], 1),
                disabled=position >= 1,
                use_container_width=True,
                help="Impacto positivo",
            )
        with c2:
            st.button(
                "▼",
                key=f"{phase_key}_dn_{m['id']}",
                on_click=change_position,
                args=(phase_key, m["id"], -1),
                disabled=position <= -1,
                use_container_width=True,
                help="Impacto negativo",
            )


# ── Indicador de progreso ─────────────────────────────────────────────────────


def render_progress():
    phase = st.session_state.phase
    labels = [
        "1️⃣  Ordenar por importancia",
        "2️⃣  Situación Actual",
        "3️⃣  Situación Deseada",
    ]
    cols = st.columns(3)
    for i, (col, label) in enumerate(zip(cols, labels)):
        step = i + 1
        if step == phase:
            css = "active"
        elif step < phase:
            css = "done"
        else:
            css = ""
        with col:
            st.markdown(
                f'<div class="phase-step {css}">{label}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("")


# ── Fases ─────────────────────────────────────────────────────────────────────


def render_phase1():
    st.subheader("Ordenar motivadores por importancia")
    st.markdown(
        "Usa los botones **◀ ▶** para mover cada tarjeta. "
        "El más importante va a la **izquierda**, el menos importante a la **derecha**."
    )

    order = st.session_state.order
    cols = st.columns(len(order))
    for i, mid in enumerate(order):
        with cols[i]:
            render_card(MOTIVATOR_MAP[mid], rank=i + 1)

    st.markdown("---")
    _, right = st.columns([3, 1])
    with right:
        st.button(
            "Siguiente: Situación Actual →",
            type="primary",
            on_click=set_phase,
            args=(2,),
            use_container_width=True,
        )


def render_phase2():
    st.subheader("Situación Actual")
    st.markdown(
        "¿Cómo impacta tu situación actual a cada motivador? "
        "**▲ Positivo** — mejora el motivador &nbsp;|&nbsp; "
        "**● Neutro** — sin efecto &nbsp;|&nbsp; "
        "**▼ Negativo** — lo perjudica"
    )

    order = st.session_state.order
    current = st.session_state.current
    cols = st.columns(len(order))
    for i, mid in enumerate(order):
        with cols[i]:
            render_card(MOTIVATOR_MAP[mid], position=current[mid], phase_key="current")

    st.markdown("---")
    left, _, right = st.columns([1, 2, 1])
    with left:
        st.button("← Paso 1", on_click=set_phase, args=(1,), use_container_width=True)
    with right:
        st.button(
            "Siguiente: Situación Deseada →",
            type="primary",
            on_click=set_phase,
            args=(3,),
            use_container_width=True,
        )


def build_comparison_chart(order, current, desired):
    names = [MOTIVATOR_MAP[mid]["name"] for mid in order]
    curr_vals = [current[mid] for mid in order]
    des_vals = [desired[mid] for mid in order]

    label_map = {1: "▲ Positivo", 0: "● Neutro", -1: "▼ Negativo"}

    fig = go.Figure()

    # Línea situación actual
    fig.add_trace(
        go.Scatter(
            x=names,
            y=curr_vals,
            mode="lines+markers",
            name="Situación Actual",
            line=dict(color="#3498DB", width=3),
            marker=dict(size=12, color="#3498DB", symbol="circle"),
            hovertemplate="<b>%{x}</b><br>Actual: %{customdata}<extra></extra>",
            customdata=[label_map[v] for v in curr_vals],
        )
    )

    # Línea situación deseada
    fig.add_trace(
        go.Scatter(
            x=names,
            y=des_vals,
            mode="lines+markers",
            name="Situación Deseada",
            line=dict(color="#E67E22", width=3, dash="dash"),
            marker=dict(size=12, color="#E67E22", symbol="diamond"),
            hovertemplate="<b>%{x}</b><br>Deseada: %{customdata}<extra></extra>",
            customdata=[label_map[v] for v in des_vals],
        )
    )

    # Relleno de área entre las líneas
    diffs = [des_vals[i] - curr_vals[i] for i in range(len(order))]
    for i, (name, diff) in enumerate(zip(names, diffs)):
        if diff != 0:
            color = "rgba(39,174,96,0.15)" if diff > 0 else "rgba(231,76,60,0.15)"
            fig.add_shape(
                type="rect",
                x0=i - 0.4,
                x1=i + 0.4,
                y0=curr_vals[i],
                y1=des_vals[i],
                fillcolor=color,
                line_width=0,
            )

    fig.update_layout(
        yaxis=dict(
            tickvals=[-1, 0, 1],
            ticktext=["▼ Negativo", "● Neutro", "▲ Positivo"],
            range=[-1.6, 1.6],
            gridcolor="#ececec",
        ),
        xaxis=dict(
            title="Motivadores (de más → menos importante)",
            gridcolor="#ececec",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        height=380,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=40, b=40, l=10, r=10),
        hovermode="x unified",
    )
    fig.add_hline(y=0, line_dash="dot", line_color="#aaa", opacity=0.6)

    return fig


def render_phase3():
    st.subheader("Situación Deseada")
    st.markdown(
        "¿Cómo impactaría tu **situación deseada** a cada motivador? "
        "Compara con la situación actual para ver qué mejora o empeora."
    )

    order = st.session_state.order
    current = st.session_state.current
    desired = st.session_state.desired

    # Tarjetas con posición deseada
    cols = st.columns(len(order))
    for i, mid in enumerate(order):
        with cols[i]:
            render_card(MOTIVATOR_MAP[mid], position=desired[mid], phase_key="desired")

    st.markdown("---")
    st.subheader("Comparación: Actual vs. Deseada")

    fig = build_comparison_chart(order, current, desired)
    st.plotly_chart(fig, use_container_width=True)

    # Leyenda de diferencias
    st.markdown(
        """
<div class="legend-box">
  <div class="legend-item"><span class="dot" style="background:#27AE60"></span> Mejora con la situación deseada</div>
  <div class="legend-item"><span class="dot" style="background:#E74C3C"></span> Empeora con la situación deseada</div>
  <div class="legend-item"><span class="dot" style="background:#7F8C8D"></span> Sin cambio</div>
  <div class="legend-item" style="color:#3498DB; font-weight:700;">─── Situación Actual</div>
  <div class="legend-item" style="color:#E67E22; font-weight:700;">- - Situación Deseada</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Resumen
    st.subheader("Resumen del impacto")

    label_map = {1: "▲ Positivo", 0: "● Neutro", -1: "▼ Negativo"}

    improved = [
        (MOTIVATOR_MAP[mid]["name"], current[mid], desired[mid])
        for mid in order
        if desired[mid] > current[mid]
    ]
    worsened = [
        (MOTIVATOR_MAP[mid]["name"], current[mid], desired[mid])
        for mid in order
        if desired[mid] < current[mid]
    ]
    same = [
        (MOTIVATOR_MAP[mid]["name"], current[mid], desired[mid])
        for mid in order
        if desired[mid] == current[mid]
    ]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f'<div class="summary-card sum-improve">'
            f"<strong>✅ Mejoran ({len(improved)})</strong></div>",
            unsafe_allow_html=True,
        )
        for name, c, d in improved:
            st.markdown(f"&nbsp;&nbsp;**{name}**: {label_map[c]} → {label_map[d]}")

    with c2:
        st.markdown(
            f'<div class="summary-card sum-worsen">'
            f"<strong>❌ Empeoran ({len(worsened)})</strong></div>",
            unsafe_allow_html=True,
        )
        for name, c, d in worsened:
            st.markdown(f"&nbsp;&nbsp;**{name}**: {label_map[c]} → {label_map[d]}")

    with c3:
        st.markdown(
            f'<div class="summary-card sum-same">'
            f"<strong>➡️ Sin cambio ({len(same)})</strong></div>",
            unsafe_allow_html=True,
        )
        for name, c, d in same:
            st.markdown(f"&nbsp;&nbsp;**{name}**: {label_map[c]}")

    st.markdown("---")
    left, _, right = st.columns([1, 2, 1])
    with left:
        st.button("← Paso 2", on_click=set_phase, args=(2,), use_container_width=True)
    with right:
        st.button(
            "🔄 Reiniciar",
            on_click=reset_all,
            use_container_width=True,
        )


# ── Barra lateral ─────────────────────────────────────────────────────────────


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🎯 Moving Motivators")
        st.markdown(
            "Herramienta basada en el modelo **CHAMPFROGS** de [Management 3.0](https://management30.com/)"
        )
        st.markdown("---")
        st.markdown("### Los 10 motivadores")
        for m in MOTIVATORS:
            st.markdown(
                f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">'
                f'<span style="background:{m["color"]}; color:{m["text_color"]}; '
                f'padding:2px 8px; border-radius:12px; font-weight:700; font-size:12px;">'
                f'{m["letter"]}</span>'
                f'<span style="font-size:13px;"><strong>{m["name"]}</strong></span>'
                f"</div>"
                f'<div style="font-size:11px; color:#666; margin-left:36px; margin-bottom:4px;">'
                f"{m['description']}</div>",
                unsafe_allow_html=True,
            )
        st.markdown("---")
        st.markdown("### Cómo usar")
        st.markdown(
            "1. **Paso 1**: Ordena las tarjetas de más a menos importante usando ◀ ▶\n"
            "2. **Paso 2**: Indica si tu situación actual impacta positiva o negativamente cada motivador\n"
            "3. **Paso 3**: Haz lo mismo para tu situación deseada y compara"
        )


# ── Main ──────────────────────────────────────────────────────────────────────

init_state()
render_sidebar()

st.markdown("# 🎯 Moving Motivators")
st.markdown(
    "Descubre qué te motiva, evalúa tu situación actual y visualiza el impacto de un cambio."
)
st.markdown("")

render_progress()
st.markdown("---")

phase = st.session_state.phase
if phase == 1:
    render_phase1()
elif phase == 2:
    render_phase2()
else:
    render_phase3()
