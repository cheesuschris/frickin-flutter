import 'package:cooking_app/auth/auth.dart';
import 'package:cooking_app/pages/login.dart';
import 'package:flutter/material.dart';

class Reg extends StatefulWidget {
  const Reg({super.key});
  @override
  State<Reg> createState() => _regPageState();
}

class _regPageState extends State<Reg> {
  final auth = Auth();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _confirm = TextEditingController();
  void signUp() async {
    final email = _email.text.trim();
    final password = _password.text;
    final confirm = _confirm.text;
    if (confirm != password) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("Passwords do not match")));
      return;
    }
    try {
      await auth.signUp(email, password);
      Navigator.pop(context);
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
            decoration: const InputDecoration(labelText: "Password"),
          ),
          ElevatedButton(onPressed: signUp, child: const Text("Register")),
          const SizedBox(height: 12),
          GestureDetector(
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const LoginPage()),
            ),
            child: const Center(child: Text("Go Back")),
          ),
        ],
      ),
    );
  }
}
