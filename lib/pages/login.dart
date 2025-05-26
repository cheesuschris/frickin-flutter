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
  bool _loading = false;

  void login() async {
    if (_loading) return;

    setState(() => _loading = true);

    try {
      final email = _email.text.trim();
      final password = _password.text;
      debugPrint('Attempting login with email: $email');

      await auth.signIn(email, password);

      if (!mounted) return;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const ProfilePage()),
      );
    } catch (e) {
      debugPrint('Login error: $e');
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    } finally {
      if (mounted) {
        setState(() => _loading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            controller: _email,
            decoration: const InputDecoration(labelText: 'Email'),
            keyboardType: TextInputType.emailAddress,
            enabled: !_loading,
          ),
          TextField(
            controller: _password,
            decoration: const InputDecoration(labelText: 'Password'),
            obscureText: true,
            enabled: !_loading,
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: _loading ? null : login,
            child: _loading
                ? const CircularProgressIndicator()
                : const Text("Login"),
          ),
          const SizedBox(height: 12),
          if (!_loading)
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