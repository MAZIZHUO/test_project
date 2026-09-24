# Simulated Data Visualization Analysis

这是一个使用模拟电商经营数据完成的数据可视化分析示例。项目强调可重复、可封装和一键运行。

## 一键运行

```powershell
uv run main.py
```

运行后会在 `outputs/` 中生成：

- `analysis_report.md`：中文分析报告与图表引用
- `charts/`：月度趋势、地区收入、渠道 ROI、渠道投入产出关系图
- `data/`：模拟明细数据和三个汇总 CSV
- `summary.json`：本次运行的核心结果摘要

## 项目结构

```text
main.py                         # 一键启动入口
simulated_analysis/
  config.py                     # 参数配置
  data.py                       # 模拟数据生成
  analysis.py                   # 指标汇总与计算
  visualization.py              # 图表生成
  report.py                     # Markdown 报告
  pipeline.py                   # 流程编排
```

数据为方法演示用途，不代表真实市场证据。随机种子写在 `AnalysisConfig` 中，保持每次运行结果可复现。
