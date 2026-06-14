"""Chat history manager untuk menyimpan dan memuat percakapan."""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

CHAT_HISTORY_DIR = Path(__file__).parent.parent / "data" / "chat_history"
CHAT_HISTORY_DIR.mkdir(exist_ok=True)

CONVERSATIONS_FILE = CHAT_HISTORY_DIR / "conversations.json"


def _load_conversations() -> list:
    """Load semua conversations dari file."""
    if CONVERSATIONS_FILE.exists():
        try:
            with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_conversations(conversations: list) -> None:
    """Save conversations ke file."""
    CHAT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=2, ensure_ascii=False)


def get_all_conversations() -> list:
    """
    Get semua conversations dengan format:
    [
        {
            "id": "conv_123",
            "title": "Produk apa yang paling laris?...",
            "created_at": "2024-01-15 10:30:45",
            "updated_at": "2024-01-15 10:35:20",
            "messages": [...]
        },
        ...
    ]
    """
    return _load_conversations()


def create_conversation(first_message: str) -> dict:
    """Buat conversation baru."""
    conversations = _load_conversations()

    title = first_message[:40] + "..." if len(first_message) > 40 else first_message

    conv = {
        "id": f"conv_{int(datetime.now().timestamp() * 1000)}",
        "title": title,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": []
    }

    conversations.insert(0, conv)
    _save_conversations(conversations)

    return conv


def save_message(conv_id: str, role: str, content: str) -> None:
    """Save message ke conversation yang spesifik."""
    conversations = _load_conversations()

    for conv in conversations:
        if conv["id"] == conv_id:
            conv["messages"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            conv["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break

    _save_conversations(conversations)


def get_conversation(conv_id: str) -> Optional[dict]:
    """Get conversation by ID."""
    conversations = _load_conversations()
    for conv in conversations:
        if conv["id"] == conv_id:
            return conv
    return None


def delete_conversation(conv_id: str) -> None:
    """Delete conversation by ID."""
    conversations = _load_conversations()
    conversations = [c for c in conversations if c["id"] != conv_id]
    _save_conversations(conversations)


def clear_all_conversations() -> None:
    """Clear semua conversations."""
    _save_conversations([])


def get_conversation_context(conv_id: str, max_turns: int = 5) -> str:
    """
    Get formatted conversation context untuk dipass ke LLM.
    Max 5 turns sebelumnya untuk menghindari token limit.
    
    Format:
    User: [message 1]
    Assistant: [response 1]
    User: [message 2]
    ...
    """
    conv = get_conversation(conv_id)
    if not conv or not conv["messages"]:
        return ""

    messages = conv["messages"][-(max_turns * 2):]  # Ambil max 5 turns (10 messages)

    context_lines = []
    for msg in messages:
        role_display = "User" if msg["role"] == "user" else "Assistant"
        context_lines.append(f"{role_display}: {msg['content']}")

    return "\n".join(context_lines)
