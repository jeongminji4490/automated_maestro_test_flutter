import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:maestro_test/dashboard_page.dart';
import 'package:maestro_test/login_page.dart';

final _router = GoRouter(
  initialLocation: '/login',
  redirect: (_, state) {
    final uri = state.uri;
    final deeplinkPath = uri.path.isNotEmpty && uri.path != '/'
        ? uri.path
        : (uri.host.isNotEmpty ? '/${uri.host}' : uri.path);

    if (deeplinkPath == '/dashboard' && state.matchedLocation != '/dashboard') {
      return '/dashboard';
    }
    if (deeplinkPath == '/login' && state.matchedLocation != '/login') {
      return '/login';
    }
    return null;
  },
  routes: [
    GoRoute(path: '/login', builder: (_, _) => const LoginPage()),
    GoRoute(path: '/dashboard', builder: (_, _) => const DashboardPage()),
  ],
);

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(routerConfig: _router);
  }
}
