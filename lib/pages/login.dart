import 'package:cooking_app/auth/auth.dart';
import 'package:flutter/material.dart';
import 'package:cooking_app/pages/reg.dart';
import 'package:cooking_app/pages/prof.dart'; 

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});
  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final auth = Auth();
  final _email = TextEditingController();
  final _password = TextEditingController();
  void login() async {
    final email = _email.text.trim();
    final password = _password.text;
    try {
      await auth.signIn(email, password);
      if (mounted) {
        Navigator.pushReplacement(
          context,
        MaterialPageRoute(builder: (context) => const ProfilePage()),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("Error $e")));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView(
        children: [
          TextField(
            controller: _email,
            decoration: const InputDecoration(labelText: 'Username'),
          ),
          TextField(
            controller: _password,
            decoration: const InputDecoration(labelText: 'Password'),
            obscureText: true,
          ),
          ElevatedButton(onPressed: login, child: const Text("Login")),
          const SizedBox(height: 12),
          GestureDetector(
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const Reg()),
            ),
            child: const Center(child: Text("Sign Up")),
          ),
        ],
      ),
    );
  }
}