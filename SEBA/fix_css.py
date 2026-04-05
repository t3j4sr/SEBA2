import os
import glob

static_dir = r"c:\Users\t3j4s\OneDrive\Desktop\Teju\Bday\SEBA\SEBA\static"
html_files = glob.glob(os.path.join(static_dir, "*.html"))

responsive_css_fixes = """
    /* Universal Mobile Polish injected automatically */
    html, body { overflow-x: hidden; width: 100%; }
    * { word-wrap: break-word; } /* Prevent text overflow */
    @media(max-width: 768px){
        nav { padding: 0.8rem 1rem !important; flex-wrap: wrap; }
        .nav-links { gap: 0.3rem !important; }
        main { padding: 1.5rem 1rem 6rem !important; }
        .stats-row, .charts-grid, .grid2, .cards-grid, .tips-row, .emi-slider-row, .emi-grid, .cc-grid, .pred-grid { grid-template-columns: 1fr !important; }
        .chart-card.full, .card, .stat-card { grid-column: span 1 !important; width: 100% !important; margin: 0 auto !important; box-sizing: border-box !important;}
        .stat-card .value { font-size: 1.5rem !important; }
        .tx-item, .insight-card { flex-direction: column !important; align-items: flex-start !important; padding: 1rem !important;}
        .tx-icon, .insight-icon { margin-bottom: 0.5rem !important; }
        h1, h2 { font-size: 1.4rem !important; word-wrap: break-word; }
        .hero-title { font-size: 2rem !important; }
        .hero-desc { font-size: 0.9rem !important; width: 100% !important; }
        table { display: block; overflow-x: auto; white-space: nowrap; }
    }
    @media(max-width: 480px){
        .nav-link { padding: 0.3rem 0.5rem !important; font-size: 0.75rem !important; }
        .logo { font-size: 1rem !important; }
        input, select, button { width: 100% !important; box-sizing: border-box; }
        .card, .stat-card { padding: 1rem !important; overflow: hidden; }
        .chart-wrap { height: 180px !important; }
        .cc-visual { width: 100% !important; height: auto !important; aspect-ratio: 1.58; }
    }
"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject before </style>
    if "</style>" in content and "Universal Mobile Polish" not in content:
        content = content.replace("</style>", f"{responsive_css_fixes}\n</style>")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {os.path.basename(filepath)}")
