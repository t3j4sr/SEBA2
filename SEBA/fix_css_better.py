import os
import glob
import re

static_dir = r"c:\Users\t3j4s\OneDrive\Desktop\Teju\Bday\SEBA\SEBA\static"
html_files = glob.glob(os.path.join(static_dir, "*.html"))

improved_css = """
    /* Universal Mobile Polish injected automatically v2 */
    html, body { overflow-x: hidden; width: 100%; }
    * { word-wrap: break-word; }
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
        input, select, .btn-submit { width: 100% !important; box-sizing: border-box; } /* FIXED: removed global 'button' */
        .toggle-pw { width: auto !important; right: 0.2rem !important; padding: 0.5rem !important; }
        .card, .stat-card { padding: 1rem !important; overflow: hidden; }
        .chart-wrap { height: 180px !important; }
        .cc-visual { width: 100% !important; height: auto !important; aspect-ratio: 1.58; }
    }
"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Remove the previous v1 injected CSS
    pattern = r"\s*/\*\s*Universal Mobile Polish injected automatically\s*\*/.*?</style>"
    content = re.sub(pattern, "\n</style>", content, flags=re.DOTALL)
    
    # Step 2: Remove v2 just in case it's run twice
    pattern2 = r"\s*/\*\s*Universal Mobile Polish injected automatically v2\s*\*/.*?</style>"
    content = re.sub(pattern2, "\n</style>", content, flags=re.DOTALL)

    # Step 3: Inject the improved CSS before the LAST </style> tag in the file
    pieces = content.rsplit("</style>", 1)
    if len(pieces) == 2:
        new_content = pieces[0] + improved_css + "</style>" + pieces[1]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {os.path.basename(filepath)}")
