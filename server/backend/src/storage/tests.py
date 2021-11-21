from typing import List, Optional
from uuid import UUID

from models.tests import Test
from models.workers import Worker
from schemas.tests import TestCreate, TestUpdate, TestView


async def get() -> List[TestView]:
    tests = await Test.all()
    test_views: List[TestView] = []
    for test in tests:
        test_views.append(TestView.from_orm(test))
    return test_views


async def get_latest(worker_id: UUID) -> Optional[TestView]:
    test = await Test.filter(worker__id=worker_id).first()
    if test is None:
        return None
    return TestView.from_orm(test)


async def create(test_create: TestCreate) -> TestView:
    worker = await Worker.get(id=test_create.worker_id)
    worker.test = Test(**test_create.dict(exclude={"worker_id"}))
    await worker.test.save()
    await worker.save()
    return TestView.from_orm(worker.test)


async def update(test: TestUpdate) -> TestView:
    test_db = await Test.get(id=test.id)
    test_db.update_from_dict(test.dict(exclude_unset=True, exclude={"id"}))
    await test_db.save()
    return TestView.from_orm(test_db)


async def delete(test_id: UUID) -> None:
    test_db = await Test.get(id=test_id)
    await test_db.delete()
