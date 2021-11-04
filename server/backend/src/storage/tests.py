from typing import List, Optional
from uuid import UUID


from models.tests import Test
from schemas.tests import TestView


async def get() -> List[TestView]:
    tests = await Test.all()
    test_views: List[TestView] = []
    for test in tests:
        test_views.append(TestView.from_orm(test))
    return test_views


async def get_latest(worker_id: UUID) -> Optional[TestView]:
    test = await Test.filter(worker__id=worker_id).order_by("date").first()
    if test is None:
        return None
    return TestView.from_orm(test)
