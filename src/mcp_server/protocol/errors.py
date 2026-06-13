"""
MCP Protocol Error Definitions

Implements JSON-RPC 2.0 error codes for the Model Context Protocol.
Error codes follow the MCP specification and JSON-RPC 2.0 standard.
"""

from typing import Optional, Any, Dict
from dataclasses import dataclass, field
from enum import IntEnum


class MCPCode(IntEnum):
    """MCP protocol error codes."""
    # JSON-RPC 2.0 reserved codes (-32768 to -32000)
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    # MCP-specific error codes (-32000 to -32099)
    CONNECTION_CLOSED = -32000
    TIMEOUT = -32001
    RATE_LIMITED = -32002
    AUTHENTICATION_FAILED = -32003
    AUTHORIZATION_FAILED = -32004
    TOOL_NOT_FOUND = -32010
    TOOL_EXECUTION_FAILED = -32011
    AGENT_ERROR = -32020
    INVALID_STATE = -32021
    VALIDATION_ERROR = -32022


@dataclass
class MCPError:
    """
    MCP Protocol Error with code, message, and optional data.
    
    Follows JSON-RPC 2.0 error object specification:
    https://www.jsonrpc.org/specification#error_object
    """
    code: int
    message: str
    data: Optional[Any] = None
    http_status: int = 500

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to JSON-RPC 2.0 error object."""
        result = {
            "code": self.code,
            "message": self.message,
        }
        if self.data is not None:
            result["data"] = self.data
        return result

    def to_jsonrpc_response(self, request_id: Optional[Any] = None) -> Dict[str, Any]:
        """Create a JSON-RPC 2.0 error response."""
        response = {
            "jsonrpc": "2.0",
            "error": self.to_dict(),
        }
        if request_id is not None:
            response["id"] = request_id
        return response


class MCPErrorMixin:
    """Mixin class providing convenient error creation methods."""

    @staticmethod
    def parse_error(message: str = "Parse error", data: Any = None) -> MCPError:
        """Invalid JSON was received by the server."""
        return MCPError(
            code=MCPCode.PARSE_ERROR,
            message=message,
            data=data,
            http_status=400,
        )

    @staticmethod
    def invalid_request(message: str = "Invalid Request", data: Any = None) -> MCPError:
        """The JSON sent is not a valid Request object."""
        return MCPError(
            code=MCPCode.INVALID_REQUEST,
            message=message,
            data=data,
            http_status=400,
        )

    @staticmethod
    def method_not_found(method: str, data: Any = None) -> MCPError:
        """The method does not exist or is not available."""
        return MCPError(
            code=MCPCode.METHOD_NOT_FOUND,
            message=f"Method not found: {method}",
            data=data,
            http_status=404,
        )

    @staticmethod
    def invalid_params(message: str = "Invalid params", data: Any = None) -> MCPError:
        """Invalid method parameter(s)."""
        return MCPError(
            code=MCPCode.INVALID_PARAMS,
            message=message,
            data=data,
            http_status=400,
        )

    @staticmethod
    def internal_error(message: str = "Internal error", data: Any = None) -> MCPError:
        """Internal MCP server error."""
        return MCPError(
            code=MCPCode.INTERNAL_ERROR,
            message=message,
            data=data,
            http_status=500,
        )

    @staticmethod
    def tool_not_found(tool_name: str, data: Any = None) -> MCPError:
        """The requested tool does not exist."""
        return MCPError(
            code=MCPCode.TOOL_NOT_FOUND,
            message=f"Tool not found: {tool_name}",
            data=data,
            http_status=404,
        )

    @staticmethod
    def tool_execution_failed(
        tool_name: str,
        reason: str,
        data: Any = None
    ) -> MCPError:
        """Tool execution failed."""
        return MCPError(
            code=MCPCode.TOOL_EXECUTION_FAILED,
            message=f"Tool execution failed: {tool_name}",
            data={"tool": tool_name, "reason": reason, "details": data},
            http_status=500,
        )

    @staticmethod
    def agent_error(
        agent_name: str,
        message: str,
        data: Any = None
    ) -> MCPError:
        """Agent processing error."""
        return MCPError(
            code=MCPCode.AGENT_ERROR,
            message=f"Agent error in {agent_name}: {message}",
            data=data,
            http_status=500,
        )

    @staticmethod
    def timeout(operation: str, timeout_seconds: float) -> MCPError:
        """Operation timed out."""
        return MCPError(
            code=MCPCode.TIMEOUT,
            message=f"Operation timed out: {operation} (timeout: {timeout_seconds}s)",
            data={"operation": operation, "timeout_seconds": timeout_seconds},
            http_status=504,
        )

    @staticmethod
    def rate_limited(retry_after: Optional[int] = None) -> MCPError:
        """Rate limit exceeded."""
        return MCPError(
            code=MCPCode.RATE_LIMITED,
            message="Rate limit exceeded",
            data={"retry_after": retry_after},
            http_status=429,
        )

    @staticmethod
    def validation_error(
        field: str,
        message: str,
        value: Any = None
    ) -> MCPError:
        """Request validation failed."""
        return MCPError(
            code=MCPCode.VALIDATION_ERROR,
            message=f"Validation error on field '{field}': {message}",
            data={"field": field, "message": message, "value": value},
            http_status=400,
        )


# Convenience singleton for creating errors
mcperror = MCPErrorMixin()
