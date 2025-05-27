import 'package:supabase_flutter/supabase_flutter.dart';

class Auth {
  final SupabaseClient _supabase = Supabase.instance.client;
  Future<AuthResponse> signIn(String email, String password) async {
    return await _supabase.auth.signInWithPassword(
      email: email,
      password: password,
    );
  }

  Future<bool> isEmailVerified() async {
    final user = _supabase.auth.currentUser;
    return user?.emailConfirmedAt != null;
  }

  Future<AuthResponse> signUp(String email, String password) async {
    return await _supabase.auth.signUp(email: email, password: password);
  }

  Future<void> signOut() async {
    return await _supabase.auth.signOut();
  }

  Future<void> resetPassword(String email) async {
    await _supabase.auth.resetPasswordForEmail(
      email,
      redirectTo:
          'http://localhost:3000/reset-password', // You'll want to change this URL for production
    );
  }

  String? getEmail() {
    final session = _supabase.auth.currentSession;
    final curr = session?.user;
    return curr?.email;
  }
}
