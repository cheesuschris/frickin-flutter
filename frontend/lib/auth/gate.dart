import 'package:flutter/material.dart';
import 'package:cooking_app/pages/login.dart';
import 'package:cooking_app/pages/home.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:supabase_flutter/supabase_flutter.dart';
class AuthGate extends StatelessWidget {

  @override
  void initState() {

  }

  Future<void> sendDataToBackend(Map<String, dynamic> data) async {
    final accessToken = Supabase.instance.client.auth.currentSession?.accessToken;
    if (accessToken == null) return;

    final response = await http.post(
      Uri.parse('http://localhost:5000/initialize_profile'),
      headers: {
        'Authorization': 'Bearer $accessToken',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(data),
    );
    if (response.statusCode == 200) {
      print("Profile sent successfully");
    } else {
      print("Failed: ${response.statusCode}");
    }
  }

  const AuthGate({super.key});

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<AuthState>(
      stream: Supabase.instance.client.auth.onAuthStateChange,
      builder: (context, snapshot) {
        debugPrint('Auth State Event: ${snapshot.data?.event}');
        debugPrint('Auth State Session: ${snapshot.data?.session != null}');
        debugPrint('Connection State: ${snapshot.connectionState}');

        if (snapshot.hasError) {
          return Scaffold(
            body: Center(child: Text('Error: ${snapshot.error}')),
          );
        }

        final authState = snapshot.data;
        if (authState?.session != null) {
          sendDataToBackend({});
          return const HomePage();
        }
        return const LoginPage();
      },
    );
  }
}
