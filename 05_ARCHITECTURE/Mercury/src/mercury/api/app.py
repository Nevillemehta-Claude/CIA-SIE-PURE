"""
Mercury FastAPI Application
===========================

Web interface for Mercury - LLM as Financial Market Cognitive Interface.

DIRECTIVE: UI/UX execution to the highest design and efficiency standards.
STANDARD: Zero-Defect | Glitch-free operation.

AUTONOMOUS ENHANCEMENTS:
- Background health monitoring with WebSocket broadcasting
- OAuth endpoints for Kite re-authentication
- Rate limiter status endpoints
"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from mercury.core.config import get_settings
from mercury.core.startup import (
    LaunchReadiness,
    ServiceStatus,
    perform_launch_readiness_check,
)
from mercury.core.health import get_system_health
from mercury.core.logging import get_logger, setup_logging
from mercury.core.monitor import get_health_monitor, start_health_monitor, stop_health_monitor
from mercury.core.rate_limiter import get_all_limiter_status
from mercury.core.persistence import get_state_store, ConversationRecord, shutdown_state_store
from mercury.core.shutdown import get_shutdown_handler, save_state_on_shutdown
from mercury.core.metrics import get_metrics_registry, get_mercury_metrics
from mercury.core.alerting import get_alert_manager, Alert, AlertSeverity, WebhookConfig
from mercury.kite.oauth_manager import get_oauth_manager, TokenExpiredError
from mercury.chat.engine import ChatEngine
from mercury.chat.conversation import ConversationManager
from mercury.attachments import get_attachment_manager, get_supported_formats

logger = get_logger("mercury.api")


# Request/Response Models
class QueryRequest(BaseModel):
    """User query request."""
    query: str
    conversation_id: Optional[str] = None
    attachment_ids: Optional[list[str]] = None  # Include specific attachments in context


class QueryResponse(BaseModel):
    """AI response."""
    response: str
    conversation_id: str
    timestamp: str
    data_sources: list[str] = []


# Global state
_readiness: Optional[LaunchReadiness] = None
_chat_engine: Optional[ChatEngine] = None
_conversations: dict[str, ConversationManager] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager with state persistence."""
    global _readiness, _chat_engine, _conversations
    
    # Startup
    logger.info("Starting Mercury API...")
    
    # Initialize state store
    state_store = get_state_store()
    await state_store.initialize()
    logger.info("State persistence initialized")
    
    # Load previous conversations from storage
    try:
        saved_convs = await state_store.list_conversations(limit=10)
        for conv_record in saved_convs:
            manager = ConversationManager()
            conv = manager.create_conversation(conv_record.id)
            # Restore messages
            for msg in conv_record.messages:
                if msg.get("role") == "user":
                    conv.add_user_message(msg.get("content", ""))
                else:
                    conv.add_assistant_message(msg.get("content", ""))
            _conversations[conv_record.id] = manager
        if saved_convs:
            logger.info(f"Restored {len(saved_convs)} conversations from storage")
    except Exception as e:
        logger.warning(f"Failed to restore conversations: {e}")
    
    # Initialize and verify APIs
    _readiness = await perform_launch_readiness_check()
    
    if not _readiness.ready:
        logger.warning("System starting in degraded mode - some APIs not available")
    
    # Initialize chat engine
    _chat_engine = ChatEngine()
    
    # Start background health monitor
    await start_health_monitor()
    logger.info("Background health monitor started")
    
    # Setup graceful shutdown
    shutdown_handler = get_shutdown_handler()
    shutdown_handler.register_handler(save_state_on_shutdown)
    shutdown_handler.install_signal_handlers()
    
    logger.info("Mercury API ready")
    
    yield
    
    # Shutdown - save all conversations
    logger.info("Shutting down Mercury API...")
    
    # Save all active conversations
    for conv_id, manager in _conversations.items():
        try:
            conv = manager.get_active_conversation()
            if conv:
                record = ConversationRecord(
                    id=conv_id,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                    messages=conv.get_history(),
                    metadata={},
                )
                await state_store.save_conversation(record)
        except Exception as e:
            logger.warning(f"Failed to save conversation {conv_id}: {e}")
    
    logger.info(f"Saved {len(_conversations)} conversations to storage")
    
    # Stop background health monitor
    await stop_health_monitor()
    logger.info("Background health monitor stopped")
    
    # Close state store
    await shutdown_state_store()
    logger.info("State persistence closed")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Mercury",
        description="LLM as Financial Market Cognitive Interface",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    # CORS - Allow frontend connections
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # =========================================================================
    # HEALTH & STATUS ENDPOINTS
    # =========================================================================
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "mercury",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    # =========================================================================
    # METRICS ENDPOINTS (Prometheus-style)
    # =========================================================================
    
    @app.get("/metrics")
    async def metrics():
        """
        Export metrics in Prometheus text format.
        
        For scraping by Prometheus or compatible monitoring systems.
        """
        registry = get_metrics_registry()
        return HTMLResponse(
            content=registry.to_prometheus(),
            media_type="text/plain; charset=utf-8",
        )
    
    @app.get("/api/metrics")
    async def metrics_json():
        """
        Export metrics in JSON format.
        
        For API consumption and dashboards.
        """
        registry = get_metrics_registry()
        return registry.to_json()
    
    # =========================================================================
    # ALERTING ENDPOINTS
    # =========================================================================
    
    @app.get("/api/alerts/webhooks")
    async def list_webhooks():
        """List configured alert webhooks."""
        manager = get_alert_manager()
        return {
            "webhooks": [
                {
                    "name": w.name,
                    "format": w.format,
                    "min_severity": w.min_severity.value,
                    "enabled": w.enabled,
                }
                for w in manager._webhooks
            ]
        }
    
    @app.post("/api/alerts/webhooks")
    async def add_webhook(
        name: str,
        url: str,
        format: str = "json",
        min_severity: str = "warning",
    ):
        """Add an alert webhook."""
        manager = get_alert_manager()
        
        severity_map = {
            "info": AlertSeverity.INFO,
            "warning": AlertSeverity.WARNING,
            "error": AlertSeverity.ERROR,
            "critical": AlertSeverity.CRITICAL,
        }
        
        config = WebhookConfig(
            name=name,
            url=url,
            format=format,
            min_severity=severity_map.get(min_severity, AlertSeverity.WARNING),
        )
        
        manager.add_webhook(config)
        await manager.start()  # Ensure worker is running
        
        return {"status": "added", "webhook": name}
    
    @app.delete("/api/alerts/webhooks/{name}")
    async def remove_webhook(name: str):
        """Remove an alert webhook."""
        manager = get_alert_manager()
        removed = manager.remove_webhook(name)
        
        return {
            "status": "removed" if removed else "not_found",
            "webhook": name,
        }
    
    @app.post("/api/alerts/test")
    async def test_alert(severity: str = "info", message: str = "Test alert from Mercury"):
        """Send a test alert to verify webhook configuration."""
        manager = get_alert_manager()
        
        severity_map = {
            "info": AlertSeverity.INFO,
            "warning": AlertSeverity.WARNING,
            "error": AlertSeverity.ERROR,
            "critical": AlertSeverity.CRITICAL,
        }
        
        alert = Alert(
            title="Test Alert",
            message=message,
            severity=severity_map.get(severity, AlertSeverity.INFO),
            source="test",
            context={"triggered_by": "api"},
        )
        
        await manager.send(alert)
        
        return {"status": "sent", "fingerprint": alert.fingerprint}
    
    # =========================================================================
    # ATTACHMENT ENDPOINTS
    # =========================================================================
    
    @app.get("/api/attachments/formats")
    async def attachment_formats():
        """Get supported attachment formats."""
        return {
            "formats": get_supported_formats(),
            "max_size_mb": 10,
            "max_per_conversation": 10,
        }
    
    @app.post("/api/attachments/upload")
    async def upload_attachment(
        file: UploadFile = File(...),
        conversation_id: Optional[str] = Form(None),
    ):
        """
        Upload a file attachment for analysis.
        
        Supported formats: CSV, Excel, JSON, Text, Images
        Max size: 10 MB
        """
        manager = get_attachment_manager()
        
        try:
            content = await file.read()
            
            attachment = await manager.upload(
                content=content,
                filename=file.filename or "unnamed",
                mime_type=file.content_type,
                conversation_id=conversation_id,
            )
            
            return {
                "status": "uploaded",
                "attachment": attachment.to_dict(),
                "context_preview": attachment.parsed.to_ai_context()[:500] if attachment.parsed else None,
            }
        
        except ValueError as e:
            return JSONResponse(
                status_code=400,
                content={"error": str(e)}
            )
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to process file"}
            )
    
    @app.get("/api/attachments")
    async def list_attachments(conversation_id: Optional[str] = None):
        """List attachments, optionally filtered by conversation."""
        manager = get_attachment_manager()
        
        if conversation_id:
            attachments = manager.get_for_conversation(conversation_id)
            return {
                "conversation_id": conversation_id,
                "attachments": [a.to_dict() for a in attachments],
            }
        else:
            return {
                "attachments": manager.list_all(),
            }
    
    @app.get("/api/attachments/{attachment_id}")
    async def get_attachment(attachment_id: str):
        """Get details of a specific attachment."""
        manager = get_attachment_manager()
        attachment = manager.get(attachment_id)
        
        if not attachment:
            return JSONResponse(
                status_code=404,
                content={"error": "Attachment not found"}
            )
        
        return {
            "attachment": attachment.to_dict(),
            "context": attachment.parsed.to_ai_context() if attachment.parsed else None,
            "statistics": attachment.parsed.get_statistics() if attachment.parsed else None,
        }
    
    @app.delete("/api/attachments/{attachment_id}")
    async def delete_attachment(attachment_id: str):
        """Delete an attachment."""
        manager = get_attachment_manager()
        deleted = await manager.delete(attachment_id)
        
        return {
            "status": "deleted" if deleted else "not_found",
            "attachment_id": attachment_id,
        }
    
    @app.get("/status")
    async def status():
        """Detailed system status."""
        global _readiness
        
        if _readiness is None:
            _readiness = await perform_launch_readiness_check()
        
        return {
            "ready": _readiness.ready,
            "kite": {
                "status": _readiness.kite_status.status.value if _readiness.kite_status else "unknown",
                "authenticated": _readiness.kite_status.authenticated if _readiness.kite_status else False,
                "message": _readiness.kite_status.message if _readiness.kite_status else "",
            },
            "anthropic": {
                "status": _readiness.anthropic_status.status.value if _readiness.anthropic_status else "unknown",
                "authenticated": _readiness.anthropic_status.authenticated if _readiness.anthropic_status else False,
                "message": _readiness.anthropic_status.message if _readiness.anthropic_status else "",
            },
            "errors": _readiness.errors,
            "warnings": _readiness.warnings,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    # =========================================================================
    # AUTONOMOUS INFRASTRUCTURE ENDPOINTS
    # =========================================================================
    
    @app.get("/api/monitor")
    async def monitor_status():
        """Get health monitor status."""
        monitor = get_health_monitor()
        return {
            "monitor": monitor.get_status(),
            "trend": monitor.get_health_trend(minutes=10),
            "rate_limiters": get_all_limiter_status(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    @app.websocket("/ws/health")
    async def websocket_health(websocket: WebSocket):
        """WebSocket endpoint for real-time health updates."""
        await websocket.accept()
        
        monitor = get_health_monitor()
        monitor.subscribe(websocket)
        
        try:
            # Send initial health status
            health = await get_system_health()
            await websocket.send_json({
                "type": "health_update",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "health": health.to_dict(),
            })
            
            # Keep connection alive, monitor will broadcast updates
            while True:
                try:
                    # Wait for any message (ping/pong or close)
                    data = await asyncio.wait_for(
                        websocket.receive_text(),
                        timeout=60.0,
                    )
                    # Handle ping
                    if data == "ping":
                        await websocket.send_text("pong")
                except asyncio.TimeoutError:
                    # Send keepalive
                    await websocket.send_json({"type": "keepalive"})
                    
        except WebSocketDisconnect:
            monitor.unsubscribe(websocket)
            logger.debug("Health WebSocket disconnected")
    
    # =========================================================================
    # OAUTH ENDPOINTS
    # =========================================================================
    
    @app.get("/auth/kite")
    async def kite_auth_start():
        """Redirect to Kite OAuth login."""
        oauth = get_oauth_manager()
        return RedirectResponse(url=oauth.login_url)
    
    @app.get("/auth/kite/callback")
    async def kite_auth_callback(
        request_token: str = Query(..., description="Request token from Kite"),
        status: str = Query(None, description="OAuth status"),
    ):
        """Handle Kite OAuth callback."""
        if status == "error":
            return HTMLResponse(
                content="""
                <html>
                <head><title>Kite Auth Failed</title></head>
                <body style="font-family: Arial; padding: 40px; text-align: center; background: #0a0a0f; color: #fff;">
                    <h1 style="color: #ef4444;">Authentication Failed</h1>
                    <p>The Kite authentication was cancelled or failed.</p>
                    <a href="/" style="color: #00d4aa;">Return to Mercury</a>
                </body>
                </html>
                """,
                status_code=400,
            )
        
        try:
            oauth = get_oauth_manager()
            token_info = await oauth.handle_oauth_callback(request_token)
            
            # Update the global readiness
            global _readiness
            _readiness = await perform_launch_readiness_check()
            
            return HTMLResponse(
                content=f"""
                <html>
                <head>
                    <title>Kite Connected</title>
                    <meta http-equiv="refresh" content="3;url=/" />
                </head>
                <body style="font-family: Arial; padding: 40px; text-align: center; background: #0a0a0f; color: #fff;">
                    <h1 style="color: #00d4aa;">✅ Successfully Connected</h1>
                    <p>Authenticated as <strong>{token_info.user_name or 'User'}</strong></p>
                    <p>Redirecting to Mercury...</p>
                    <a href="/" style="color: #00d4aa;">Click here if not redirected</a>
                </body>
                </html>
                """,
                status_code=200,
            )
            
        except Exception as e:
            logger.error(f"Kite OAuth callback failed: {e}")
            return HTMLResponse(
                content=f"""
                <html>
                <head><title>Kite Auth Failed</title></head>
                <body style="font-family: Arial; padding: 40px; text-align: center; background: #0a0a0f; color: #fff;">
                    <h1 style="color: #ef4444;">Authentication Failed</h1>
                    <p>{str(e)}</p>
                    <a href="/auth/kite" style="color: #00d4aa;">Try Again</a>
                </body>
                </html>
                """,
                status_code=500,
            )
    
    @app.get("/auth/kite/status")
    async def kite_auth_status():
        """Get Kite OAuth status."""
        oauth = get_oauth_manager()
        return oauth.get_status()
    
    # =========================================================================
    # CHAT ENDPOINTS
    # =========================================================================
    
    @app.post("/api/chat", response_model=QueryResponse)
    async def chat(request: QueryRequest):
        """
        Process a chat query.
        
        CONSTITUTIONAL: MR-002 - Response is UNRESTRICTED
        
        Supports file attachments for data analysis.
        """
        global _chat_engine, _conversations
        
        if _chat_engine is None:
            _chat_engine = ChatEngine()
        
        # Get or create conversation
        conv_id = request.conversation_id or f"conv_{datetime.now(timezone.utc).timestamp()}"
        if conv_id not in _conversations:
            # Create a ConversationManager and get/create a conversation
            manager = ConversationManager()
            conv = manager.create_conversation()
            _conversations[conv_id] = manager
        
        conversation = _conversations[conv_id].get_active_conversation()
        
        # Build attachment context if provided
        attachment_context = ""
        image_attachments = []
        data_sources = ["kite_api", "anthropic_api"]
        
        if request.attachment_ids:
            att_manager = get_attachment_manager()
            for att_id in request.attachment_ids:
                attachment = att_manager.get(att_id)
                if attachment and attachment.parsed:
                    # Check if it's an image (for vision)
                    if attachment.parsed.image_base64:
                        image_data = att_manager.get_image_for_vision(att_id)
                        if image_data:
                            image_attachments.append(image_data)
                    else:
                        # Add text-based context
                        context = att_manager.get_context(att_id)
                        if context:
                            attachment_context += f"\n\n{context}"
            
            if attachment_context or image_attachments:
                data_sources.append("attachments")
        
        # Also get any attachments associated with this conversation
        if conv_id:
            att_manager = get_attachment_manager()
            conv_context = att_manager.get_all_context(conv_id)
            if conv_context and conv_context not in attachment_context:
                attachment_context += f"\n\n{conv_context}"
        
        # Process query with attachment context
        try:
            response = await _chat_engine.process(
                query=request.query,
                conversation=conversation,
                attachment_context=attachment_context if attachment_context else None,
                image_attachments=image_attachments if image_attachments else None,
            )
            
            return QueryResponse(
                response=response,
                conversation_id=conv_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data_sources=data_sources,
            )
        
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return QueryResponse(
                response=f"I encountered an error processing your query: {str(e)}",
                conversation_id=conv_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data_sources=[],
            )
    
    @app.delete("/api/chat/{conversation_id}")
    async def clear_conversation(conversation_id: str):
        """Clear a conversation."""
        global _conversations
        
        if conversation_id in _conversations:
            del _conversations[conversation_id]
            return {"status": "cleared", "conversation_id": conversation_id}
        
        return {"status": "not_found", "conversation_id": conversation_id}
    
    # =========================================================================
    # WEBSOCKET FOR REAL-TIME CHAT
    # =========================================================================
    
    @app.websocket("/ws/chat")
    async def websocket_chat(websocket: WebSocket):
        """WebSocket endpoint for real-time chat."""
        global _chat_engine, _conversations
        
        await websocket.accept()
        
        conv_id = f"ws_{datetime.now(timezone.utc).timestamp()}"
        manager = ConversationManager()
        _conversations[conv_id] = manager
        conversation = manager.create_conversation()
        
        if _chat_engine is None:
            _chat_engine = ChatEngine()
        
        try:
            while True:
                # Receive message
                data = await websocket.receive_text()
                message = json.loads(data)
                
                query = message.get("query", "")
                
                if not query:
                    continue
                
                # Send typing indicator
                await websocket.send_json({
                    "type": "typing",
                    "status": "processing",
                })
                
                # Process query
                try:
                    response = await _chat_engine.process(
                        query=query,
                        conversation=conversation,
                    )
                    
                    await websocket.send_json({
                        "type": "response",
                        "content": response,
                        "conversation_id": conv_id,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "content": str(e),
                    })
        
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected: {conv_id}")
            if conv_id in _conversations:
                del _conversations[conv_id]
    
    # =========================================================================
    # FRONTEND - BEAUTIFUL UI
    # =========================================================================
    
    @app.get("/", response_class=HTMLResponse)
    async def frontend():
        """Serve the Mercury frontend."""
        return get_frontend_html()
    
    return app


def get_frontend_html() -> str:
    """
    Generate the Mercury frontend HTML.
    
    DIRECTIVE: UI/UX execution to the highest design and efficiency standards.
    """
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>☿ Mercury - Financial Market Intelligence</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-tertiary: #1a1a24;
            --bg-hover: #22222e;
            --accent-primary: #00d4aa;
            --accent-secondary: #00a8ff;
            --accent-tertiary: #8b5cf6;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b0;
            --text-muted: #606070;
            --border-color: #2a2a38;
            --success: #00d4aa;
            --warning: #fbbf24;
            --error: #ef4444;
            --gradient-1: linear-gradient(135deg, #00d4aa 0%, #00a8ff 100%);
            --gradient-2: linear-gradient(135deg, #8b5cf6 0%, #00a8ff 100%);
            --shadow-glow: 0 0 40px rgba(0, 212, 170, 0.15);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        /* Header */
        header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .logo-icon {
            font-size: 2rem;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .logo-text {
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        
        .logo-tagline {
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .status-indicators {
            display: flex;
            gap: 1rem;
        }
        
        .status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-tertiary);
            border-radius: 2rem;
            font-size: 0.8rem;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        .status-dot.connected { background: var(--success); }
        .status-dot.disconnected { background: var(--error); }
        .status-dot.warning { background: var(--warning); }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Main Content */
        main {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 1000px;
            width: 100%;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* Chat Container */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
            border-radius: 1rem;
            border: 1px solid var(--border-color);
            overflow: hidden;
            box-shadow: var(--shadow-glow);
        }
        
        /* Messages */
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        
        .message {
            display: flex;
            gap: 1rem;
            animation: fadeIn 0.3s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            font-size: 1.2rem;
        }
        
        .message.user .message-avatar {
            background: var(--gradient-2);
        }
        
        .message.assistant .message-avatar {
            background: var(--gradient-1);
        }
        
        .message-content {
            flex: 1;
            background: var(--bg-tertiary);
            padding: 1rem 1.25rem;
            border-radius: 0.75rem;
            line-height: 1.6;
        }
        
        .message.user .message-content {
            background: var(--bg-hover);
        }
        
        .message-content p {
            margin-bottom: 0.5rem;
        }
        
        .message-content p:last-child {
            margin-bottom: 0;
        }
        
        .message-content code {
            font-family: 'JetBrains Mono', monospace;
            background: var(--bg-primary);
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.9em;
        }
        
        .message-content pre {
            background: var(--bg-primary);
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin: 0.5rem 0;
        }
        
        .message-content pre code {
            background: none;
            padding: 0;
        }
        
        /* Typing Indicator */
        .typing-indicator {
            display: flex;
            gap: 0.3rem;
            padding: 0.5rem;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-primary);
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
        
        /* Input Area */
        .input-area {
            padding: 1.5rem;
            background: var(--bg-tertiary);
            border-top: 1px solid var(--border-color);
        }
        
        .input-wrapper {
            display: flex;
            gap: 1rem;
            align-items: flex-end;
        }
        
        .input-field {
            flex: 1;
            position: relative;
        }
        
        textarea {
            width: 100%;
            padding: 1rem 1.25rem;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 1rem;
            resize: none;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
            min-height: 56px;
            max-height: 200px;
        }
        
        textarea:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1);
        }
        
        textarea::placeholder {
            color: var(--text-muted);
        }
        
        button.send-btn {
            padding: 1rem 1.5rem;
            background: var(--gradient-1);
            border: none;
            border-radius: 0.75rem;
            color: var(--bg-primary);
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        button.send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0, 212, 170, 0.4);
        }
        
        button.send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        /* Attachment Button */
        .attach-btn {
            padding: 1rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
            font-size: 1.1rem;
        }
        
        .attach-btn:hover {
            background: var(--bg-hover);
            border-color: var(--accent-primary);
            color: var(--text-primary);
        }
        
        /* Attachment Preview */
        .attachment-preview {
            padding: 0.75rem 1rem;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
        }
        
        .attachment-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.75rem;
            background: var(--bg-tertiary);
            border-radius: 0.5rem;
            font-size: 0.85rem;
        }
        
        .attachment-icon {
            font-size: 1rem;
        }
        
        .attachment-name {
            flex: 1;
            color: var(--text-primary);
            font-weight: 500;
        }
        
        .attachment-size {
            color: var(--text-muted);
        }
        
        .attachment-remove {
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 1.2rem;
            padding: 0;
            margin-left: 0.5rem;
        }
        
        .attachment-remove:hover {
            color: var(--error);
        }
        
        /* Attachment badge in message */
        .attachment-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.25rem 0.5rem;
            background: var(--bg-hover);
            border-radius: 0.25rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }
        
        /* Welcome Screen */
        .welcome {
            text-align: center;
            padding: 4rem 2rem;
        }
        
        .welcome-icon {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .welcome h2 {
            font-size: 1.75rem;
            margin-bottom: 0.5rem;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .welcome p {
            color: var(--text-secondary);
            margin-bottom: 2rem;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            justify-content: center;
        }
        
        .suggestion {
            padding: 0.75rem 1.25rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 2rem;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
        }
        
        .suggestion:hover {
            background: var(--bg-hover);
            border-color: var(--accent-primary);
            color: var(--text-primary);
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            header {
                padding: 1rem;
                flex-direction: column;
                gap: 1rem;
            }
            
            main {
                padding: 1rem;
            }
            
            .suggestions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">
            <span class="logo-icon">☿</span>
            <div>
                <div class="logo-text">Mercury</div>
                <div class="logo-tagline">Financial Market Intelligence</div>
            </div>
        </div>
        <div class="status-indicators">
            <div class="status-badge">
                <span class="status-dot" id="kite-status"></span>
                <span>Kite</span>
            </div>
            <div class="status-badge">
                <span class="status-dot" id="ai-status"></span>
                <span>AI</span>
            </div>
        </div>
    </header>
    
    <main>
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="welcome">
                    <div class="welcome-icon">☿</div>
                    <h2>Welcome to Mercury</h2>
                    <p>Your AI-powered financial market assistant. Ask me anything about stocks, markets, or your portfolio.</p>
                    <div class="suggestions">
                        <span class="suggestion" onclick="askSuggestion(this)">What's the current market sentiment?</span>
                        <span class="suggestion" onclick="askSuggestion(this)">Show me my positions</span>
                        <span class="suggestion" onclick="askSuggestion(this)">Analyze RELIANCE</span>
                        <span class="suggestion" onclick="askSuggestion(this)">Compare IT sector stocks</span>
                    </div>
                </div>
            </div>
            
            <div class="input-area">
                <!-- Attachment Preview -->
                <div class="attachment-preview" id="attachment-preview" style="display: none;">
                    <div class="attachment-item" id="attachment-item">
                        <span class="attachment-icon">📎</span>
                        <span class="attachment-name" id="attachment-name"></span>
                        <span class="attachment-size" id="attachment-size"></span>
                        <button class="attachment-remove" onclick="removeAttachment()">×</button>
                    </div>
                </div>
                
                <div class="input-wrapper">
                    <input type="file" id="file-input" style="display: none;" 
                           accept=".csv,.xlsx,.xls,.json,.txt,.md,.png,.jpg,.jpeg,.gif,.webp"
                           onchange="handleFileSelect(event)">
                    <button class="attach-btn" onclick="document.getElementById('file-input').click()" title="Attach file for analysis">
                        <span>📎</span>
                    </button>
                    <div class="input-field">
                        <textarea 
                            id="input" 
                            placeholder="Ask about stocks, markets, or attach files for analysis..."
                            rows="1"
                            onkeydown="handleKeyDown(event)"
                            oninput="autoResize(this)"
                        ></textarea>
                    </div>
                    <button class="send-btn" onclick="sendMessage()" id="send-btn">
                        <span>Send</span>
                        <span>→</span>
                    </button>
                </div>
            </div>
        </div>
    </main>
    
    <script>
        let conversationId = null;
        let isProcessing = false;
        let currentAttachment = null;
        
        // =====================================================================
        // FILE ATTACHMENT HANDLING
        // =====================================================================
        
        async function handleFileSelect(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            // Check file size (10 MB limit)
            if (file.size > 10 * 1024 * 1024) {
                showToast('File too large. Maximum size is 10 MB.', 'error');
                return;
            }
            
            // Show loading state
            const preview = document.getElementById('attachment-preview');
            const nameEl = document.getElementById('attachment-name');
            const sizeEl = document.getElementById('attachment-size');
            
            nameEl.textContent = file.name;
            sizeEl.textContent = formatFileSize(file.size);
            preview.style.display = 'block';
            
            // Upload file
            try {
                const formData = new FormData();
                formData.append('file', file);
                if (conversationId) {
                    formData.append('conversation_id', conversationId);
                }
                
                const response = await fetch('/api/attachments/upload', {
                    method: 'POST',
                    body: formData,
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Upload failed');
                }
                
                const result = await response.json();
                currentAttachment = result.attachment;
                
                showToast(`Attached: ${file.name}`, 'success');
                console.log('Attachment uploaded:', result);
                
            } catch (e) {
                console.error('Upload error:', e);
                showToast(`Upload failed: ${e.message}`, 'error');
                removeAttachment();
            }
            
            // Clear the file input
            event.target.value = '';
        }
        
        function removeAttachment() {
            currentAttachment = null;
            document.getElementById('attachment-preview').style.display = 'none';
            document.getElementById('file-input').value = '';
        }
        
        function formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        }
        
        // Check system status on load
        async function checkStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                const kiteStatus = document.getElementById('kite-status');
                const aiStatus = document.getElementById('ai-status');
                
                if (data.kite.authenticated) {
                    kiteStatus.className = 'status-dot connected';
                } else if (data.kite.status === 'mock_mode' || data.kite.status === 'configured') {
                    kiteStatus.className = 'status-dot warning';
                } else {
                    kiteStatus.className = 'status-dot disconnected';
                }
                
                if (data.anthropic.authenticated) {
                    aiStatus.className = 'status-dot connected';
                } else if (data.anthropic.status === 'mock_mode' || data.anthropic.status === 'configured') {
                    aiStatus.className = 'status-dot warning';
                } else {
                    aiStatus.className = 'status-dot disconnected';
                }
            } catch (e) {
                console.error('Status check failed:', e);
            }
        }
        
        // Auto-resize textarea
        function autoResize(el) {
            el.style.height = 'auto';
            el.style.height = Math.min(el.scrollHeight, 200) + 'px';
        }
        
        // Handle keyboard shortcuts
        function handleKeyDown(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }
        
        // Use suggestion
        function askSuggestion(el) {
            document.getElementById('input').value = el.textContent;
            sendMessage();
        }
        
        // Add message to chat
        function addMessage(role, content) {
            const messages = document.getElementById('messages');
            const welcome = messages.querySelector('.welcome');
            if (welcome) welcome.remove();
            
            const avatar = role === 'user' ? '👤' : '☿';
            
            const messageHtml = `
                <div class="message ${role}">
                    <div class="message-avatar">${avatar}</div>
                    <div class="message-content">${formatContent(content)}</div>
                </div>
            `;
            
            messages.insertAdjacentHTML('beforeend', messageHtml);
            messages.scrollTop = messages.scrollHeight;
        }
        
        // Add typing indicator
        function addTypingIndicator() {
            const messages = document.getElementById('messages');
            const typingHtml = `
                <div class="message assistant" id="typing">
                    <div class="message-avatar">☿</div>
                    <div class="message-content">
                        <div class="typing-indicator">
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                        </div>
                    </div>
                </div>
            `;
            messages.insertAdjacentHTML('beforeend', typingHtml);
            messages.scrollTop = messages.scrollHeight;
        }
        
        // Remove typing indicator
        function removeTypingIndicator() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
        }
        
        // Format content with markdown-like formatting
        function formatContent(text) {
            // Basic formatting
            text = text.replace(/\\n/g, '<br>');
            text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
            text = text.replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>');
            text = text.replace(/\\*([^*]+)\\*/g, '<em>$1</em>');
            
            // Wrap in paragraph
            if (!text.includes('<')) {
                text = '<p>' + text.replace(/\\n\\n/g, '</p><p>') + '</p>';
            }
            
            return text;
        }
        
        // Send message
        async function sendMessage() {
            if (isProcessing) return;
            
            const input = document.getElementById('input');
            const query = input.value.trim();
            
            if (!query) return;
            
            isProcessing = true;
            document.getElementById('send-btn').disabled = true;
            
            // Add user message
            addMessage('user', query);
            input.value = '';
            autoResize(input);
            
            // Show typing indicator
            addTypingIndicator();
            
            try {
                // Build request body
                const requestBody = {
                    query: query,
                    conversation_id: conversationId
                };
                
                // Include attachment if present
                if (currentAttachment) {
                    requestBody.attachment_ids = [currentAttachment.id];
                }
                
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestBody)
                });
                
                const data = await response.json();
                conversationId = data.conversation_id;
                
                // Clear attachment after sending
                if (currentAttachment) {
                    removeAttachment();
                }
                
                removeTypingIndicator();
                addMessage('assistant', data.response);
                
            } catch (e) {
                removeTypingIndicator();
                addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
                console.error('Chat error:', e);
            }
            
            isProcessing = false;
            document.getElementById('send-btn').disabled = false;
        }
        
        // =====================================================================
        // AUTONOMOUS ENHANCEMENTS: Auto-reconnect, Toasts, Degraded Mode
        // =====================================================================
        
        // Toast notification system
        function showToast(message, type = 'info', duration = 5000) {
            const container = document.getElementById('toast-container') || createToastContainer();
            
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = `
                <span class="toast-icon">${type === 'success' ? '✓' : type === 'error' ? '✕' : type === 'warning' ? '⚠' : 'ℹ'}</span>
                <span class="toast-message">${message}</span>
                <button class="toast-close" onclick="this.parentElement.remove()">×</button>
            `;
            
            container.appendChild(toast);
            
            // Auto-remove after duration
            setTimeout(() => {
                toast.classList.add('toast-fade-out');
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }
        
        function createToastContainer() {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText = `
                position: fixed;
                top: 1rem;
                right: 1rem;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            `;
            document.body.appendChild(container);
            
            // Add toast styles
            const style = document.createElement('style');
            style.textContent = `
                .toast {
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    padding: 1rem 1.25rem;
                    background: var(--bg-secondary);
                    border: 1px solid var(--border-color);
                    border-radius: 0.75rem;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                    animation: slideIn 0.3s ease-out;
                    min-width: 300px;
                }
                .toast-success { border-left: 4px solid var(--success); }
                .toast-error { border-left: 4px solid var(--error); }
                .toast-warning { border-left: 4px solid var(--warning); }
                .toast-info { border-left: 4px solid var(--accent-secondary); }
                .toast-icon { font-size: 1.2rem; }
                .toast-success .toast-icon { color: var(--success); }
                .toast-error .toast-icon { color: var(--error); }
                .toast-warning .toast-icon { color: var(--warning); }
                .toast-info .toast-icon { color: var(--accent-secondary); }
                .toast-message { flex: 1; font-size: 0.9rem; }
                .toast-close { 
                    background: none; 
                    border: none; 
                    color: var(--text-muted); 
                    cursor: pointer; 
                    font-size: 1.2rem;
                    padding: 0;
                }
                .toast-close:hover { color: var(--text-primary); }
                .toast-fade-out { opacity: 0; transform: translateX(100%); transition: all 0.3s; }
                @keyframes slideIn {
                    from { opacity: 0; transform: translateX(100%); }
                    to { opacity: 1; transform: translateX(0); }
                }
                
                /* Degraded mode banner */
                .degraded-banner {
                    background: linear-gradient(90deg, var(--warning), #f59e0b);
                    color: var(--bg-primary);
                    padding: 0.5rem 1rem;
                    text-align: center;
                    font-weight: 500;
                    display: none;
                }
                .degraded-banner.visible { display: block; }
                .degraded-banner a { color: inherit; text-decoration: underline; }
                
                /* Connection status overlay */
                .reconnect-overlay {
                    position: fixed;
                    inset: 0;
                    background: rgba(10,10,15,0.9);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    z-index: 9998;
                    opacity: 0;
                    pointer-events: none;
                    transition: opacity 0.3s;
                }
                .reconnect-overlay.visible {
                    opacity: 1;
                    pointer-events: auto;
                }
                .reconnect-spinner {
                    width: 50px;
                    height: 50px;
                    border: 3px solid var(--border-color);
                    border-top-color: var(--accent-primary);
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin-bottom: 1rem;
                }
                @keyframes spin { to { transform: rotate(360deg); } }
                .reconnect-text { color: var(--text-secondary); font-size: 1.1rem; }
                .reconnect-count { color: var(--text-muted); font-size: 0.9rem; margin-top: 0.5rem; }
            `;
            document.head.appendChild(style);
            
            return container;
        }
        
        // Connection state tracking
        let connectionState = {
            kite: 'unknown',
            ai: 'unknown',
            lastCheck: null,
            reconnectAttempts: 0,
            maxReconnectAttempts: 5,
            reconnectDelay: 5000,
        };
        
        // Enhanced status check with auto-reconnect
        async function checkStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                const kiteStatus = document.getElementById('kite-status');
                const aiStatus = document.getElementById('ai-status');
                const degradedBanner = document.getElementById('degraded-banner');
                const reconnectOverlay = document.getElementById('reconnect-overlay');
                
                // Update Kite status
                const prevKiteState = connectionState.kite;
                if (data.kite.authenticated) {
                    kiteStatus.className = 'status-dot connected';
                    connectionState.kite = 'connected';
                } else if (data.kite.status === 'mock_mode' || data.kite.status === 'configured') {
                    kiteStatus.className = 'status-dot warning';
                    connectionState.kite = 'degraded';
                } else {
                    kiteStatus.className = 'status-dot disconnected';
                    connectionState.kite = 'disconnected';
                }
                
                // Update AI status
                const prevAiState = connectionState.ai;
                if (data.anthropic.authenticated) {
                    aiStatus.className = 'status-dot connected';
                    connectionState.ai = 'connected';
                } else if (data.anthropic.status === 'mock_mode' || data.anthropic.status === 'configured') {
                    aiStatus.className = 'status-dot warning';
                    connectionState.ai = 'degraded';
                } else {
                    aiStatus.className = 'status-dot disconnected';
                    connectionState.ai = 'disconnected';
                }
                
                // Show/hide degraded banner
                const isDegraded = connectionState.kite === 'degraded' || connectionState.ai === 'degraded';
                const isDisconnected = connectionState.kite === 'disconnected' || connectionState.ai === 'disconnected';
                
                if (degradedBanner) {
                    if (isDegraded) {
                        degradedBanner.textContent = '⚠️ Running in degraded mode - some features may be limited';
                        degradedBanner.classList.add('visible');
                    } else if (isDisconnected && connectionState.kite === 'disconnected') {
                        degradedBanner.innerHTML = '⚠️ Kite API disconnected - <a href="/api/kite/login">Click to reconnect</a>';
                        degradedBanner.classList.add('visible');
                    } else {
                        degradedBanner.classList.remove('visible');
                    }
                }
                
                // Hide reconnect overlay on success
                if (reconnectOverlay) {
                    reconnectOverlay.classList.remove('visible');
                }
                
                // Show toast on state changes
                if (prevKiteState !== 'unknown' && prevKiteState !== connectionState.kite) {
                    if (connectionState.kite === 'connected') {
                        showToast('Kite API connected', 'success');
                    } else if (connectionState.kite === 'disconnected') {
                        showToast('Kite API disconnected', 'error');
                    }
                }
                
                if (prevAiState !== 'unknown' && prevAiState !== connectionState.ai) {
                    if (connectionState.ai === 'connected') {
                        showToast('AI connected', 'success');
                    } else if (connectionState.ai === 'disconnected') {
                        showToast('AI disconnected', 'error');
                    }
                }
                
                connectionState.lastCheck = new Date();
                connectionState.reconnectAttempts = 0;
                
            } catch (e) {
                console.error('Status check failed:', e);
                connectionState.reconnectAttempts++;
                
                // Show reconnect overlay after failures
                if (connectionState.reconnectAttempts >= 2) {
                    const overlay = document.getElementById('reconnect-overlay');
                    const countEl = document.getElementById('reconnect-count');
                    if (overlay) {
                        overlay.classList.add('visible');
                        if (countEl) {
                            countEl.textContent = `Attempt ${connectionState.reconnectAttempts} of ${connectionState.maxReconnectAttempts}`;
                        }
                    }
                }
                
                // Auto-reconnect logic
                if (connectionState.reconnectAttempts < connectionState.maxReconnectAttempts) {
                    setTimeout(checkStatus, connectionState.reconnectDelay);
                } else {
                    showToast('Connection lost. Please refresh the page.', 'error', 0);
                }
            }
        }
        
        // Initialize
        checkStatus();
        setInterval(checkStatus, 30000); // Check every 30 seconds
        
        // Add degraded banner and reconnect overlay to DOM
        document.body.insertAdjacentHTML('afterbegin', `
            <div class="degraded-banner" id="degraded-banner"></div>
            <div class="reconnect-overlay" id="reconnect-overlay">
                <div class="reconnect-spinner"></div>
                <div class="reconnect-text">Reconnecting to Mercury...</div>
                <div class="reconnect-count" id="reconnect-count"></div>
            </div>
        `);
    </script>
</body>
</html>'''


# Create application instance
app = create_app()
