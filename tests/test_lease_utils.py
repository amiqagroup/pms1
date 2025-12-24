from uae_property_management.property_management.utils.lease_utils import (
    get_payment_schedule,
)
import sys
import types
from datetime import date

# Provide a minimal fake `frappe.utils` so lease_utils can import getdate/add_months
fake_frappe = types.ModuleType("frappe")
fake_utils = types.ModuleType("frappe.utils")


def getdate(val):
    if isinstance(val, str):
        return date.fromisoformat(val)
    return val


def add_months(d, months):
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    days_in_month = [
        31,
        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    day = min(d.day, days_in_month[month - 1])
    return date(year, month, day)


fake_utils.getdate = getdate
fake_utils.add_months = add_months
sys.modules['frappe'] = fake_frappe
sys.modules['frappe.utils'] = fake_utils


class DummyLease:
    def __init__(self, lease_start, annual_rent, payment_frequency=None):
        self.lease_start = lease_start
        self.annual_rent = annual_rent
        self.payment_frequency = payment_frequency


def test_annual_schedule():
    lease = DummyLease('2025-01-01', 120000, 'Annual')
    sched = get_payment_schedule(lease)
    assert len(sched) == 1
    assert sched[0]['amount'] == 120000
    assert sched[0]['due_date'] == date(2025, 1, 1)


def test_monthly_schedule_total_and_count():
    lease = DummyLease('2025-01-15', 120000, 'Monthly')
    sched = get_payment_schedule(lease)
    assert len(sched) == 12
    total = sum(p['amount'] for p in sched)
    assert abs(total - 120000) < 0.001
