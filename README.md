# 厦门大学小学期Python课程作业 - 古籍下载器 (Ancient Text Downloader)

## 项目简介 (Project Introduction)

本项目是一个使用 Python 和 Tkinter 图形用户界面库开发的桌面应用程序，旨在从古诗词网 (gushici.net) 爬取并下载中国古籍。用户可以通过图形界面浏览可下载的古籍列表，选择并下载感兴趣的书籍，下载内容将保存为本地 TXT 文件。

This project is a desktop application developed using Python and the Tkinter GUI library as part of a Xiamen University Summer Semester Python course assignment. Its purpose is to scrape and download ancient Chinese texts (古籍) from the website gushici.net. Users can browse a list of available books via the GUI, select desired books for download, and the content will be saved locally as TXT files.

## 项目背景 (Project Context)

*   **课程名称 (Course Name):** 厦门大学小学期Python课程 (Xiamen University Summer Semester Python Course)
*   **作业类型 (Assignment Type):** 课程设计/项目作业 (Course Design / Project Assignment)
*   **目标 (Goal):** 实践 Python 编程、网络爬虫技术 (requests, lxml)、文件操作以及图形用户界面设计 (Tkinter)。

## 主要功能 (Features)

1.  **获取古籍列表 (Fetch Book List):**
    *   自动从 `gushici.net` 网站爬取所有分页的古籍名称和对应的链接。
    *   首次运行时获取列表，并将其缓存到 `poem_data.json` 文件中，以加快后续启动速度。
    *   提供 "刷新列表" 按钮，可以强制重新从网站获取最新的古籍列表。
2.  **图形用户界面 (Graphical User Interface):**
    *   使用 Tkinter 构建，提供直观的操作界面。
    *   左侧列表框显示所有可供下载的古籍名称。
    *   用户可以在输入框中输入想要下载的古籍名称。
    *   右侧列表框实时显示当前下载任务的进度（按章节/篇目显示）。
    *   下方列表框显示已经成功下载过的古籍名称。
3.  **古籍下载 (Book Download):**
    *   根据用户输入的古籍名称，查找对应的链接。
    *   访问该古籍的主页面，获取其包含的所有章节或篇目列表。
    *   逐一访问每个章节/篇目的链接，提取正文内容。
    *   将所有章节/篇目的内容追加写入到一个以该古籍名称命名的 `.txt` 文件中。
4.  **下载记录 (Download Tracking):**
    *   将已成功下载的古籍名称记录在 `downloaded_poems.txt` 文件中。
    *   在界面上显示已下载列表，并防止重复下载同一本书籍。
5.  **进度显示 (Progress Display):**
    *   在下载过程中，每下载完成一个章节/篇目，就在进度列表框中显示一条信息。

## 环境要求 (Requirements)

*   Python 3.x
*   第三方库 (Third-party Libraries):
    *   `requests`: 用于发送 HTTP 请求获取网页内容。
    *   `lxml`: 用于解析 HTML 网页内容，提取数据。

## 安装依赖 (Install Dependencies)

在运行脚本前，请确保已安装所需库：

```bash
pip install requests lxml
