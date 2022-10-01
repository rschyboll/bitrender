# pylint: disable=not-context-manager
"""Contains tests for the bitrender.services.inject module."""

from antidote import world

from bitrender.services.inject import InjectInService


class TestDIClass:
    """Class used as a test dependency for antidote"""


class TestInjectInService:
    """Test case for testing the InjectInService class."""

    def test_inject_dependency(self) -> None:
        """Tests proper injecting"""
        context = object()
        context_key = "context"
        dependency = TestDIClass()
        inject = InjectInService(context, context_key)

        with world.test.clone() as overrides:

            overrides.update({TestDIClass: dependency})
            dependency_injected = inject(TestDIClass)
            assert dependency_injected == dependency
            assert getattr(dependency_injected, context_key) == context
