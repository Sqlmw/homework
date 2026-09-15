# B站推荐页视频主题分析

## 📌 项目简介

本项目基于 Python 爬取 B 站首页个性化推荐视频，并对视频标题进行数据清洗、中文分词和词频统计，最终通过词频柱状图与词云图分析推荐视频的主题特征。

主要流程：

**数据获取 → 数据清洗 → 中文分词 → 词频统计 → 可视化**

---

## 📂 项目结构

```text
├── spider.py                  # B站推荐视频爬虫及 WBI 签名
├── analysis.ipynb             # 数据分析与可视化
├── bilibili_recommend.csv     # 爬取生成的推荐视频数据
└── README.md                  # 项目说明
```

---

## 🛠️ 环境与依赖

### 基础环境

* Python 3.9
* Anaconda
* VS Code / Jupyter Notebook

### 创建环境

```bash
conda create -n bili_homework python=3.9 -y
conda activate bili_homework
```

### 安装依赖

```bash
pip install requests pandas jieba wordcloud matplotlib numpy
```

| 依赖库          | 用途          |
| ------------ | ----------- |
| `requests`   | 网络请求        |
| `pandas`     | 数据读取与处理     |
| `jieba`      | 中文分词        |
| `wordcloud`  | 词云生成        |
| `matplotlib` | 图表绘制        |
| `numpy`      | 数值计算及词云辅助处理 |

---

## 🔑 Cookie 配置

B站推荐接口需要登录状态及 WBI 签名验证，因此运行爬虫前需要配置个人 Cookie。

### 获取 Cookie

1. 浏览器登录 B 站。
2. 按 `F12` 打开开发者工具，进入 **Console（控制台）**。
3. 输入：

```javascript
document.cookie
```

4. 复制返回的 Cookie 字符串。

### 配置 Cookie

打开 `spider.py`，找到：

```python
if __name__ == '__main__':
    MY_COOKIE = "YOUR_COOKIE_HERE"
    get_bilibili_recommend(MY_COOKIE)
```

将 `YOUR_COOKIE_HERE` 替换为自己的 Cookie。

> Cookie 属于个人登录凭证，请勿上传至公开仓库。

**提交作业前，请将 Cookie 恢复为：**

```python
MY_COOKIE = "YOUR_COOKIE_HERE"
```

---

## 🚀 运行项目

### 1. 获取推荐视频数据

确保已经激活环境并配置 Cookie：

```bash
conda activate bili_homework
python spider.py
```

运行成功后将生成：

```text
bilibili_recommend.csv
```

默认保存 200 条推荐视频标题。

### 2. 数据分析

使用 VS Code 或 Jupyter Notebook 打开：

```text
analysis.ipynb
```

选择 `Python (bili_homework)` 内核后，执行 **Restart Kernel and Run All Cells**。

Notebook 将完成：

* 数据清洗
* 中文分词
* 高频词统计
* TOP15 主题词展示
* 词频柱状图绘制
* 词云图生成

运行完成后保存 `analysis.ipynb`，即可保留分析结果。

---

## ⚠️ 注意事项

* 未配置有效 Cookie 时，推荐接口可能返回 `412` 或 `-400` 等错误。
* `bilibili_recommend.csv` 已提供，因此无需运行爬虫也可以直接进行 Notebook 分析。
* 不要将包含真实 Cookie 的 `spider.py` 提交或上传至公开仓库。
* 如果 Notebook 提示缺少模块，请确认当前 Python 内核为 `bili_homework` 环境。
