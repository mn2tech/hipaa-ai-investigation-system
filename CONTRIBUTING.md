# Contributing Guidelines

## Development Setup

1. Follow the installation instructions in README.md
2. Install development dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest
```

4. Run linters:
```bash
black src tests
flake8 src tests
mypy src
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Write docstrings for all classes and functions
- Keep functions focused and single-purpose

## Security Considerations

- Never commit sensitive data (API keys, passwords, etc.)
- All PHI handling must be encrypted
- Follow HIPAA compliance requirements
- Document security-related changes

## Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Test compliance and security features thoroughly

## Documentation

- Update README.md for user-facing changes
- Update API.md for API changes
- Update COMPLIANCE.md for compliance-related changes
- Add docstrings to all new code

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Update documentation
5. Run linters and tests
6. Submit pull request with clear description

