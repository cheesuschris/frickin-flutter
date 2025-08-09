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
  bool _isLoading = false; // Not final: toggled when navigating to settings
  User? get _currentUser => Supabase.instance.client.auth.currentUser;

  // _signOut removed (unused)

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
