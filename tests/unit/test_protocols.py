"""
Unit tests for protocol functionality.

---
description: Test protocol functionality
endpoints: [test_protocols]
inputs: []
outputs: []
dependencies: [pytest]
auth: none
alwaysApply: false
---
"""

import os
import pytest
from labeeb.protocols.a2a_protocol import A2AProtocol
from labeeb.protocols.agent_protocol import AgentProtocol
from labeeb.utils.platform_utils import ensure_labeeb_directories

@pytest.fixture
def a2a_protocol():
    """Create an A2A protocol instance."""
    return A2AProtocol()

@pytest.fixture
def agent_protocol():
    """Create an agent protocol instance."""
    return AgentProtocol()

def test_a2a_protocol_initialization(a2a_protocol):
    """Test A2A protocol initialization."""
    assert a2a_protocol is not None
    assert isinstance(a2a_protocol, A2AProtocol)

def test_agent_protocol_initialization(agent_protocol):
    """Test agent protocol initialization."""
    assert agent_protocol is not None
    assert isinstance(agent_protocol, AgentProtocol)

def test_a2a_protocol_handshake(a2a_protocol):
    """Test A2A protocol handshake."""
    # Test successful handshake
    result = a2a_protocol.perform_handshake()
    assert result["status"] == "success"
    assert "session_id" in result
    
    # Test handshake with invalid credentials
    a2a_protocol.credentials = {"invalid": "credentials"}
    result = a2a_protocol.perform_handshake()
    assert result["status"] == "error"
    assert "Invalid credentials" in result["message"]

def test_a2a_protocol_message_exchange(a2a_protocol):
    """Test A2A protocol message exchange."""
    # Perform handshake first
    a2a_protocol.perform_handshake()
    
    # Test sending message
    message = {"type": "request", "content": "Hello"}
    result = a2a_protocol.send_message(message)
    assert result["status"] == "success"
    assert "message_id" in result
    
    # Test receiving message
    response = a2a_protocol.receive_message(result["message_id"])
    assert response["status"] == "success"
    assert "content" in response

def test_agent_protocol_command_execution(agent_protocol):
    """Test agent protocol command execution."""
    # Test valid command
    result = agent_protocol.execute_command("calculate", {"expression": "2 + 2"})
    assert result["status"] == "success"
    assert result["result"] == 4
    
    # Test invalid command
    result = agent_protocol.execute_command("invalid_command", {})
    assert result["status"] == "error"
    assert "Unknown command" in result["message"]

def test_agent_protocol_state_management(agent_protocol):
    """Test agent protocol state management."""
    # Test setting state
    agent_protocol.set_state("active", True)
    assert agent_protocol.get_state("active") is True
    
    # Test getting non-existent state
    assert agent_protocol.get_state("non_existent") is None
    
    # Test clearing state
    agent_protocol.clear_state("active")
    assert agent_protocol.get_state("active") is None

def test_a2a_protocol_error_handling(a2a_protocol):
    """Test A2A protocol error handling."""
    # Test connection error
    a2a_protocol.connection = None
    result = a2a_protocol.send_message({"type": "request", "content": "Hello"})
    assert result["status"] == "error"
    assert "Connection error" in result["message"]
    
    # Test timeout
    a2a_protocol.timeout = 0.001
    result = a2a_protocol.receive_message("non_existent_id")
    assert result["status"] == "error"
    assert "Timeout" in result["message"]

def test_agent_protocol_error_handling(agent_protocol):
    """Test agent protocol error handling."""
    # Test invalid command parameters
    result = agent_protocol.execute_command("calculate", {})
    assert result["status"] == "error"
    assert "Missing required parameter" in result["message"]
    
    # Test command execution error
    result = agent_protocol.execute_command("calculate", {"expression": "2 / 0"})
    assert result["status"] == "error"
    assert "Division by zero" in result["message"]

def test_a2a_protocol_security(a2a_protocol):
    """Test A2A protocol security features."""
    # Test message encryption
    message = {"type": "request", "content": "Secret message"}
    encrypted = a2a_protocol.encrypt_message(message)
    assert encrypted != message
    assert isinstance(encrypted, str)
    
    # Test message decryption
    decrypted = a2a_protocol.decrypt_message(encrypted)
    assert decrypted == message
    
    # Test invalid encryption
    with pytest.raises(ValueError):
        a2a_protocol.decrypt_message("invalid_encrypted_message")

def test_agent_protocol_security(agent_protocol):
    """Test agent protocol security features."""
    # Test command validation
    result = agent_protocol.execute_command("calculate", {"expression": "os.system('rm -rf /')"})
    assert result["status"] == "error"
    assert "Invalid command" in result["message"]
    
    # Test state isolation
    agent_protocol.set_state("sensitive_data", "secret")
    other_protocol = AgentProtocol()
    assert other_protocol.get_state("sensitive_data") is None

def test_a2a_protocol_performance(a2a_protocol):
    """Test A2A protocol performance."""
    import time
    
    # Test message exchange performance
    start_time = time.time()
    for _ in range(100):
        message = {"type": "request", "content": "Test message"}
        result = a2a_protocol.send_message(message)
        a2a_protocol.receive_message(result["message_id"])
    end_time = time.time()
    
    # Should complete within 5 seconds
    assert end_time - start_time < 5.0

def test_agent_protocol_performance(agent_protocol):
    """Test agent protocol performance."""
    import time
    
    # Test command execution performance
    start_time = time.time()
    for _ in range(100):
        agent_protocol.execute_command("calculate", {"expression": "2 + 2"})
    end_time = time.time()
    
    # Should complete within 5 seconds
    assert end_time - start_time < 5.0 