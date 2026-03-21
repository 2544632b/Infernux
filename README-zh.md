<p align="center">
  <img src="docs/assets/logo.png" alt="InfernuxEngine Logo" width="128" />
</p>

<h1 align="center">InfernuxEngine</h1>

<p align="center">
  <strong>开源游戏引擎 · C++17 / Vulkan · Python 脚本 · MIT 协议</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/version-0.1.0-orange.svg" alt="Version" />
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey.svg" alt="Platform" />
  <img src="https://img.shields.io/badge/python-3.12+-brightgreen.svg" alt="Python" />
  <img src="https://img.shields.io/badge/C%2B%2B-17-blue.svg" alt="C++ 17" />
  <img src="https://img.shields.io/badge/graphics-Vulkan-red.svg" alt="Vulkan" />
</p>

<p align="center">
  <a href="README.md">🇬🇧 English</a> · <a href="#快速开始">快速开始</a> · <a href="#架构">架构</a> · <a href="https://chenlizheme.github.io/InfEngine/">网站</a>
</p>

---

## 项目简介

InfernuxEngine 是一个从零开始构建的游戏引擎，使用 **C++17 / Vulkan 运行时**和 **Python 脚本层**。C++ 负责渲染、物理和资源管理；Python 负责玩法逻辑、编辑器工具和内容工作流。

主要特点：

- **C++17 / Vulkan 核心** — 前向/延迟渲染、PBR、RenderGraph 管线、Jolt 物理
- **Python 脚本** — 类 Unity 组件模型、热重载、编辑器扩展、Python 生态直接可用
- **MIT 协议** — 无版税、无运行时费用、完全开源

---

## 设计立场

### 渲染可编排

渲染管线通过 RenderGraph API 对外开放。你可以用 Python 编写和修改渲染 Pass，而不是面对一个封闭的编辑器黑箱。

### 快速迭代

Python 不只处理玩法代码，也负责编辑器扩展、资产工作流和工具开发，让内循环尽可能短。

### 无授权顾虑

MIT 协议。无版税、无运行时费用、无供应商锁定。

---

## 功能

### 运行时基础

- Vulkan 前向与延迟渲染
- PBR 材质、级联阴影、MSAA、后处理
- 基于 RenderGraph 的 Pass 编排
- Jolt 物理（刚体 + 碰撞体）
- 输入、音频基础、场景与资源系统

### Python 层

- 类 Unity 的组件生命周期
- `serialized_field` 元数据，支持 Inspector 编辑
- 组件依赖与编辑器执行的装饰器
- 脚本和内容热重载
- 完整接入 Python 生态

### 编辑器

- Hierarchy、Inspector、Scene View、Game View、Console、Project 面板
- 选择、Gizmo、撤销重做、Play 模式场景隔离

---

## C++ / Python 分层

| 层 | 角色 |
|---|---|
| C++17 / Vulkan | 渲染、场景系统、资源、物理、平台服务 |
| pybind11 | 原生系统与 Python API 之间的绑定层 |
| Python | 玩法、编辑器逻辑、渲染编排、工具开发 |

---

## 快速开始

### 环境要求

| 依赖 | 版本 |
|:-----|:-----|
| Windows | 10 / 11（64 位） |
| Python | 3.12+ |
| Vulkan SDK | 1.3+ |
| CMake | 3.22+ |
| Visual Studio | 2022（MSVC v143） |
| pybind11 | 2.11+ |

说明：

- `python packaging/launcher.py` 是开发模式入口，使用你当前的 Python 环境。
- 打包后的 Hub 是另一条独立分发链路，它会为终端用户维护一套私有的 Python 3.12 运行时。
- 当前官方预编译 wheel 面向 Windows，现阶段发布链以 `win_amd64` 为主。

### 克隆仓库

```bash
git clone --recurse-submodules https://github.com/ChenlizheMe/InfEngine.git
cd InfEngine
```

如果克隆时没有带子模块：

```bash
git submodule update --init --recursive
```

### 构建

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cmake --preset release
cmake --build --preset release
```

构建流程会生成原生 Python 模块、复制运行时依赖，并把包安装到当前工作区环境里，之后即可直接 `import InfEngine`。

### 运行

```bash
python packaging/launcher.py
```

这是 Hub 的开发模式运行方式。在这个模式下：

- 不需要安装器
- 不会安装 Hub 私有运行时
- 项目的 `.venv` 会基于当前 Python 解释器创建
- 创建项目仍然要求 `dist/` 里存在预编译好的 InfEngine wheel

### 测试

```bash
cd python
python -m pytest test/ -v
```

---

## Hub 打包与分发

现在 Hub 有两条明确分开的分发方式。

### 1. 裸目录打包

```bash
cmake --build --preset packaging
```

这会生成 PyInstaller 输出目录：`dist/InfEngine Hub/`。

适合用于：

- 开发者本地验证打包版是否能启动
- 快速分发一个便携目录
- 在没有安装器工具链时作为后备方案

这种方式下：

- Hub 仍然可以在首次启动时为自己准备 Python 3.12
- 运行时准备发生在第一次启动阶段
- 这是后备路径，不是推荐的终端用户安装方式

### 2. Windows 安装器

```bash
cmake --build --preset packaging-installer
```

这会生成一个正式的图形化 Windows 安装器可执行文件。

这个目标现在会直接生成一个可双击运行的图形化安装器。

适合用于：

- 让 Hub 像标准桌面软件一样被安装
- 在安装阶段根据当前机器架构下载对应的 Python 3.12 安装包
- 把 Hub 私有 Python 安装到 `InfEngineHubData/python312`
- 在安装阶段就提前准备好可复用的 venv 模板

### 安装器依赖

安装器目标现在直接使用仓库现有的 Python 打包链路。

- 不再需要额外安装 Windows 安装器制作工具
- 日常源码开发仍然不需要运行安装器目标
- `packaging-installer` 会直接依赖 `packaging` 产出的 Hub 目录作为载荷

### 安装器行为

安装器本身就是图形化程序，并会直接完成这些步骤：

- 检测当前主机架构
- 下载匹配的 Python 3.12 安装包
- 把 Python 安装到 Hub 私有数据目录
- 预先准备一个可复用的 venv 模板

### 安装器说明

InfEngine Hub 安装器这部分并不是我目前最熟悉的方向，因此当前安装器相关流程是在 AI 辅助下完成的。

目前这条安装器技术栈包括：

- 使用 PyInstaller 生成 Hub 裸目录
- 使用 PyInstaller 生成图形化安装器可执行文件
- 使用 PySide6 编写安装器界面
- 按机器架构下载 Python 官方 Windows 安装包

如果你发现问题、边界情况，或者有更合理的 Windows 安装器实践，欢迎提 Issue。

### 当前架构说明

Python 运行时安装器已经可以按机器架构选择，但引擎分发最终还受你发布的 wheel 限制。

也就是说，如果未来你要完整支持非 `amd64` 机器，除了下载匹配架构的 Python，还需要同时发布对应架构的 InfEngine wheel。

---

## Hub 运行时模型

现在 Hub 已经明确区分开发模式和安装模式。

### 开发模式

- 通过 `python packaging/launcher.py` 启动
- 使用当前 Python 环境
- 不安装 Hub 私有运行时
- 使用本地构建产物和本地 wheel

### 安装版 Hub

- 从打包应用启动
- 使用 `InfEngineHubData/` 下的私有 Python 3.12
- 只在首次准备时生成一次共享 venv 模板
- 创建新项目时优先复制这个模板，从而提升速度
- 复制模板后，再安装用户为该项目选择的 InfEngine 版本

这意味着共享模板里只包含 Python 本身，不会预装某个固定版本的 InfEngine wheel。因为用户是在创建项目时按项目选择引擎版本的。

---

## 架构

```text
Python 创作层
  -> 编辑器面板、组件系统、RenderGraph 编排、工具工作流
  -> pybind11 绑定接缝
C++ 引擎核心
  -> 渲染器、场景、资源、物理、音频、平台服务
外部技术栈
  -> Vulkan、SDL3、Jolt、ImGui、Assimp、GLM、glslang、VMA
```

### 实际工作流

1. 用 Python 编写玩法或渲染逻辑。
2. 绑定到编辑器可见的数据和场景对象。
3. 通过 RenderGraph API 描述渲染 Pass。
4. 原生后端负责调度、内存管理和 GPU 执行。

---

## 当前状态

### 已完成

- 渲染与渲染管线
- Python 脚本与编辑器集成
- 编辑器核心创作流程
- 资产标识与项目启动
- 物理集成与场景交互

### 进行中

- Prefab 工作流
- UI 管线
- 动画系统
- 独立构建与导出
- Hub 安装器与分发链路工程化
- 大规模项目的生产化完善

---

## 路线图

| 版本 | 重点 |
|:-----|:-----|
| v0.1 | **当前** — 脚本、渲染、物理、编辑器均可用，已支持开发不含动画的基础游戏 |
| v0.2 | Prefab 工作流、UI 完善、资产重命名改进 |
| v0.3 | 动画系统、模型/内容管线 |
| v0.4 | 独立构建、粒子、地形 |
| v1.0 | 文档、示例、生产就绪 |

---

## 仓库结构

```text
cpp/infengine/        原生引擎运行时
python/InfEngine/     Python 引擎层与编辑器系统
packaging/            启动器与项目管理工具
docs/                 网站与生成文档入口
external/             第三方依赖与子模块
dev/                  规划文档与内部设计记录
```

---

## 参与贡献

1. 先读 README 和文档站。
2. 查看路线图了解当前优先级。
3. 大改动前请先开 Issue 或 Discussion。
4. 提交目标明确的 Pull Request。

---

## 致谢

- 架构方向受到王希 [GAMES104](https://games104.boomingtech.com/) 课程启发
- 使用了 [Jolt Physics](https://github.com/jrouwe/JoltPhysics)、[SDL3](https://github.com/libsdl-org/SDL)、[Dear ImGui](https://github.com/ocornut/imgui)、[Assimp](https://github.com/assimp/assimp)、[GLM](https://github.com/g-truc/glm)、[glslang](https://github.com/KhronosGroup/glslang) 与 [VulkanMemoryAllocator](https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator)

---

## 联系方式

- 作者：Lizhe Chen
- 邮箱：[chenlizheme@outlook.com](mailto:chenlizheme@outlook.com)
- GitHub：[https://github.com/ChenlizheMe/InfEngine](https://github.com/ChenlizheMe/InfEngine)

## 许可证

MIT 协议。详见 [LICENSE](LICENSE)。
