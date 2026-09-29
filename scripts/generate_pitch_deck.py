import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY = RGBColor(18, 48, 68)        # #123044
    C_TEAL = RGBColor(12, 124, 134)      # #0C7C86
    C_TEAL_DARK = RGBColor(8, 59, 76)    # #083B4C
    C_ORANGE = RGBColor(242, 142, 91)    # #F28E5B
    C_AQUA = RGBColor(216, 244, 242)      # #D8F4F2
    C_PALE = RGBColor(244, 248, 250)      # #F4F8FA
    C_WHITE = RGBColor(255, 255, 255)
    C_INK = RGBColor(24, 50, 63)         # #18323F
    C_MUTED = RGBColor(97, 119, 132)     # #617784
    C_LINE = RGBColor(199, 215, 222)     # #C7D7DE
    C_GREEN = RGBColor(47, 143, 104)     # #2F8F68

    def add_bg(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, subtitle_text=""):
        # Header Container
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.font.name = 'Arial'

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(14)
            p2.font.color.rgb = C_MUTED
            p2.font.name = 'Arial'
            p2.space_before = Pt(4)

        # Decorative Horizontal Accent Line
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.04))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_TEAL
        shape.line.color.rgb = C_TEAL

    def add_footer(slide, slide_num):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.3))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "AirlineSense MLOps & Feature Engineering  |  Sparsh Sharma"
        p.font.size = Pt(11)
        p.font.color.rgb = C_MUTED
        p.font.name = 'Arial'
        
        p_num = tf.add_paragraph()
        p_num.text = f"{slide_num:02d}"
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = C_TEAL
        p_num.font.name = 'Arial'

    # -------------------------------------------------------------
    # SLIDE 1: COVER
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    add_bg(slide1, C_TEAL_DARK)

    # Left Dark Panel Box
    panel = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(7.5), Inches(7.5))
    panel.fill.solid()
    panel.fill.fore_color.rgb = C_NAVY
    panel.line.fill.background()

    # Cover Text Box
    tb1 = slide1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.2), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "AirlineSense"
    p.font.size = Pt(52)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Predict passenger satisfaction before the complaint"
    p2.font.size = Pt(24)
    p2.font.color.rgb = C_AQUA
    p2.space_before = Pt(16)

    p3 = tf1.add_paragraph()
    p3.text = "End-to-End Feature Engineering & MLOps System"
    p3.font.size = Pt(16)
    p3.font.bold = True
    p3.font.color.rgb = C_WHITE
    p3.space_before = Pt(36)

    p4 = tf1.add_paragraph()
    p4.text = "Sparsh Sharma  ·  Roll 37"
    p4.font.size = Pt(15)
    p4.font.color.rgb = C_AQUA
    p4.space_before = Pt(8)

    # UI Demo Image Embed on Right
    ui_img_path = "presentation/ui-demo.png"
    if os.path.exists(ui_img_path):
        slide1.shapes.add_picture(ui_img_path, Inches(7.8), Inches(0.9), Inches(5.1), Inches(5.7))

    # -------------------------------------------------------------
    # SLIDE 2: BUSINESS & COMPANY PROBLEM
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_bg(slide2, C_WHITE)
    add_header(slide2, "Business & Company Problem Overview", "Airlines need an early signal of dissatisfaction while frontline staff can still intervene")
    add_footer(slide2, 2)

    # Metric Cards Left Column
    m_box1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.0), Inches(1.6))
    m_box1.fill.solid()
    m_box1.fill.fore_color.rgb = C_PALE
    m_box1.line.color.rgb = C_LINE
    tf = m_box1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "129,880"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = "Total Passenger Survey Records"
    p2.font.size = Pt(14)
    p2.font.color.rgb = C_MUTED

    m_box2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.4), Inches(4.0), Inches(1.6))
    m_box2.fill.solid()
    m_box2.fill.fore_color.rgb = C_PALE
    m_box2.line.color.rgb = C_LINE
    tf = m_box2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "43.5%"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_ORANGE
    p2 = tf.add_paragraph()
    p2.text = "Satisfied Passengers (Baseline Rate)"
    p2.font.size = Pt(14)
    p2.font.color.rgb = C_MUTED

    # Problem & Solution Statement Card
    p_card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.2), Inches(4.0), Inches(1.5))
    p_card.fill.solid()
    p_card.fill.fore_color.rgb = C_NAVY
    p_card.line.fill.background()
    tf = p_card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Business Goal:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_AQUA
    p2 = tf.add_paragraph()
    p2.text = "Predict dissatisfaction at touchpoints so agents can deliver proactive recovery (lounge access, miles, upgrades) before complaints happen."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(4)

    # Segment Satisfaction Chart Embed Right Column
    seg_img_path = "reports/figures/segment_satisfaction.png"
    if os.path.exists(seg_img_path):
        slide2.shapes.add_picture(seg_img_path, Inches(5.1), Inches(1.6), Inches(7.4), Inches(5.1))

    # -------------------------------------------------------------
    # SLIDE 3: DATA SIDE & LEAKAGE CONTROL
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_bg(slide3, C_PALE)
    add_header(slide3, "Data Side & Leakage Control", "Every learned transformation fits on training folds ONLY")
    add_footer(slide3, 3)

    # 4 Data Flow Boxes
    steps = [
        ("01", "Raw CSV Ingestion", "129,880 rows · 24 columns\nChecked schema & types"),
        ("02", "Stratified Split", "80% Train / 20% Test\nSplit BEFORE any scaling"),
        ("03", "Pipeline Fit", "Imputation & encoding\nfit on TRAIN fold only"),
        ("04", "Untouched Test", "25,976 test rows\nEvaluated once at end")
    ]
    for i, (num, label, desc) in enumerate(steps):
        x = Inches(0.8 + i * 2.98)
        box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.7), Inches(2.8), Inches(2.2))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_TEAL if i < 3 else C_ORANGE
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = C_TEAL if i < 3 else C_ORANGE
        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY
        p2.space_before = Pt(6)
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(12)
        p3.font.color.rgb = C_MUTED
        p3.space_before = Pt(6)

    # Highlight Cards Below
    h_card1 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.3))
    h_card1.fill.solid()
    h_card1.fill.fore_color.rgb = C_WHITE
    h_card1.line.color.rgb = C_LINE
    tf = h_card1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Handling 393 Missing Arrival Delays:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = tf.add_paragraph()
    p2.text = "• Applied SimpleImputer(strategy='median') inside training folds.\n• Median is robust against extreme right-skewed delay outliers (e.g. 300+ mins).\n• Kept all incomplete rows rather than dropping data."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_INK
    p2.space_before = Pt(6)

    h_card2 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(4.3), Inches(5.7), Inches(2.3))
    h_card2.fill.solid()
    h_card2.fill.fore_color.rgb = C_WHITE
    h_card2.line.color.rgb = C_LINE
    tf = h_card2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Identifier Leakage Prevention:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = tf.add_paragraph()
    p2.text = "• Unique Passenger ID dropped from feature matrix.\n• Zero row identifier signal reaches the classifier.\n• Prevents arbitrary row-id memorization and guarantees true generalization."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_INK
    p2.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 4: FEATURE ENGINEERING USED (MIND MAP AUDIT)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_bg(slide4, C_WHITE)
    add_header(slide4, "Feature Engineering Concepts Used (Mind Map Audit)", "Encapsulated inside sklearn ColumnTransformer & Pipeline")
    add_footer(slide4, 4)

    # Column 1: Production Pipeline (USED)
    c1 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.0))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_PALE
    c1.line.color.rgb = C_TEAL
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "PRODUCTION PIPELINE (USED)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    items_used = [
        ("Median Imputation", "Fills missing arrival delays cleanly without outlier corruption."),
        ("Mode Imputation", "Safe categorical fallback for missing strings."),
        ("One-Hot Encoding", "Converts categoricals with handle_unknown='ignore' (API safe)."),
        ("Conditional Scaling", "StandardScaler enabled for Logistic Regression; omitted for scale-invariant Random Forest.")
    ]
    for title, desc in items_used:
        p_t = tf1.add_paragraph()
        p_t.text = f"✔  {title}"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_before = Pt(10)
        p_d = tf1.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = C_MUTED

    # Column 2: Evaluated Experiment & Occam's Razor
    c2 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.6), Inches(5.7), Inches(5.0))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_ORANGE
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "EVALUATED EXPERIMENT (NOT PROMOTED)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_ORANGE

    p_t = tf2.add_paragraph()
    p_t.text = "AirlineFeatureEngineer (Domain Features):"
    p_t.font.size = Pt(14)
    p_t.font.bold = True
    p_t.font.color.rgb = C_NAVY
    p_t.space_before = Pt(10)

    p_d = tf2.add_paragraph()
    p_d.text = "Created 5 domain features:\n• Total Delay  ·  Average Service Score\n• Digital Experience Score  ·  Delay per 1,000 Miles\n• Is Delayed Flag"
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = C_INK
    p_d.space_before = Pt(4)

    p_r = tf2.add_paragraph()
    p_r.text = "Result: CV F1 = 0.951 vs 0.952 (Baseline)"
    p_r.font.size = Pt(15)
    p_r.font.bold = True
    p_r.font.color.rgb = C_ORANGE
    p_r.space_before = Pt(14)

    p_o = tf2.add_paragraph()
    p_o.text = "Occam's Razor Rationale:\nBaseline Random Forest performed slightly better. Adding engineered aggregations compressed finer details and added extra pipeline complexity without evidence of benefit. Baseline selected."
    p_o.font.size = Pt(12)
    p_o.font.color.rgb = C_MUTED
    p_o.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 5: EXPERIMENTS & MODEL SELECTION
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_bg(slide5, C_WHITE)
    add_header(slide5, "Experiment Tracking & Model Selection", "Cross-validated F1 determined the registered production model")
    add_footer(slide5, 5)

    # Model Comparison Table
    table_shape = slide5.shapes.add_table(4, 4, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(3.5)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(4.633)

    headers = ["Candidate Pipeline", "CV F1", "CV ROC-AUC", "Production Decision & Rationale"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    row_data = [
        ("Logistic Regression (Scaled)", "0.850", "0.926", "Interpretable linear baseline. Missed non-linear rating interactions."),
        ("Random Forest Baseline", "0.952", "0.993", "SELECTED & REGISTERED. Highest CV F1 score and ROC-AUC."),
        ("Random Forest (Engineered)", "0.951", "0.993", "Rejected. Extra feature complexity did not improve F1 score.")
    ]
    for row_idx, row in enumerate(row_data, start=1):
        for col_idx, text in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            if row_idx == 2: # Selected
                cell.fill.fore_color.rgb = C_AQUA
            else:
                cell.fill.fore_color.rgb = C_PALE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(13)
            p.font.color.rgb = C_NAVY if row_idx == 2 else C_INK
            if col_idx in (1, 2):
                p.font.bold = True

    # Why Random Forest Card Below Table
    rf_card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.6))
    rf_card.fill.solid()
    rf_card.fill.fore_color.rgb = C_NAVY
    rf_card.line.fill.background()
    tf = rf_card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Why Random Forest Won:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_AQUA
    p2 = tf.add_paragraph()
    p2.text = "Passenger satisfaction is non-linear and interactive. For example, a 30-min delay is acceptable IF Wi-Fi and seat comfort are 5/5, but unacceptable IF Wi-Fi is 1/5. Random Forest captures these multi-feature interactions natively without manual transformation."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 6: VERIFIED TEST SET PERFORMANCE (EVIDENCE)
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_bg(slide6, C_PALE)
    add_header(slide6, "Verified Test Performance Evidence", "Evaluated on untouched 20% test set (25,976 passengers)")
    add_footer(slide6, 6)

    # 4 Metric Cards
    metrics = [
        ("96.0%", "Accuracy", "Overall correct predictions"),
        ("95.4%", "F1 Score", "Harmonic mean of precision & recall"),
        ("94.7%", "Recall", "Catches dissatisfied passengers"),
        ("0.994", "ROC-AUC", "Excellent threshold separation")
    ]
    for i, (val, name, sub) in enumerate(metrics):
        x = Inches(0.8 + i * 2.98)
        box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(2.8), Inches(1.8))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_TEAL
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        p2 = tf.add_paragraph()
        p2.text = name
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(11)
        p3.font.color.rgb = C_MUTED

    # Confusion Matrix Image Left / ROC Curve Right
    cm_path = "reports/figures/confusion_matrix.png"
    roc_path = "reports/figures/roc_curve.png"
    if os.path.exists(cm_path):
        slide6.shapes.add_picture(cm_path, Inches(0.8), Inches(3.6), Inches(5.7), Inches(3.1))
    if os.path.exists(roc_path):
        slide6.shapes.add_picture(roc_path, Inches(6.833), Inches(3.6), Inches(5.7), Inches(3.1))

    # -------------------------------------------------------------
    # SLIDE 7: MLOPS ARCHITECTURE & SYSTEM STACK
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_bg(slide7, C_WHITE)
    add_header(slide7, "End-to-End MLOps Architecture", "Decoupled microservice architecture from versioning to serving")
    add_footer(slide7, 7)

    # Architecture Cards
    stack_items = [
        ("DVC (Data Version Control)", "Tracks raw CSV lineage & orchestrates 4-stage pipeline DAG (dvc.yaml).", C_TEAL),
        ("MLflow Tracking & Registry", "Logs experiments, metrics, artifacts, and registers AirlineSenseClassifier in sqlite.", C_NAVY),
        ("FastAPI Microservice (:8000)", "Serves REST endpoints (/health, /predict) with Pydantic boundary validation.", C_TEAL),
        ("Streamlit Console (:8501)", "Decoupled customer support interface communicating purely over HTTP POST.", C_NAVY),
        ("Docker & GitHub Actions", "Multi-stage container packaging + automated pytest CI/CD workflow.", C_ORANGE)
    ]
    for i, (title, desc, color) in enumerate(stack_items):
        y = Inches(1.6 + i * 1.05)
        box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.9))
        box.fill.solid()
        box.fill.fore_color.rgb = C_PALE
        box.line.color.rgb = color
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = C_INK
        p2.space_before = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 8: LIVE PRODUCT DEMONSTRATION
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_bg(slide8, C_PALE)
    add_header(slide8, "Live Product Demonstration", "Real-time HTTP interaction between Streamlit UI and FastAPI pipeline")
    add_footer(slide8, 8)

    # Demo Flow Steps Left Column
    demo_box = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.1))
    demo_box.fill.solid()
    demo_box.fill.fore_color.rgb = C_WHITE
    demo_box.line.color.rgb = C_TEAL
    tf = demo_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LIVE DEMO SEQUENCE"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    demo_steps = [
        ("1. Verify API Badge", "Streamlit confirms live connection to FastAPI on port 8000."),
        ("2. Baseline Prediction", "High rating inputs -> Returns 'Satisfied' (99.99% prob)."),
        ("3. Interactive Stress Test", "Lower Wi-Fi/Boarding & add 60m delay -> Model flips to 'Dissatisfied'."),
        ("4. Operational Action", "Agent triggers instant lounge pass or service recovery.")
    ]
    for title, desc in demo_steps:
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_before = Pt(10)
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = C_MUTED

    # UI Screenshot Right Column
    if os.path.exists(ui_img_path):
        slide8.shapes.add_picture(ui_img_path, Inches(5.5), Inches(1.6), Inches(7.0), Inches(5.1))

    # -------------------------------------------------------------
    # SLIDE 9: END-TO-END SUMMARY & CONCLUSION
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_bg(slide9, C_TEAL_DARK)

    # Cover Text Box
    tb9 = slide9.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.733), Inches(5.5))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "AirlineSense: End-to-End Product Summary"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    takeaways = [
        ("Business Impact", "Transforms passive survey feedback into real-time dissatisfaction alerts for proactive customer retention."),
        ("ML Engineering Rigor", "Zero data leakage via strict sklearn pipeline encapsulation fitted only on training folds."),
        ("MLOps Lifecycle", "Fully automated stack combining DVC versioning, MLflow registry, FastAPI, Streamlit, Docker, and GitHub Actions."),
        ("Verified Metrics", "Achieved 96.0% Accuracy, 95.4% F1, and 0.994 ROC-AUC on an untouched test set of 25,976 passengers.")
    ]
    for title, desc in takeaways:
        p_t = tf9.add_paragraph()
        p_t.text = f"✔  {title}"
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = C_AQUA
        p_t.space_before = Pt(18)
        p_d = tf9.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(14)
        p_d.font.color.rgb = C_WHITE
        p_d.space_before = Pt(2)

    # Save Presentation
    output_path = "outputs/AirlineSense_Pitch_Deck_Feature_MLOps_Final.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint pitch deck at {output_path}")

if __name__ == "__main__":
    create_deck()
