import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Yash Patel | Bioinformatics",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Hide default Streamlit menu and footer */
#MainMenu {visibility: hidden;}
footer    {visibility: hidden;}
header    {visibility: hidden;}

/* Overall font */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Navigation bar spacing */
.nav-container { margin-bottom: 2rem; }

/* Hero heading gradient */
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00C9A7 0%, #845EC2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.hero-subtitle {
    font-size: 1.2rem;
    color: #A0AEC0;
    margin-bottom: 1.5rem;
}

/* Metric cards */
.metric-card {
    background: #1A1D2E;
    border: 1px solid #2D3047;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.metric-card .metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #00C9A7;
}
.metric-card .metric-label {
    font-size: 0.85rem;
    color: #718096;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Section headers */
.section-header {
    font-size: 1.6rem;
    font-weight: 700;
    color: #E8EAED;
    border-left: 4px solid #00C9A7;
    padding-left: 0.75rem;
    margin: 2rem 0 1rem 0;
}

/* Project cards */
.project-card {
    background: #1A1D2E;
    border: 1px solid #2D3047;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: border-color 0.2s;
}
.project-card:hover {
    border-color: #00C9A7;
}
.project-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #00C9A7;
    margin-bottom: 0.4rem;
}
.project-tag {
    display: inline-block;
    background: #2D3047;
    color: #A0AEC0;
    font-size: 0.75rem;
    border-radius: 20px;
    padding: 2px 10px;
    margin: 2px 3px 2px 0;
}

/* Badge chips */
.badge {
    display: inline-block;
    background: rgba(0,201,167,0.15);
    color: #00C9A7;
    border: 1px solid rgba(0,201,167,0.3);
    font-size: 0.8rem;
    border-radius: 20px;
    padding: 3px 12px;
    margin: 3px;
}

/* Chat message custom */
.chat-hint {
    font-size: 0.8rem;
    color: #718096;
    font-style: italic;
    margin-bottom: 1rem;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #2D3047;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS — UPDATE THESE WITH YOUR REAL INFO
# ══════════════════════════════════════════════════════════════════════════════

GITHUB_USERNAME = "Yash22062002"        # ← Replace with your actual GitHub username
LINKEDIN_URL    = "https://www.linkedin.com/in/yash-patel-network/"   # ← Replace
RESUME_URL      = ""                 # ← Optional: link to hosted PDF resume

ABOUT_ME = """
MSc Bioinformatics graduate from Northeastern University (Toronto, GPA 3.7) with a
Bachelor of Pharmacy background. I specialise in building reproducible computational
pipelines for genomics and transcriptomics, and I am passionate about translating
complex biological data into actionable insights.
"""

SYSTEM_PROMPT = """You are an intelligent assistant representing Yash Patel, a bioinformatics
professional. Answer recruiter and researcher questions ONLY using the facts below.
If a question is outside these facts, say you will pass it to Yash directly and suggest
they email or connect on LinkedIn.

=== EDUCATION ===
MSc Bioinformatics — Northeastern University, Toronto Campus. GPA 3.7. Graduated December 2025.
Bachelor of Pharmacy — L.M. College of Pharmacy, Ahmedabad, India.
Coursework: Single-cell RNA-seq (Seurat, Scanpy), spatial transcriptomics, proteomics, epigenomics,
multi-omics integration, machine learning for biology.

=== FLAGSHIP PROJECTS ===
1. Comparative Genomics Nextflow Pipeline (MSc Capstone)
   - Analyzed synonymous acceleration elements (SAEs) across 120 mammalian species.
   - Tools: Nextflow, HyPhy, FRESCo, SLURM, BEDTools, Python, Bash.
   - Scale: ~20,000 CPU-hours on Discovery HPC; 1,977 of 1,980 gene-level alignments processed.
   - Dataset: Hiller Lab 120-mammal whole-genome alignment. Supervised by Prof. Maxim Y. Wolf.
   - Output: BED12 format synonymous acceleration calls with Bonferroni-corrected p-values.

2. Bulk RNA-seq Pipeline — Tumour Microenvironment Remodeling in Multiple Myeloma
   - Investigated TME remodeling using bulk RNA-seq differential expression analysis.
   - Tools: STAR, Salmon, DESeq2, R (ggplot2, pheatmap), Python.
   - Outputs: Volcano plots, PCA, pathway enrichment, differential gene expression results.

3. Multi-omics Coursework Project — NFKB1
   - Integrated genomics, transcriptomics, epigenomics, and proteomics data for NFKB1.

=== TECHNICAL SKILLS ===
Programming: Python, R, Bash/Shell scripting
Pipeline tools: Nextflow, Snakemake, SLURM (HPC job arrays)
Bioinformatics: GATK, bcftools, STAR, Salmon, DESeq2, Seurat, Scanpy, HyPhy, FRESCo
Containerisation: Docker, Singularity
Statistics/ML: elastic net regression (glmnet), DESeq2, survival analysis
Cloud/HPC: SLURM cluster, Discovery HPC, GitHub Actions

=== WORK EXPERIENCE ===
Pharmacy Assistant — Pharmazone Pharmacy, Scarborough, Ontario (current)
Walmart Associate — Store 3159, Scarborough (current)
GMP Manufacturing (Quality/Production) — Rakesh Health Care India Limited, Gandhinagar, India

=== RESEARCH & PRESENTATIONS ===
MSc Poster: RNA-seq Tumour Microenvironment (Northeastern Capstone Showcase)
MSc Poster: Comparative Genomics Synonymous Acceleration Elements (Northeastern Capstone Showcase)
Presidential Visit Presentation — Northeastern Toronto, October 2025
Poster accepted at CBHC conference (unable to attend in person)
Student representative on Program Advisory Committee (PAC) for Bioinformatics at Northeastern
Volunteer: MaRS Discovery District Impact Health Event

=== CAREER INTERESTS ===
Open to bioinformatics analyst, computational biology, pharmaceutical QA/validation,
and clinical research associate roles across Canada (GTA preferred, remote considered).
Available immediately. Valid Canadian work authorisation.

=== CONTACT ===
LinkedIn: https://www.linkedin.com/in/yash-patel-network/
GitHub: https://github.com/Yash22062002
Email: yp8287@gmail.com
Location: Toronto, Ontario, Greater Toronto Area
"""

# ── FLOATING CHAT WIDGET ─────────────────────────────────────────────────────
_api_key = st.secrets.get("API_KEY", "")
import json
_system  = SYSTEM_PROMPT.replace("\\", "").replace("`", "'").replace('"', "'").replace("\n", " ")
<script>
(function() {{
  var par = window.parent.document;
  var win = window.parent;

  var apiKey    = "{_api_key}";
  var sysPrompt = "{_system}";
  // Persist chat history across page changes
  if (!win._yashHistory) win._yashHistory = [];

  // Inject styles once ───────────────────────────────────────────────────
  if (!par.getElementById('yash-chat-styles')) {{
    var style    = par.createElement('style');
    style.id     = 'yash-chat-styles';
    style.textContent = `
      #yash-chat-bubble {{
        position: fixed; bottom: 2rem; right: 2rem;
        width: 58px; height: 58px;
        background: linear-gradient(135deg, #00C9A7, #845EC2);
        border-radius: 50%; border: none; cursor: pointer;
        font-size: 1.5rem; z-index: 99999;
        box-shadow: 0 4px 20px rgba(0,201,167,0.45);
        transition: transform 0.2s;
        display: flex; align-items: center; justify-content: center;
      }}
      #yash-chat-bubble:hover {{ transform: scale(1.1); }}
      #yash-chat-panel {{
        position: fixed; bottom: 5.5rem; right: 2rem;
        width: 320px; height: 460px;
        background: #1A1D2E; border: 1px solid #2D3047;
        border-radius: 16px; z-index: 99998;
        box-shadow: 0 8px 40px rgba(0,0,0,0.6);
        display: none; flex-direction: column; overflow: hidden;
        font-family: Inter, sans-serif;
      }}
      #yash-chat-panel.open {{ display: flex !important; }}
      #yash-chat-header {{
        background: linear-gradient(135deg, #00C9A7, #845EC2);
        padding: 0.75rem 1rem; font-weight: 700; font-size: 0.9rem;
        color: #0F1117; display: flex;
        justify-content: space-between; align-items: center;
        flex-shrink: 0;
      }}
      #yash-chat-close {{
        background: none; border: none; cursor: pointer;
        font-size: 1.1rem; font-weight: 700; color: #0F1117;
      }}
      #yash-chat-msgs {{
        flex: 1; overflow-y: auto; padding: 0.75rem;
        display: flex; flex-direction: column; gap: 0.5rem;
      }}
      .ycmsg {{
        max-width: 88%; padding: 0.5rem 0.75rem;
        border-radius: 12px; font-size: 0.82rem;
        line-height: 1.5; word-wrap: break-word;
      }}
      .ycmsg.user {{
        background: rgba(0,201,167,0.18); color: #E8EAED;
        align-self: flex-end; border-bottom-right-radius: 3px;
      }}
      .ycmsg.bot {{
        background: #2D3047; color: #E8EAED;
        align-self: flex-start; border-bottom-left-radius: 3px;
      }}
      .ycmsg.thinking {{
        background: #2D3047; color: #718096;
        align-self: flex-start; font-style: italic;
      }}
      #yash-chat-footer {{
        padding: 0.6rem; border-top: 1px solid #2D3047;
        display: flex; gap: 0.4rem; flex-shrink: 0;
      }}
      #yash-chat-input {{
        flex: 1; background: #0F1117; border: 1px solid #2D3047;
        border-radius: 8px; color: #E8EAED;
        padding: 0.45rem 0.65rem; font-size: 0.82rem; outline: none;
      }}
      #yash-chat-input:focus {{ border-color: #00C9A7; }}
      #yash-chat-send {{
        background: #00C9A7; border: none; border-radius: 8px;
        color: #0F1117; padding: 0.45rem 0.8rem;
        cursor: pointer; font-weight: 700; font-size: 1rem;
      }}
      #yash-chat-send:hover {{ background: #00b896; }}
    `;
    par.head.appendChild(style);
  }}

  // ── Inject HTML once ─────────────────────────────────────────────────────
  if (!par.getElementById('yash-chat-bubble')) {{
    var bubble    = par.createElement('button');
    bubble.id     = 'yash-chat-bubble';
    bubble.innerHTML = '🤖';
    par.body.appendChild(bubble);

    var panel    = par.createElement('div');
    panel.id     = 'yash-chat-panel';
    panel.innerHTML = `
      <div id="yash-chat-header">
        <span>🧬 Ask Yash's AI</span>
        <button id="yash-chat-close">✕</button>
      </div>
      <div id="yash-chat-msgs">
        <div class="ycmsg bot">
          Hi! I am Yash's AI assistant. Ask me anything about his background, projects, or experience.
        </div>
      </div>
      <div id="yash-chat-footer">
        <input id="yash-chat-input" type="text" placeholder="Ask a question..." />
        <button id="yash-chat-send">➤</button>
      </div>
    `;
    par.body.appendChild(panel);
  }}

  // ── Always redefine functions on parent window ────────────────────────────
  win._yashToggle = function() {{
    var panel = par.getElementById('yash-chat-panel');
    panel.classList.toggle('open');
    if (panel.classList.contains('open'))
      par.getElementById('yash-chat-input').focus();
  }};

  win._yashAddMsg = function(role, text) {{
    var box = par.getElementById('yash-chat-msgs');
    var d   = par.createElement('div');
    d.className   = 'ycmsg ' + role;
    d.textContent = text;
    box.appendChild(d);
    box.scrollTop = box.scrollHeight;
    return d;
  }};

  win._yashSend = async function() {{
    var inp  = par.getElementById('yash-chat-input');
    var text = inp.value.trim();
    if (!text) return;
    inp.value = '';
    win._yashAddMsg('user', text);
    win._yashHistory.push({{role:'user', content:text}});
    var thinking = win._yashAddMsg('thinking', 'Thinking...');
    try {{
      var res = await fetch(
        'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions',
        {{
          method: 'POST',
          headers: {{
            'Content-Type':  'application/json',
            'Authorization': 'Bearer ' + apiKey
          }},
          body: JSON.stringify({{
            model:      'gemini-2.5-flash',
            max_tokens: 400,
            messages:   [
              {{role:'system', content: sysPrompt}},
              ...win._yashHistory
            ]
          }})
        }}
      );
      var data   = await res.json();
      var answer = data.choices[0].message.content;
      thinking.className   = 'ycmsg bot';
      thinking.textContent = answer;
      win._yashHistory.push({{role:'assistant', content:answer}});
    }} catch(e) {{
      thinking.className   = 'ycmsg bot';
      thinking.textContent = 'Could not connect right now. Please try again.';
    }}
  }};

  // ── Re-attach event listeners every rerun (cloneNode removes old ones) ────
  function reattach(id, event, fn) {{
    var el = par.getElementById(id);
    if (!el) return;
    var fresh = el.cloneNode(true);
    el.parentNode.replaceChild(fresh, el);
    fresh.addEventListener(event, fn);
  }}

  reattach('yash-chat-bubble', 'click', win._yashToggle);
  reattach('yash-chat-close',  'click', win._yashToggle);
  reattach('yash-chat-send',   'click', win._yashSend);
  reattach('yash-chat-input',  'keydown', function(e) {{
    if (e.key === 'Enter') win._yashSend();
  }});

}})();
</script>
""", height=0, scrolling=False) 
# ══════════════════════════════════════════════════════════════════════════════
#  NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════

selected = option_menu(
    menu_title=None,
    options=["Home", "Projects", "Skills", "GitHub", "Ask My AI"],
    icons=["house-fill", "code-slash", "bar-chart-fill", "github", "robot"],
    orientation="horizontal",
    styles={
        "container":    {"padding": "0.4rem 0", "background-color": "#1A1D2E",
                         "border-radius": "12px", "margin-bottom": "2rem"},
        "icon":         {"color": "#00C9A7", "font-size": "1rem"},
        "nav-link":     {"font-size": "0.9rem", "color": "#A0AEC0",
                         "padding": "0.5rem 1.2rem", "border-radius": "8px"},
        "nav-link-selected": {"background-color": "#00C9A7",
                              "color": "#0F1117", "font-weight": "700"},
    },
)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════

if selected == "Home":

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown('<p class="hero-title">Yash Patel</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="hero-subtitle">🧬 Bioinformatics · Computational Biology · Genomics Pipelines</p>',
            unsafe_allow_html=True,
        )
        st.markdown(ABOUT_ME)

        st.markdown("**Currently based in:** Toronto, Ontario (Greater Toronto Area)")
        st.markdown("**Open to:** Bioinformatics Analyst · Computational Biology · Pharma QA · Remote roles")
        
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Profile placeholder — replace with st.image("photo.jpg") once you add a headshot
        st.image("yash.jpg", width=180)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Quick-stats row
    st.markdown('<p class="section-header">At a Glance</p>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, val, label in [
        (s1, "3.7", "MSc GPA"),
        (s2, "2", "Flagship Pipelines"),
        (s3, "120", "Mammalian Species Analyzed"),
        (s4, "20K+", "CPU-Hours (HPC)"),
    ]:
        with col:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Education
    st.markdown('<p class="section-header">Education</p>', unsafe_allow_html=True)
    ec1, ec2 = st.columns(2)
    with ec1:
        st.markdown("""
        **MSc Bioinformatics**
        Northeastern University — Toronto Campus
        GPA 3.7 · Graduated December 2025
        """)
    with ec2:
        st.markdown("""
        **Bachelor of Pharmacy**
        L.M. College of Pharmacy — Ahmedabad, India
        """)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — PROJECTS
# ══════════════════════════════════════════════════════════════════════════════

elif selected == "Projects":

    st.markdown('<p class="section-header">Bioinformatics Projects</p>', unsafe_allow_html=True)

    # ── Project 1: Comparative Genomics ─────────────────────────────────────
    with st.expander("🦎 Comparative Genomics Nextflow Pipeline — Synonymous Acceleration Elements", expanded=True):
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown("""
**Scientific Question:** Which protein-coding regions show unexpectedly elevated synonymous
substitution rates across 120 mammalian species — suggesting novel regulatory or functional evolution?

**Approach:**
- Processed the Hiller Lab 120-mammal whole-genome alignment
- Ran gene-level codon alignments (1,977 of 1,980 genes completed)
- Used HyPhy and FRESCo to detect synonymous acceleration on each branch
- Applied Bonferroni correction for multiple testing; output in BED12 format
- Managed ~20,000 CPU-hours via SLURM job arrays on the Discovery HPC cluster

**Tools:** Nextflow · HyPhy · FRESCo · SLURM · BEDTools · Python · Bash
            """)
            for tag in ["Nextflow", "HyPhy", "FRESCo", "SLURM", "HPC", "Python", "Bash", "120 Species"]:
                st.markdown(f'<span class="project-tag">{tag}</span>', unsafe_allow_html=True)

        with c2:
            # Simulated scale chart
            df = pd.DataFrame({
                "Metric": ["Genes Completed", "Genes Total", "CPU Hours (K)"],
                "Value":  [1977, 1980, 20],
            })
            fig = go.Figure(go.Bar(
                x=df["Value"],
                y=df["Metric"],
                orientation="h",
                marker_color=["#00C9A7", "#2D3047", "#845EC2"],
                text=df["Value"],
                textposition="outside",
            ))
            fig.update_layout(
                title="Pipeline Scale",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#E8EAED",
                height=250,
                margin=dict(l=10, r=30, t=40, b=10),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Project 2: RNA-seq ──────────────────────────────────────────────────
    with st.expander("🔬 Bulk RNA-seq Pipeline — Tumour Microenvironment Remodeling in Multiple Myeloma"):
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown("""
**Scientific Question:** How does the tumour microenvironment remodel in multiple myeloma,
and which genes drive differential immune cell infiltration?

**Approach:**
- Aligned raw reads with STAR; quantified transcripts with Salmon
- Performed differential expression analysis using DESeq2 in R
- Visualised results with volcano plots, PCA, and pathway enrichment heatmaps
- Identified key immune cell markers and pathway dysregulation in the TME

**Tools:** STAR · Salmon · DESeq2 · R (ggplot2, pheatmap) · Python
            """)
            for tag in ["STAR", "Salmon", "DESeq2", "R", "ggplot2", "RNA-seq", "Cancer Genomics"]:
                st.markdown(f'<span class="project-tag">{tag}</span>', unsafe_allow_html=True)

        with c2:
            # Simulated volcano-style scatter
            import random
            random.seed(42)
            n = 150
            log2fc = [random.gauss(0, 2) for _ in range(n)]
            neglog10p = [abs(random.gauss(2, 1.5)) for _ in range(n)]
            colors = []
            for lfc, p in zip(log2fc, neglog10p):
                if lfc > 1 and p > 2:
                    colors.append("#00C9A7")
                elif lfc < -1 and p > 2:
                    colors.append("#845EC2")
                else:
                    colors.append("#4A5568")

            fig2 = go.Figure(go.Scatter(
                x=log2fc,
                y=neglog10p,
                mode="markers",
                marker=dict(color=colors, size=5, opacity=0.8),
                hovertemplate="Log2FC: %{x:.2f}<br>-log10(p): %{y:.2f}<extra></extra>",
            ))
            fig2.add_vline(x=1,  line_dash="dash", line_color="#718096", line_width=1)
            fig2.add_vline(x=-1, line_dash="dash", line_color="#718096", line_width=1)
            fig2.add_hline(y=2,  line_dash="dash", line_color="#718096", line_width=1)
            fig2.update_layout(
                title="Simulated Volcano Plot",
                xaxis_title="Log2 Fold Change",
                yaxis_title="-log10(p-value)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#E8EAED",
                height=280,
                margin=dict(l=10, r=10, t=40, b=10),
                xaxis=dict(gridcolor="#2D3047"),
                yaxis=dict(gridcolor="#2D3047"),
                showlegend=False,
            )
            st.caption("Simulated — replace with your actual DESeq2 results")
            st.plotly_chart(fig2, use_container_width=True)

    # ── Project 3: Multi-omics ──────────────────────────────────────────────
    with st.expander("🔗 Multi-omics Integration — NFKB1"):
        st.markdown("""
**Scientific Question:** What is the integrated regulatory landscape of NFKB1 across
multiple molecular layers in disease contexts?

**Approach:**
- Integrated four data layers: genomics (variant data), transcriptomics (expression),
  epigenomics (methylation/chromatin), and proteomics (protein abundance)
- Applied elastic net regression (glmnet in R) to identify cross-layer associations
- Identified concordant regulatory signals across omics layers

**Tools:** R · glmnet · Python · Bioconductor
        """)
        for tag in ["Multi-omics", "glmnet", "Elastic Net", "R", "Epigenomics", "Proteomics"]:
            st.markdown(f'<span class="project-tag">{tag}</span>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — SKILLS
# ══════════════════════════════════════════════════════════════════════════════

elif selected == "Skills":

    st.markdown('<p class="section-header">Technical Skills</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Programming languages bar chart
        langs = pd.DataFrame({
            "Skill":      ["Python", "R", "Bash / Shell", "Nextflow", "SQL"],
            "Proficiency": [90, 85, 80, 75, 60],
        })
        fig = go.Figure(go.Bar(
            y=langs["Skill"],
            x=langs["Proficiency"],
            orientation="h",
            marker=dict(
                color=langs["Proficiency"],
                colorscale=[[0, "#845EC2"], [1, "#00C9A7"]],
                showscale=False,
            ),
            text=[f"{v}%" for v in langs["Proficiency"]],
            textposition="outside",
        ))
        fig.update_layout(
            title="Programming & Pipeline Languages",
            xaxis=dict(range=[0, 110], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#E8EAED",
            height=300,
            margin=dict(l=10, r=60, t=50, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bioinformatics tools radar
        tools = ["GATK", "DESeq2", "Seurat", "Nextflow", "STAR/Salmon", "HyPhy"]
        scores = [75, 90, 80, 85, 88, 70]
        fig2 = go.Figure(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=tools + [tools[0]],
            fill="toself",
            fillcolor="rgba(0,201,167,0.15)",
            line=dict(color="#00C9A7", width=2),
            marker=dict(color="#00C9A7", size=6),
        ))
        fig2.update_layout(
            title="Bioinformatics Tools Proficiency",
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=False, range=[0, 100]),
                angularaxis=dict(color="#A0AEC0"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#E8EAED",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Domain expertise tags
    st.markdown('<p class="section-header">Domain Expertise</p>', unsafe_allow_html=True)

    domains = {
        "Genomics & Variant Analysis": ["GATK", "bcftools", "VCF processing", "Variant annotation", "BED/BEDTools"],
        "Transcriptomics": ["Bulk RNA-seq", "DESeq2", "STAR", "Salmon", "Volcano plots", "PCA"],
        "Single-cell & Spatial": ["Seurat", "Scanpy", "scRNA-seq QC", "Cell clustering", "Spatial transcriptomics"],
        "Pipeline & HPC": ["Nextflow", "SLURM", "Job arrays", "Docker", "Singularity", "GitHub Actions"],
        "Statistics & ML": ["DESeq2", "Elastic net (glmnet)", "Multi-omics integration", "Bonferroni correction"],
        "Pharma / Regulatory": ["GMP manufacturing", "QA/QC principles", "Pharmacy operations"],
    }
    for domain, tags in domains.items():
        st.markdown(f"**{domain}**")
        st.markdown(
            " ".join(f'<span class="badge">{t}</span>' for t in tags),
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Soft skills / research achievements
    st.markdown('<p class="section-header">Research Achievements</p>', unsafe_allow_html=True)
    achievements = [
        ("🎓", "MSc Bioinformatics — Northeastern University, Toronto (GPA 3.7, Dec 2025)"),
        ("📊", "2 MSc capstone poster presentations (RNA-seq + Comparative Genomics)"),
        ("🎤", "Presidential Visit Presentation — Northeastern Toronto, October 2025"),
        ("🏛", "Student rep on Program Advisory Committee (PAC) for Bioinformatics"),
        ("🔬", "Poster accepted at CBHC Conference 2025"),
        ("🤝", "Volunteer at MaRS Discovery District Impact Health Event"),
    ]
    for icon, text in achievements:
        st.markdown(f"{icon} &nbsp; {text}", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — GITHUB ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════

elif selected == "GitHub":

    st.markdown('<p class="section-header">Live GitHub Analytics</p>', unsafe_allow_html=True)
    st.caption(f"Live data from github.com/{GITHUB_USERNAME} — refreshes every hour")

    @st.cache_data(ttl=3600)
    def fetch_github_profile(username):
        try:
            r = requests.get(
                f"https://api.github.com/users/{username}",
                headers={"Accept": "application/vnd.github+json"},
                timeout=8,
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    @st.cache_data(ttl=3600)
    def fetch_repos(username):
        try:
            r = requests.get(
                f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated",
                headers={"Accept": "application/vnd.github+json"},
                timeout=8,
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return []

    profile = fetch_github_profile(GITHUB_USERNAME)
    repos   = fetch_repos(GITHUB_USERNAME)

    if not profile:
        st.warning(
            f"Could not load GitHub data for **{GITHUB_USERNAME}**. "
            "Please update the `GITHUB_USERNAME` constant at the top of `app.py` "
            "with your real GitHub username."
        )
    else:
        # Summary metrics
        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        total_forks = sum(r.get("forks_count", 0)      for r in repos)

        m1, m2, m3, m4 = st.columns(4)
        for col, val, label in [
            (m1, profile.get("public_repos", "N/A"), "Public Repos"),
            (m2, profile.get("followers",    "N/A"), "Followers"),
            (m3, total_stars,                         "Total Stars"),
            (m4, total_forks,                         "Total Forks"),
        ]:
            with col:
                st.markdown(
                    f"""<div class="metric-card">
                        <div class="metric-value">{val}</div>
                        <div class="metric-label">{label}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Language distribution
        lang_counts: dict = {}
        for repo in repos:
            lang = repo.get("language")
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1

        if lang_counts:
            lc_df = pd.DataFrame(
                sorted(lang_counts.items(), key=lambda x: x[1], reverse=True),
                columns=["Language", "Repos"],
            )
            col_a, col_b = st.columns(2)
            with col_a:
                fig_lang = go.Figure(go.Pie(
                    labels=lc_df["Language"],
                    values=lc_df["Repos"],
                    hole=0.4,
                    marker_colors=px.colors.sequential.Teal[::-1][:len(lc_df)],
                ))
                fig_lang.update_layout(
                    title="Languages Used Across Repos",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#E8EAED",
                    height=320,
                    margin=dict(t=50, b=10, l=10, r=10),
                    legend=dict(font=dict(color="#A0AEC0")),
                )
                st.plotly_chart(fig_lang, use_container_width=True)

            with col_b:
                # Top repos by stars
                top_repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:8]
                tr_df = pd.DataFrame({
                    "Repo":  [r["name"] for r in top_repos],
                    "Stars": [r.get("stargazers_count", 0) for r in top_repos],
                })
                fig_stars = go.Figure(go.Bar(
                    y=tr_df["Repo"],
                    x=tr_df["Stars"],
                    orientation="h",
                    marker_color="#845EC2",
                    text=tr_df["Stars"],
                    textposition="outside",
                ))
                fig_stars.update_layout(
                    title="Top Repos by Stars",
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#E8EAED",
                    height=320,
                    margin=dict(l=10, r=50, t=50, b=10),
                )
                st.plotly_chart(fig_stars, use_container_width=True)

        # Recent repositories table
        st.markdown('<p class="section-header">Recently Updated Repositories</p>', unsafe_allow_html=True)
        for repo in repos[:6]:
            with st.container():
                rc1, rc2 = st.columns([3, 1])
                with rc1:
                    st.markdown(
                        f"**[{repo['name']}](https://github.com/{GITHUB_USERNAME}/{repo['name']})**"
                    )
                    if repo.get("description"):
                        st.caption(repo["description"])
                with rc2:
                    lang = repo.get("language", "")
                    stars = repo.get("stargazers_count", 0)
                    st.caption(f"⭐ {stars}  {('  🔵 ' + lang) if lang else ''}")
            st.markdown('<hr class="divider" style="margin:0.5rem 0">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — AI CHAT
# ══════════════════════════════════════════════════════════════════════════════

elif selected == "Ask My AI":

    st.markdown('<p class="section-header">Ask My AI Assistant</p>', unsafe_allow_html=True)
    st.markdown(
        "Ask anything about my background, projects, or skills. "
        "The assistant knows my full résumé and research experience."
    )

    # Check for API key
    api_key = st.secrets.get("API_KEY", "")
    if not api_key:
        st.warning(
            "**API key not configured.** "
            "Add `API_KEY = 'your-key-here'` to your Streamlit secrets "
            "(Settings → Secrets in the Community Cloud dashboard) to enable the chatbot."
        )
        st.info(
            "Get a free Gemini API key at https://aistudio.google.com/apikey — "
            "no credit card required. 1,500 free requests per day."
        )
        st.stop()

    # Suggested questions as clickable pills
    st.markdown('<p class="chat-hint">Try one of these questions, or type your own below:</p>',
                unsafe_allow_html=True)

    suggestions = [
        "What RNA-seq projects has Yash completed?",
        "Walk me through the Nextflow comparative genomics pipeline",
        "What tools and languages does Yash know best?",
        "Is Yash open to remote roles?",
        "What is Yash's educational background?",
    ]
    pill_cols = st.columns(len(suggestions))
    for i, (col, q) in enumerate(zip(pill_cols, suggestions)):
        with col:
            if st.button(q, key=f"pill_{i}", use_container_width=True):
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state["trigger_response"] = True

    st.markdown("<br>", unsafe_allow_html=True)

    # Conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask about my background, projects, or experience...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state["trigger_response"] = True

    # Generate response when triggered
    if st.session_state.get("trigger_response"):
        st.session_state["trigger_response"] = False
        last_msg = st.session_state.messages[-1]["content"]
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    from openai import OpenAI
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                    )
                    response = client.chat.completions.create(
                        model="gemini-2.5-flash",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            *st.session_state.messages,
                        ],
                        stream=True
                    )
                    placeholder = st.empty()
                    full_response = ""
                    for chunk in response:
                        if (
                            hasattr(chunk.choices[0], "delta")
                            and chunk.choices[0].delta.content
                        ):
                            full_response += chunk.choices[0].delta.content
                            placeholder.markdown(full_response)
                    answer = full_response
                except Exception as e:
                    answer = (
                        "I was unable to connect to the AI backend right now. "
                        f"Error: {str(e)[:120]}"
                    )
                st.session_state.messages.append({"role": "assistant", "content": answer})

    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑 Clear conversation", type="secondary"):
            st.session_state.messages = []
            st.rerun()
