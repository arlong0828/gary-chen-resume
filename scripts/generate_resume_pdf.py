from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/Gary-Cheng-Resume.pdf"
pdfmetrics.registerFont(TTFont("CJK", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
NAVY, TEAL, GOLD = colors.HexColor("#17384A"), colors.HexColor("#0D8F95"), colors.HexColor("#D99A2B")
INK, MUTED, LINE, PALE = colors.HexColor("#24323A"), colors.HexColor("#60717A"), colors.HexColor("#D8E0E3"), colors.HexColor("#F3F7F7")
s = getSampleStyleSheet()
for name, size, leading, color, align in [("RName",24,29,NAVY,TA_CENTER),("RRole",10.5,15,TEAL,TA_CENTER),("RContact",8.3,13,MUTED,TA_CENTER),("RSection",12.5,17,NAVY,0),("RTitle",10.3,15,INK,0),("RMeta",8.3,12,MUTED,0),("RBody",8.8,13.5,INK,0),("RBullet",8.6,13.2,INK,0)]:
    s.add(ParagraphStyle(name=name, fontName="CJK", fontSize=size, leading=leading, textColor=color, alignment=align, spaceAfter=3, leftIndent=10 if name=="RBullet" else 0, firstLineIndent=-7 if name=="RBullet" else 0))

def page(canvas, doc):
    w, h = A4; canvas.saveState(); canvas.setFillColor(NAVY); canvas.rect(0,h-7*mm,w,7*mm,fill=1,stroke=0)
    canvas.setStrokeColor(LINE); canvas.line(16*mm,13*mm,w-16*mm,13*mm); canvas.setFont("CJK",7.5); canvas.setFillColor(MUTED)
    canvas.drawString(16*mm,8.5*mm,"鄭樺駿 Gary Cheng｜軟體工程師"); canvas.drawRightString(w-16*mm,8.5*mm,str(doc.page)); canvas.restoreState()

def section(t):
    rule=Table([[""]],colWidths=[178*mm],rowHeights=[.6*mm],style=TableStyle([("BACKGROUND",(0,0),(-1,-1),TEAL)]))
    return [Spacer(1,3*mm),Paragraph(t,s["RSection"]),rule,Spacer(1,2*mm)]

def block(title, meta, items):
    x=[Paragraph(f"<b>{title}</b>",s["RTitle"]),Paragraph(meta,s["RMeta"])]
    x += [Paragraph(f"• {i}",s["RBullet"]) for i in items]; x.append(Spacer(1,1.5*mm)); return KeepTogether(x)

def build():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc=BaseDocTemplate(str(OUT),pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=14*mm,bottomMargin=18*mm,title="鄭樺駿 Gary Cheng｜軟體工程師履歷",author="鄭樺駿 Gary Cheng")
    doc.addPageTemplates(PageTemplate(id="resume",frames=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id="body"),onPage=page))
    story=[Paragraph("鄭樺駿 <font color='#D99A2B'>Gary Cheng</font>",s["RName"]),Paragraph("軟體工程師｜智慧物流系統・企業 AI／LLM・全端開發",s["RRole"]),Paragraph("arlongchen082557@gmail.com　｜　github.com/arlong0828　｜　gary-cheng.com　｜　新北市",s["RContact"])]
    story+=section("專業摘要")+[Paragraph("具備智慧物流系統與企業 AI 實務經驗，負責 WMS、WCS、LMS 的開發、整合與維護。熟悉 Laravel、FastAPI、Vue 3、異質資料庫同步、PLC 通訊及 Docker CI/CD；並設計全本地 SOPRAG 架構，將知識圖譜、混合式檢索及可查核證據機制應用於企業 SOP 問答。",s["RBody"])]
    story+=section("核心技能")
    rows=[("程式語言","Python、PHP、TypeScript／JavaScript、SQL、Java"),("後端／前端","Laravel 12、FastAPI、Vue 3、Vite、Pinia、Tailwind CSS、Celery"),("資料與平台","Oracle、MSSQL、MySQL、PostgreSQL、Redis、Docker、GitHub Actions、Git"),("AI／檢索","LLM、GraphRAG、Qwen3.6 35B、ChromaDB、BGE-large-zh、RAGAS、BERTScore"),("設備整合","Siemens S7（snap7）、Mitsubishi SLMP、WebSocket、REST API")]
    tab=Table([[Paragraph(f"<b>{a}</b>",s["RBody"]),Paragraph(b,s["RBody"])] for a,b in rows],colWidths=[29*mm,149*mm]); tab.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),PALE),("GRID",(0,0),(-1,-1),.35,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("PADDING",(0,0),(-1,-1),5)])); story.append(tab)
    story+=section("工作經歷")+[Paragraph("<b>軟體工程師｜嘉泰興股份有限公司</b>",s["RTitle"]),Paragraph("2025/10 — 現在｜電腦系統整合服務業｜台北市中山區｜管理 4 人以下",s["RMeta"])]
    story += [
      block("企業 SOP 智能問答系統","Python・本地 LLM・GraphRAG",["設計 SOPRAG 檢索架構，以 Qwen3.6 35B + LM Studio 全本地部署，企業文件零外流。","為 24 份 SOP、308 筆事實建立五種知識圖譜，整合 ChromaDB／BGE-large-zh 混合檢索與圖專家動態加權。","以證據編號、低信心擴檢索與 LLM 自我修正降低幻覺；使用 RAGAS、BERTScore、ROUGE-L／BLEU-4、消融實驗及 HITL 評估。"]),
      block("倉儲管理系統（WMS）","PHP 8.2・Laravel 12・Vue 3・Oracle・MSSQL・Redis",["開發入庫、出庫、庫存與庫位核心流程；整合 Oracle 主庫與客戶 MSSQL ERP 雙向同步，隔離 ERP 異常以維持現場作業。","將單體拆分為 5 個獨立版控 Composer package。","以 Redis 佇列串接自製 Rust 列印程式，並整合本地 Ollama 倉儲問答。"]),
      block("倉儲控制系統（WCS）","FastAPI・Celery・Siemens S7・Mitsubishi SLMP",["建置 WMS 至自動化設備的控制層，支援堆垛機、輸送帶及穿梭車。","隔離設備輪詢、心跳與任務派工，實作退避重試、快速失敗、狀態機及分段逾時。"]),
      block("標籤管理系統（LMS）","FastAPI・Vue 3・Konva・Docker",["以 Canvas 拖放排版打造視覺化標籤設計器，提供條碼與 QR Code 即時預覽。","支援 Excel 批次匯入與自動套版，並以 Docker + nginx 容器化部署。"]),
      block("CI/CD 與開發流程標準化","GitHub Actions・Docker・Bash／PowerShell・Git Hooks",["為 WMS、LMS、WCS 建立兩段式 CI/CD、環境分流、並發控管與部署閘門。","建立 101 份跨 AI 工具規範、跨平台建置腳本、5 道同步防線、12 個內部指令及 OpenSpec 規格流程。"])
    ]
    story+=section("精選專案")+[
      block("碩士論文｜智慧物流路徑最佳化","2024/11–2025/06｜Applied Soft Computing 投稿｜2025 崇越論文大賞特優",["解決二層級、多倉庫、多日、多時期、容量限制且具同時取送需求之車輛路徑問題。","提出 Hybrid NSGA-II，結合 3D K-Means、Clarke-Wright 儲蓄法與 Local Search，同時最小化營運成本與車輛數。"]),
      block("無人化商店實作","Django・SQLite・Keras CNN・OpenCV・Azure Face API",["整合商品辨識、人臉驗證與刷臉支付；以約 1,000 張商品影像訓練 CNN，辨識準確率達 95% 以上。"]),
      block("Noty 智能筆記工具","PHP・MySQL・JavaScript・Flask",["支援帳號、分類、收藏、垃圾桶及分享，並整合中英文關鍵字分析與視覺化圖表。"])
    ]
    story+=section("學歷、證照與語言")
    for a,b in [("2023/09–2025/08","國立高雄科技大學｜資訊管理學系 碩士"),("2019/09–2023/06","國立澎湖科技大學｜資訊管理系 學士"),("證照／獎項","OCA Java SE 8｜2025 第十八屆崇越論文大賞特優"),("語言","中文：精通｜英文：中等｜日文：略懂")]: story.append(KeepTogether([Paragraph(a,s["RMeta"]),Paragraph(b,s["RBody"]),Spacer(1,1*mm)]))
    doc.build(story); print(OUT)

if __name__=="__main__": build()
