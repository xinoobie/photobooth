"""Payment Engine - modular payment processing.

Features:
- Package pricing
- Voucher support
- Discount
- Transaction history
- Payment verification
- Payment status tracking
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from app_core.config import Config
from app_core.logging_config import get_logger

config = Config.instance()
logger = get_logger("xinoobie.payment_engine")


@dataclass
class PaymentMethod:
    """A payment method definition."""
    id: str
    name: str
    type: str  # cash, qris_manual, ewallet, gateway
    is_enabled: bool = True


@dataclass
class Transaction:
    """A payment transaction."""
    id: str
    session_id: str
    package_name: str
    amount: float
    payment_method: str
    status: str = "pending"  # pending, paid, failed, refunded
    voucher_code: Optional[str] = None
    discount_amount: float = 0.0
    transaction_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    paid_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None


class PaymentManager:
    """Manages payments and transactions."""

    def __init__(self):
        self._payment_methods: list[PaymentMethod] = []
        self._transactions: list[Transaction] = []
        self._initialize_default_methods()

    def _initialize_default_methods(self):
        """Add default payment methods."""
        methods = [
            PaymentMethod(id="cash", name="Tuition/Cash", type="cash", is_enabled=True),
            PaymentMethod(id="qris_manual", name="QRIS Manual", type="qris_manual", is_enabled=True),
            PaymentMethod(id="ewallet", name="E-wallet", type="ewallet", is_enabled=True),
            PaymentMethod(id="gateway", name="Payment Gateway", type="gateway", is_enabled=False),
        ]
        self._payment_methods.extend(methods)

    def get_payment_methods(self) -> list[PaymentMethod]:
        """Get all enabled payment methods."""
        return [m for m in self._payment_methods if m.is_enabled]

    def get_method(self, method_id: str) -> Optional[PaymentMethod]:
        """Get a payment method by ID."""
        return next((m for m in self._payment_methods if m.id == method_id), None)

    def create_transaction(self, session_id: str, package_name: str,
                           amount: float, payment_method: str,
                           voucher_code: Optional[str] = None,
                           discount_amount: float = 0.0) -> Transaction:
        """Create a new transaction."""
        transaction = Transaction(
            id=str(uuid.uuid4()),
            session_id=session_id,
            package_name=package_name,
            amount=amount,
            payment_method=payment_method,
            voucher_code=voucher_code,
            discount_amount=discount_amount,
            status="pending",
        )
        self._transactions.append(transaction)
        logger.info("Transaction created: %s (session=%s)",
                    transaction.id, session_id)
        return transaction

    def verify_payment(self, transaction_id: str, amount_received: float) -> bool:
        """Verify payment receipt."""
        transaction = self._get_transaction(transaction_id)
        if not transaction:
            return False

        if transaction.status == "paid":
            return True

        if amount_received >= transaction.amount:
            transaction.status = "paid"
            transaction.paid_at = datetime.now(timezone.utc)
            logger.info("Payment verified: %s", transaction_id)
            return True
        return False

    def refund_transaction(self, transaction_id: str) -> bool:
        """Refund a transaction."""
        transaction = self._get_transaction(transaction_id)
        if not transaction:
            return False
        if transaction.status == "paid":
            transaction.status = "refunded"
            transaction.refunded_at = datetime.now(timezone.utc)
            logger.info("Transaction refunded: %s", transaction_id)
            return True
        return False

    def _get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get a transaction by ID."""
        return next((t for t in self._transactions if t.id == transaction_id), None)

    def get_transactions_by_session(self, session_id: str) -> list[Transaction]:
        """Get all transactions for a session."""
        return [t for t in self._transactions
                if t.session_id == session_id]

    def get_transactions_by_status(self, status: str) -> list[Transaction]:
        """Get transactions by status."""
        return [t for t in self._transactions if t.status == status]
