# System Architecture

## 1. Overview

The GitHub MCP Assistant uses the Model Context Protocol (MCP) as the interface between an AI model and GitHub.

The MCP server exposes GitHub capabilities as standardized tools that an AI assistant can discover and invoke.

The system is designed with security, reliability, observability, and evaluation in mind.

---

## 2. High-Level Architecture

```text
                         ┌─────────────────┐
                         │      User       │
                         └────────┬────────┘
                                  │
                                  │ Natural Language
                                  ▼
                         ┌─────────────────┐
                         │       LLM       │
                         │  Tool Selection │
                         └────────┬────────┘
                                  │
                                  │ MCP
                                  ▼
                         ┌─────────────────┐
                         │   MCP Client    │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │       MCP Server         │
                    │         Python           │
                    │                          │
                    │  ┌────────────────────┐  │
                    │  │    MCP Tools       │  │
                    │  │                    │  │
                    │  │ Repository         │  │
                    │  │ Issues             │  │
                    │  │ Pull Requests      │  │
                    │  │ Files              │  │
                    │  │ Search             │  │
                    │  └─────────┬──────────┘  │
                    │            │             │
                    │  ┌─────────▼──────────┐  │
                    │  │   Safety Layer     │  │
                    │  │   Confirmation     │  │
                    │  └─────────┬──────────┘  │
                    │            │             │
                    │  ┌─────────▼──────────┐  │
                    │  │   Error Handling   │  │
                    │  └─────────┬──────────┘  │
                    └────────────┼─────────────┘
                                 │
                                 ▼
                       ┌─────────────────────┐
                       │     GitHub API      │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ GitHub Repository   │
                       └─────────────────────┘