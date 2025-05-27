import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:cooking_app/pages/login.dart';
import 'package:cooking_app/pages/prof.dart';

class AuthGate extends StatelessWidget {
  const AuthGate({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: StreamBuilder<AuthState>(
        stream: Supabase.instance.client.auth.onAuthStateChange,
        builder: (context, snapshot) {
          debugPrint('Auth State: ${snapshot.data?.event}');
          debugPrint('Connection State: ${snapshot.connectionState}');
          
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          
          final currentSession = Supabase.instance.client.auth.currentSession;
          
          if (currentSession != null) {
            return const ProfilePage();
          }
          
          return const LoginPage();
        },
      ),
    );
  }
}
