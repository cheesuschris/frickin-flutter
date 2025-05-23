import 'package:cooking_app/auth/auth.dart';
import 'package:flutter/material.dart';

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
          TextField(controller: _email),
          TextField(
            controller: _password,
            decoration: const InputDecoration(labelText: 'Password'),
            obscureText: true,
          ),

          ElevatedButton(onPressed: login, child: const Text("Login")),
        ],
      ),
    );
  }
}
