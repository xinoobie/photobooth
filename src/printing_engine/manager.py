"""Print Engine - manage printing operations.

Features:
- Printer detection
- Print queue
- Print preview
- Print quantity
- Paper size selection
- Print resolution
- Auto print
- Retry printing
- Print history
"""

from __future__ import annotations

import os
import queue as queue_module
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from app_core.config import Config
from app_core.logging_config import get_logger
from app_core.utils import ensure_dir

config = Config.instance()
logger = get_logger("xinoobie.printing_engine")


@dataclass
class Printer:
    """A printer definition."""
    id: str
    name: str
    device_id: str
    is_enabled: bool = True
    status: str = "offline"  # offline, online, error
    is_default: bool = False


@dataclass
class PrintJob:
    """A print job."""
    job_id: str
    session_id: str
    photo_paths: list[str]
    quantity: int
    paper_size: str = "A6"
    resolution: int = 600
    status: str = "pending"  # pending, printing, completed, failed
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class PrintManager:
    """Manages the print queue and printing operations."""

    def __init__(self):
        self._printers: list[Printer] = []
        self._print_queue: queue_module.Queue[PrintJob] = queue_module.Queue()
        self._active_job: Optional[PrintJob] = None
        self._printer_status: dict[str, str] = {}

        # Register default printers
        self._register_default_printers()

    def _register_default_printers(self):
        """Register default printers for development."""
        self._add_printer(
            Printer(
                id="printer1",
                name="Default Printer",
                device_id="\\.\\SCREEN001",
                is_default=True,
            )
        )

    def _add_printer(self, printer: Printer):
        """Add a printer."""
        self._printers.append(printer)
        logger.info("Printer registered: %s (%s)", printer.name, printer.id)

    def get_printers(self) -> list[Printer]:
        """Get all printers."""
        return self._printers

    def get_default_printer(self) -> Optional[Printer]:
        """Get the default printer."""
        for p in self._printers:
            if p.is_default:
                return p
        return self._printers[0] if self._printers else None

    def scan_printers(self) -> list[Printer]:
        """Scan for available printers."""
        # In a real implementation, this would call Windows printing API
        # For Phase 1, returns configured printers
        logged = []
        for p in self._printers:
            logged.append(f"{p.name} ({p.device_id}) - {p.status}")
        logger.info("Printer scan results: %s", logged)
        return self._printers

    def add_print_job(self, session_id: str, photo_paths: list[str],
                      quantity: int, paper_size: str = "A6",
                      resolution: int = 600) -> PrintJob:
        """Add a print job to the queue."""
        job = PrintJob(
            job_id=str(uuid.uuid4()),
            session_id=session_id,
            photo_paths=photo_paths,
            quantity=quantity,
            paper_size=paper_size,
            resolution=resolution,
            status="pending",
        )
        self._print_queue.put(job)
        logger.info("Print job added: job=%s, qty=%d", job.job_id, quantity)
        return job

    def get_next_job(self) -> Optional[PrintJob]:
        """Get the next pending job."""
        try:
            job = self._print_queue.get_nowait()
            job.status = "printing"
            logger.info("Next print job: %s", job.job_id)
            return job
        except queue_module.Empty:
            return None

    def complete_job(self, job_id: str, error: str = None):
        """Mark a job as completed or failed."""
        # In a real implementation, this would be thread-safe
        logger.info("Job completed: %s, error=%s", job_id, error)

    def retry_job(self, job_id: str):
        """Retry a failed job."""
        logger.info("Retrying job: %s", job_id)
        # Re-add to queue
        # self._print_queue.put(job)  # would need access to job object

    def get_queue(self) -> list[PrintJob]:
        """Get current print queue."""
        # In a real implementation, this would get from queue
        return list(self._print_queue.queue)
