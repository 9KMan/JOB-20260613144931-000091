"""
MCP Protocol Error Classes

Implements the Model Context Protocol error handling with proper JSON-RPC 2.0
error codes and error definitions as specified in the MCP specification.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import json


# MCP Error Codes (matching JSON-RPC 2.0 base + MCP-specific extensions)
MCP_ERROR_PARSE_ERROR = -32700
MCP_ERROR_INVALID_REQUEST = -32600
MCP_ERROR_METHOD_NOT_FOUND = -32601
MCP_ERROR_INVALID_PARAMS = -32602
MCP_ERROR_INTERNAL_ERROR = -32603

# MCP-specific error codes (in range -32000 to -32099 as per JSON-RPC 2.0)
MCP_ERROR_CONNECTION_FAILED = -32000
MCP_ERROR_PROTOCOL_ERROR = -32001
MCP_ERROR_REQUEST_CANCELLED = -32002
MCP_ERROR_CONTENT_TRUNCATED = -32003
MCP_ERROR_TOOL_NOT_FOUND = -32004
MCP_ERROR_TOOLExecution_FAILED = -32005
MCP_ERROR_INVALID_TOOL_INPUT = -32006
MCP_ERROR_SESSION_NOT_FOUND = -32007
MCP_ERROR_SERVER_NOT_INITIALIZED = -32008
MCP_ERROR_RESOURCE_NOT_FOUND = -32009
MCP_ERROR_RESOURCE_ALREADY_EXISTS = -32010
MCP_ERROR_SAMPLING_FAILED = -32011
MCP_ERROR_PROMPT_NOT_FOUND = -32012


@dataclass
class MCPError:
    """Base MCP Protocol Error class."""
    
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if not isinstance(self.code, int):
            raise TypeError("Error code must be an integer")
        if not isinstance(self.message, str):
            raise TypeError("Error message must be a string")
        if self.data is not None and not isinstance(self.data, dict):
            raise TypeError("Error data must be a dictionary or None")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to JSON-RPC 2.0 error response format."""
        result = {
            "code": self.code,
            "message": self.message,
        }
        if self.data is not None:
            result["data"] = self.data
        return result
    
    def to_jsonrpc_response(self, request_id: Optional[Any] = None) -> Dict[str, Any]:
        """Convert to a full JSON-RPC 2.0 error response."""
        response = {
            "jsonrpc": "2.0",
            "error": self.to_dict(),
        }
        if request_id is not None:
            response["id"] = request_id
        return response


class ParseError(MCPError):
    """Invalid JSON was received by the server."""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_PARSE_ERROR,
            message="Parse error - Invalid JSON",
            data=data
        )


class InvalidRequest(MCPError):
    """The JSON sent is not a valid Request object."""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_INVALID_REQUEST,
            message="Invalid Request",
            data=data
        )


class MethodNotFound(MCPError):
    """The method does not exist or is not available."""
    
    def __init__(self, method: str, data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_METHOD_NOT_FOUND,
            message=f"Method not found: {method}",
            data=data
        )


class InvalidParams(MCPError):
    """Invalid method parameter(s)."""
    
    def __init__(self, message: str = "Invalid parameters", data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_INVALID_PARAMS,
            message=message,
            data=data
        )


class InternalError(MCPError):
    """Internal MCP server error."""
    
    def __init__(self, message: str = "Internal error", data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_INTERNAL_ERROR,
            message=message,
            data=data
        )


class ConnectionFailedError(MCPError):
    """Failed to connect to external service or resource."""
    
    def __init__(self, message: str = "Connection failed", data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_CONNECTION_FAILED,
            message=message,
            data=data
        )


class ProtocolError(MCPError):
    """Protocol violation or malformed message."""
    
    def __init__(self, message: str = "Protocol error", data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_PROTOCOL_ERROR,
            message=message,
            data=data
        )


class RequestCancelledError(MCPError):
    """The request was cancelled by the client."""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_REQUEST_CANCELLED,
            message="Request cancelled",
            data=data
        )


class ContentTruncatedError(MCPError):
    """Response content was truncated due to size limits."""
    
    def __init__(self, limit: Optional[int] = None, actual_size: Optional[int] = None):
        super().__init__(
            code=MCP_ERROR_CONTENT_TRUNCATED,
            message="Content was truncated",
            data={"limit": limit, "actual_size": actual_size} if limit or actual_size else None
        )


class ToolNotFoundError(MCPError):
    """The requested tool does not exist."""
    
    def __init__(self, tool_name: str, data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_TOOL_NOT_FOUND,
            message=f"Tool not found: {tool_name}",
            data=data
        )


class ToolExecutionFailedError(MCPError):
    """Tool execution failed."""
    
    def __init__(self, tool_name: str, reason: str, data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_TOOLExecution_FAILED,
            message=f"Tool execution failed: {reason}",
            data={"tool_name": tool_name, **(data or {})}
        )


class InvalidToolInputError(MCPError):
    """Tool input validation failed."""
    
    def __init__(self, tool_name: str, validation_errors: Dict[str, Any], data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_INVALID_TOOL_INPUT,
            message=f"Invalid input for tool {tool_name}",
            data={"tool_name": tool_name, "validation_errors": validation_errors, **(data or {})}
        )


class ServerNotInitializedError(MCPError):
    """Server received a request before initialization."""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_SERVER_NOT_INITIALIZED,
            message="Server not initialized",
            data=data
        )


class ResourceNotFoundError(MCPError):
    """The requested resource does not exist."""
    
    def __init__(self, uri: str, data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_RESOURCE_NOT_FOUND,
            message=f"Resource not found: {uri}",
            data={"uri": uri, **(data or {})}
        )


class SamplingFailedError(MCPError):
    """LLM sampling failed."""
    
    def __init__(self, message: str = "Sampling failed", data: Optional[Dict[str, Any]] = None):
        super().__init__(
            code=MCP_ERROR_SAMPLING_FAILED,
            message=message,
            data=data
        )


def error_from_exception(exc: Exception, include_traceback: bool = False) -> MCPError:
    """Convert an exception to an appropriate MCPError.
    
    Args:
        exc: The exception to convert
        include_traceback: Whether to include the traceback in error data
        
    Returns:
        The appropriate MCPError subclass for the exception
    """
    import traceback
    
    error_mapping = {
        ValueError: lambda e: InvalidParams(str(e)),
        TypeError: lambda e: InvalidParams(str(e)),
        KeyError: lambda e: InvalidParams(f"Missing required key: {str(e)}"),
        NotImplementedError: lambda e: MethodNotFound(str(e)),
        TimeoutError: lambda e: ConnectionFailedError(f"Request timed out: {str(e)}"),
    }
    
    for exc_type, error_factory in error_mapping.items():
        if isinstance(exc, exc_type):
            error = error_factory(exc)
            if include_traceback:
                error.data = error.data or {}
                error.data["traceback"] = traceback.format_exc()
            return error
    
    # Default to InternalError for unhandled exceptions
    error = InternalError(str(exc))
    if include_traceback:
        error.data = error.data or {}
        error.data["traceback"] = traceback.format_exc()
    return error
