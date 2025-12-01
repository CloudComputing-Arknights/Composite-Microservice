from dataclasses import dataclass

@dataclass
class MessagingThreadDto:
    thread_id: str
    author_id: str
    participant_id: str
    created_at: str
    updated_at: str