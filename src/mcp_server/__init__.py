"""
MCP Server - Model Context Protocol Server Implementation

A production-ready MCP server with tool execution, resource management,
and protocol support for AI assistants.
"""

__version__ = "1.0.0"
__author__ = "MCP Server Team"
__license__ = "MIT"

from .server import MCPServer, create_server
from .tools import Tool, ToolRegistry, ToolResult
from .protocol import MCPProtocol, MCPRequest, MCPResponse
from .transport import Transport, StdioTransport, HTTPTransport

__all__ = [
    "__version__",
    "MCPServer",
    "create_server",
    "Tool",
    "ToolRegistry",
    "ToolResult",
    "MCPProtocol",
    "MCPRequest",
    "MCPResponse",
    "Transport",
    "StdioTransport",
    "HTTPTransport",
]
