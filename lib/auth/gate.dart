import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:cooking_app/pages/login.dart';
import 'package:cooking_app/pages/prof.dart';

class AuthGate extends StatefulWidget {
  const AuthGate({super.key});

  @override
  State<AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends State<AuthGate> {
  bool _initialAuthCheckDone = false;

  @override
  void initState() {
    super.initState();
    _checkInitialAuthState();
  }

  Future<void> _checkInitialAuthState() async {
    // Force an immediate auth check
    final session = Supabase.instance.client.auth.currentSession;
    debugPrint('Initial Session Check: ${session != null}');
    if (mounted) {
      setState(() => _initialAuthCheckDone = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    // If we haven't done initial check, show spinner
    if (!_initialAuthCheckDone) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return StreamBuilder<AuthState>(
      stream: Supabase.instance.client.auth.onAuthStateChange,
      builder: (context, snapshot) {
        debugPrint('Auth State: ${snapshot.data?.event}');
        debugPrint('Connection State: ${snapshot.connectionState}');
        
        // Get current session directly
        final currentSession = Supabase.instance.client.auth.currentSession;
        
        if (currentSession != null) {
          return const ProfilePage();
        }

        return const LoginPage();
      },
    );
  }
}
