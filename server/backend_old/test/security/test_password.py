from src.security.password import hash, check, strength_check, PasswordStrengthError
from unittest import TestCase


class PasswordTest(TestCase):
    def test_hash_check(self):
        password = 'Test'
        passwordHash = hash(password)
        assert check(password, passwordHash)
        password = 'Test'
        passwordHash = hash('Test2')
        assert not check(password, passwordHash)

    def test_strength_check(self):
        password = "12Test!"
        self.assertRaises(PasswordStrengthError, strength_check, password)
        password = "123Test123"
        self.assertRaises(PasswordStrengthError, strength_check, password)
        password = "!TestTest"
        self.assertRaises(PasswordStrengthError, strength_check, password)
        password = "test123!"
        self.assertRaises(PasswordStrengthError, strength_check, password)
        password = "Test123!"
        try:
            strength_check(password)
        except PasswordStrengthError:
            self.fail("strength_check() raised PasswordStrengthError with acceptable password.")