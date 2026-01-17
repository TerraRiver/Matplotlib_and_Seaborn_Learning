import os
from pathlib import Path

# ================= 配置区域 =================

# 定义目录结构 (相对于当前位置)
DIRS = [
    "data/raw",          # 原始数据 (只读)
    "data/interim",      # 中间数据
    "data/processed",    # 最终用于模型的数据
    "data/external",     # 外部来源数据
    "notebooks",         # Jupyter Notebooks
    "references/literature", # 参考文献
    "results/figures",   # 图片输出
    "results/tables",    # 表格输出
    "results/logs",      # 运行日志
    "src/data",          # 数据处理脚本
    "src/models",        # 模型逻辑
    "src/visualization", # 绘图逻辑
    "scripts",           # 独立的批处理脚本 (可选)
]

# 定义核心文件的初始内容
FILES_CONTENT = {
    "README.md": """# 项目名称

## 研究背景
在此处简要描述研究问题...

## 项目结构
- `data/`: 数据存放 (注意：原始数据在 raw 中，永远不要手动修改)
- `notebooks/`: 探索性分析与实验
- `src/`: 核心代码逻辑 (数据清洗、模型、绘图)
- `results/`: 自动生成的图表
""",

    ".gitignore": """
# ==========================
# 1. Python & uv 核心环境 (Core)
# ==========================
# 编译产生的缓存文件 (必须忽略)
__pycache__/
*.py[cod]
*$py.class
# uv 创建的虚拟环境 (千万别上传，体积大且跨平台不兼容)
.venv/
env/
venv/
# 如果你习惯在项目里放本地的环境变量文件 (包含API Key等机密信息，严禁上传！)
.env
.env.local
# ==========================
# 2. uv 专属配置
# ==========================
# uv 的构建缓存（一般在系统层级，但如果改到了项目里，需忽略）
.uv_cache/
# 注意：以下两个文件必须保留（不要忽略）！
# !pyproject.toml
# !uv.lock
# !.python-version
# ==========================
# 3. 数据层安全 (Data Safety)
# ==========================
# 原则：代码上传，但数据不上传（特别是 raw 数据）
# 忽略 data 下的所有内容...
data/*
# ...但是！保留文件夹结构本身 (配合 .gitkeep 使用)
!data/.gitkeep
!data/raw/.gitkeep
!data/interim/.gitkeep
!data/processed/.gitkeep
!data/external/.gitkeep
# 如果你有非常小的外部字典或配置数据(比如 <1MB)，可以设立例外规则：
# !data/external/small_config.csv
# ==========================
# 4. 结果与输出 (Generated Artifacts)
# ==========================
# 结果应该是代码跑出来的，不需要版本控制
results/figures/*
results/tables/*
results/logs/*
# 同样保留文件夹结构
!results/figures/.gitkeep
!results/tables/.gitkeep
!results/logs/.gitkeep
# ==========================
# 5. Jupyter Notebooks (Lab/Experiment)
# ==========================
# Jupyter 的自动保存记录
.ipynb_checkpoints/
# 如果你不想上传具体的 notebook 输出图表（只传代码），可以使用 nbstripout 工具
# 但通常 CSS 项目为了展示过程，会保留 .ipynb 本身
# ==========================
# 6. 编辑器与系统垃圾 (OS/IDE Junk)
# ==========================
.DS_Store
Thumbs.db
.vscode/
.idea/
# ==========================
# 7. 兼容性文件 (Optional)
# ==========================
# 如果你是纯 uv 项目，requirements.txt 属于导出产物，可以忽略。
# 但为了兼容不用 uv 的人，也可以选择上传。
# requirements.txt
""",

    "requirements.txt": """# 依赖库文件
""",

    # 这里的 config.py 能够自动识别当前项目根目录
    "src/config.py": """
from pathlib import Path

# 获取项目根目录 (假设 config.py 位于 src/ 下，根目录就是它的上级再上级)
# 这里指向的是包含 src 文件夹的那个目录
PROJECT_DIR = Path(__file__).resolve().parents[1]

# 数据路径
DATA_DIR = PROJECT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
INTERIM_DATA_DIR = DATA_DIR / "interim"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# 结果路径
FIGURES_DIR = PROJECT_DIR / "results" / "figures"
TABLES_DIR = PROJECT_DIR / "results" / "tables"

# 确保核心目录存在 (防止手动删除后报错)
for path in [DATA_DIR, FIGURES_DIR, TABLES_DIR]:
    path.mkdir(parents=True, exist_ok=True)
""",

    "src/utils.py": """
import pandas as pd
from pathlib import Path

def get_project_root() -> Path:
    \"\"\"返回项目根目录\"\"\"
    return Path(__file__).resolve().parents[1]

def load_data(filename: str, folder="raw"):
    \"\"\"
    辅助函数：从 data 目录读取文件
    用法: df = load_data("my_data.csv", folder="processed")
    \"\"\"
    # 避免循环导入，这里重新计算路径或导入 config
    from src import config
    
    base_path = config.DATA_DIR / folder
    file_path = base_path / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件未找到: {file_path}")
        
    if filename.endswith('.csv'):
        return pd.read_csv(file_path)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(file_path)
    # 根据需要添加更多格式 (dta, sav 等)
    return None
""",

    "src/__init__.py": "",
    "src/data/__init__.py": "",
    "src/models/__init__.py": "",
    "src/visualization/__init__.py": "",
}

# ================= 执行逻辑 =================

def init_project_structure():
    # 获取当前工作目录
    current_path = Path.cwd()
    
    print(f"🚀 正在当前目录初始化项目结构: {current_path}")
    print(f"⚠️  注意：已存在的文件将被跳过，不会覆盖。\n")

    confirm = input("确认继续吗？(y/n): ")
    if confirm.lower() != 'y':
        print("已取消。")
        return

    # 1. 创建文件夹
    print("\n[1/3] 创建目录结构...")
    for folder in DIRS:
        dir_path = current_path / folder
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {folder}/")
            
            # 在空文件夹里创建一个 .gitkeep，否则 git 不会追踪空文件夹
            (dir_path / ".gitkeep").touch()
        else:
            print(f"  ⏭️  Skipped: {folder}/ (已存在)")

    # 2. 创建核心文件
    print("\n[2/3] 生成核心文件...")
    for filename, content in FILES_CONTENT.items():
        file_path = current_path / filename
        
        # 只有文件不存在时才写入
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"  ✅ Created: {filename}")
        else:
            print(f"  ⏭️  Skipped: {filename} (已存在)")

    print("\n[3/3] 完成！")
    print("="*30)
    print("💡 建议接下来的操作：")
    print("   1. 把你的数据放入 data/raw/")
    print("   2. 运行 'pip install -r requirements.txt'")
    print("   3. 启动 Jupyter Lab 开始研究")
    print("="*30)

if __name__ == "__main__":
    init_project_structure()