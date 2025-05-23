import 'package:supabase_flutter/supabase_flutter.dart';

class Auth {
  final SupabaseClient _supabase = Supabase.instance.client;
  Future<AuthResponse> signIn(String email, String password) async {
    return await _supabase.auth.signInWithPassword(
      email: email,
      password: password,
    );
  }

  Future<AuthResponse> signUp(String email, String password) async {
    return await _supabase.auth.signUp(email: email, password: password);
  }

  Future<void> signOut() async {
    return await _supabase.auth.signOut();
  }

  String? getEmail() {
    final session = _supabase.auth.currentSession;
    final curr = session?.user;
    return curr?.email;
  }
}
