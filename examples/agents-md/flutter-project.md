# AGENTS.md — Flutter Project

## Stack
- Flutter 3.x / Dart 3.x
- Riverpod for state management
- GoRouter for navigation
- Dio for HTTP
- Freezed for immutable models

## Code Style
- Follow Effective Dart guidelines
- Use `const` constructors wherever possible
- Prefer `final` over `var`
- File naming: snake_case
- One widget per file

## Project Structure
```
lib/
├── main.dart
├── app/              # App config, router, theme
├── features/         # Feature modules
│   └── auth/
│       ├── data/     # Repositories, data sources
│       ├── domain/   # Models, interfaces
│       └── ui/       # Screens, widgets
├── shared/           # Shared widgets, utils
└── generated/        # Auto-generated (freezed, l10n)
```

## Commands
- Run: `flutter run`
- Test: `flutter test`
- Build APK: `flutter build apk`
- Build iOS: `flutter build ios`
- Generate code: `dart run build_runner build`
- Analyze: `flutter analyze`

## Rules
- Responsive design: ใช้ LayoutBuilder, never hardcode pixel sizes
- ตอบเป็นภาษาไทยเสมอ
- Extract widgets when build() exceeds 80 lines
- Always dispose controllers in StatefulWidgets
- Use `.env` for API endpoints, never hardcode URLs
- Support both light and dark theme
