"""
Pydantic models for WhatsApp AI Second Brain Assistant
Defines data structures for API requests, responses, and database documents
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class MessageType(str, Enum):
    """Types of messages"""
    TEXT = "text"
    DOCUMENT = "document"
    IMAGE = "image"
    LINK = "link"
    REMINDER = "reminder"
    QUESTION = "question"

class ContentType(str, Enum):
    """Types of stored content"""
    NOTE = "note"
    DOCUMENT = "document"
    TASK = "task"
    REMINDER = "reminder"
    SUMMARY = "summary"

class ReminderStatus(str, Enum):
    """Reminder status"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class WhatsAppMessage(BaseModel):
    """Incoming WhatsApp message structure"""
    from_number: str = Field(..., description="Sender's phone number")
    to_number: str = Field(..., description="Recipient's phone number")
    body: str = Field(..., description="Message content")
    message_type: MessageType = Field(default=MessageType.TEXT, description="Type of message")
    media_url: Optional[str] = Field(None, description="URL for media content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ProcessedContent(BaseModel):
    """Processed content for storage"""
    user_id: str = Field(..., description="User identifier")
    content_type: ContentType = Field(..., description="Type of content")
    title: str = Field(..., description="Content title")
    content: str = Field(..., description="Main content text")
    summary: Optional[str] = Field(None, description="AI-generated summary")
    tags: List[str] = Field(default_factory=list, description="Content tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskItem(BaseModel):
    """Extracted task item"""
    task_id: str = Field(..., description="Unique task identifier")
    user_id: str = Field(..., description="User identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    priority: str = Field(default="medium", description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Due date")
    completed: bool = Field(default=False, description="Completion status")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReminderItem(BaseModel):
    """Reminder item"""
    reminder_id: str = Field(..., description="Unique reminder identifier")
    user_id: str = Field(..., description="User identifier")
    title: str = Field(..., description="Reminder title")
    message: str = Field(..., description="Reminder message")
    scheduled_time: datetime = Field(..., description="When to send reminder")
    status: ReminderStatus = Field(default=ReminderStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SummaryRequest(BaseModel):
    """Request for document summarization"""
    content: str = Field(..., description="Content to summarize")
    summary_type: str = Field(default="concise", description="Type of summary")
    max_length: int = Field(default=200, description="Maximum summary length")

class SummaryResponse(BaseModel):
    """Response for document summarization"""
    summary: str = Field(..., description="Generated summary")
    key_points: List[str] = Field(default_factory=list, description="Key points")
    word_count: int = Field(..., description="Summary word count")

class QuestionRequest(BaseModel):
    """Request for Q&A"""
    question: str = Field(..., description="User question")
    user_id: str = Field(..., description="User identifier")
    context_limit: int = Field(default=5, description="Number of context documents")

class QuestionResponse(BaseModel):
    """Response for Q&A"""
    answer: str = Field(..., description="Generated answer")
    sources: List[str] = Field(default_factory=list, description="Source documents")
    confidence: float = Field(default=0.0, description="Answer confidence score")

class VectorDocument(BaseModel):
    """Document for vector storage"""
    doc_id: str = Field(..., description="Document identifier")
    user_id: str = Field(..., description="User identifier")
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    embedding: Optional[List[float]] = Field(None, description="Document embedding")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatResponse(BaseModel):
    """WhatsApp bot response"""
    message: str = Field(..., description="Response message")
    message_type: str = Field(default="text", description="Response type")
    actions: List[str] = Field(default_factory=list, description="Actions taken")

# Example usage for documentation.
EXAMPLE_WHATSAPP_MESSAGE = {
    "from_number": "whatsapp:+1234567890",
    "to_number": "whatsapp:+14155238886",
    "body": "Please summarize this document and remind me to review it tomorrow at 2pm",
    "message_type": "text",
    "timestamp": "2025-06-29T10:00:00Z"
}

EXAMPLE_PROCESSED_CONTENT = {
    "user_id": "user_123",
    "content_type": "document",
    "title": "Meeting Notes - Q2 Planning",
    "content": "Discussion about quarterly goals and objectives...",
    "summary": "Key points from Q2 planning meeting covering goals, timelines, and resource allocation.",
    "tags": ["meeting", "planning", "Q2"],
    "metadata": {"source": "whatsapp", "file_type": "pdf"}
}

EXAMPLE_TASK_EXTRACTION = {
    "tasks": [
        {
            "task_id": "task_001",
            "user_id": "user_123",
            "title": "Review quarterly report",
            "description": "Review and provide feedback on Q2 report",
            "priority": "high",
            "due_date": "2025-07-01T14:00:00Z"
        }
    ],
    "reminders": [
        {
            "reminder_id": "rem_001",
            "user_id": "user_123",
            "title": "Document Review Reminder",
            "message": "Don't forget to review the quarterly report",
            "scheduled_time": "2025-06-30T14:00:00Z"
        }
    ]
}
