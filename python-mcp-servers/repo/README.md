# Repo MCP Server (Python)

🐍 Repository analysis and structure mapping MCP server for Auckland Library legacy system modernization.

## 概述

这是一个**独立的程序**，实现了MCP（Model Context Protocol）服务器：

- **程序类型**: 独立的Python进程
- **通信方式**: 通过stdin/stdout与Claude等AI客户端通信
- **功能**: 提供仓库分析工具给CodeUnderstandingAgent使用

```
Claude等AI客户端 ←→ Repo MCP Server (这个程序) ←→ Git仓库/文件系统
```

## 功能特性

### 🔍 仓库分析
- **结构分析**: 文件统计、目录结构、代码行数
- **语言检测**: 自动识别编程语言及占比
- **框架识别**: 检测Express.js、MongoDB、Solr等技术栈
- **架构模式**: 识别MVC、分层架构等模式

### 📁 文件管理
- **文件分类**: 自动分类源码、配置、测试、文档文件
- **目录树**: 生成层次化的文件结构
- **入口点**: 识别应用程序入口文件

### 📈 Git分析
- **提交历史**: 获取提交统计和变更信息
- **分支分析**: 分析活跃和过期分支
- **贡献者**: 统计开发者贡献情况

## 安装和使用

### 1. 安装依赖
```bash
cd /Users/ianzhou/19_project/python-mcp-servers/repo
pip install -r requirements.txt
```

### 2. 运行MCP服务器
```bash
python main.py
```

服务器启动后会通过stdio等待MCP客户端连接。

### 3. 测试功能
```bash
python test_mcp_server.py
```

## 可用工具 (Tools)

### `analyze_structure`
分析仓库整体结构和指标

**参数:**
- `repo_path` (string): 仓库路径

**返回:** 完整的仓库结构分析，包括文件统计、语言分布、架构模式等

### `detect_frameworks`  
检测使用的框架和技术栈

**参数:**
- `repo_path` (string): 仓库路径

**返回:** 按类别分类的框架检测结果（前端、后端、数据库、测试工具）

### `classify_files`
按用途分类文件

**参数:**
- `repo_path` (string): 仓库路径  

**返回:** 文件分类结果（源码、配置、文档、测试等）

### `get_file_tree`
获取层次化文件树

**参数:**
- `repo_path` (string): 仓库路径
- `max_depth` (integer, 可选): 最大遍历深度

**返回:** 树形文件结构

### `identify_entry_points`
识别应用程序入口点

**参数:**
- `repo_path` (string): 仓库路径

**返回:** 入口点列表及其类型

### 其他工具
- `get_commit_history`: 获取Git提交历史
- `analyze_branches`: 分析分支结构  
- `get_contributors`: 获取贡献者统计
- `find_config_files`: 查找配置文件

## 与CodeUnderstandingAgent集成

这个MCP服务器专门为奥克兰图书馆遗留系统分析设计：

1. **发现阶段**: `analyze_structure` 获取系统概览
2. **技术栈识别**: `detect_frameworks` 识别当前技术
3. **代码组织**: `classify_files` 和 `get_file_tree` 理解代码结构  
4. **迁移规划**: `identify_entry_points` 和 `find_config_files` 制定现代化计划
5. **团队上下文**: `get_contributors` 了解开发历史

## 性能特点

- ⚡ 30秒内完成典型遗留仓库分析
- 📊 支持10万行代码规模的仓库
- 💾 内存高效的文件遍历
- 🔧 针对奥克兰图书馆技术栈优化

## 错误处理

服务器提供全面的错误处理：
- 无效仓库路径检查
- 权限问题处理
- Git仓库损坏检测  
- 大文件处理优化
- 网络超时处理

所有错误都包含描述性消息以便排错。

## MCP协议

此服务器实现了标准的MCP协议：
- **list_tools**: 返回可用工具列表
- **call_tool**: 执行指定工具并返回结果
- **stdio通信**: 通过标准输入输出与客户端通信

## 示例输出

```json
{
  "total_files": 15,
  "total_directories": 8,
  "languages": [
    {"language": "JavaScript", "files": 8, "percentage": 65.2},
    {"language": "JSON", "files": 3, "percentage": 20.1}
  ],
  "architecture": {
    "type": "layered",
    "confidence": 85,
    "indicators": ["Express.js server found", "MVC structure"]
  }
}
```

---

这就是一个完整的MCP服务器程序！它作为独立进程运行，为AI客户端提供仓库分析能力。