import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:cooking_app/widgets/main_scaffold_with_bottom_navbar.dart';
import 'package:cooking_app/pages/settings/setmain.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});
  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  bool _isLoading = false;
  User? get _currentUser => Supabase.instance.client.auth.currentUser;

  Future<void> _signOut() async {
    setState(() => _isLoading = true);
    try {
      await Supabase.instance.client.auth.signOut();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Error signing out: $e')));
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Widget _buildLogoutButton() {
    return IconButton(
      icon: _isLoading
          ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                color: Colors.white,
              ),
            )
          : const Icon(Icons.settings),
      onPressed: () {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => Setmain()),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return MainScaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome ${_currentUser?.email ?? "User"}!',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
      currentIndex: 4,
      actions: [_buildLogoutButton()],
    );
  }
}
