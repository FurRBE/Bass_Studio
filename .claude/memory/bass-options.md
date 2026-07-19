---
name: bass-options
description: 贝斯定制配置选项 — 8 个分类及内容
metadata:
  type: reference
---

# 贝斯配置选项

定制器有 8 个分类，按固定顺序展示。基础价 5000 元，各选项价格累加。

| 分类 (category) | 中文名 | 选项数 | 默认项 (price=0) |
|-----------------|--------|--------|-------------------|
| body | 琴体木材 | 5 | Alder/赤杨木 |
| neck | 琴颈木材 | 4 | Maple/枫木 |
| fingerboard | 指板材质 | 4 | Maple/枫木 |
| pickup | 拾音器 | 5 | Standard Single Coil |
| bridge | 琴桥 | 4 | Standard Fixed |
| finish | 颜色/漆面 | 6 | Natural/原木色 |
| strings | 弦数 | 3 | 4-String |
| handedness | 左右手 | 2 | Right Hand |

## 价格范围

- 最低配：5000 (全部默认)
- 最高配：约 15800 (全选最贵选项)
- 各分类价格跨度：0 ~ 2000 元

## 数据初始化

`backend/init_data.py` 中的 `BASS_OPTIONS` 列表定义了所有选项。初始化时检查 `category + name` 是否已存在，存在则跳过（支持增量添加）。

## options API

- `GET /api/options` — 返回所有启用的选项，按预定义 category_order 排列
- `GET /api/options/{category}` — 按分类获取

**Why:** 定制器是项目的核心功能，了解配置选项结构对前后端修改都很关键。
**How to apply:** 添加新选项时修改 init_data.py 的 BASS_OPTIONS 列表并重新运行，前端 CATEGORY_LABELS 若新增分类需同步更新。
