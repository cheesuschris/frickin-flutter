import 'package:flutter/material.dart';
import 'package:cooking_app/widgets/main_scaffold_with_bottom_navbar.dart';

class LandingPage extends StatefulWidget {
  const LandingPage({super.key});

  @override
  State<LandingPage> createState() => _LandingPageState();
}

class _LandingPageState extends State<LandingPage> {

  @override
  void initState() {
    super.initState();
    sendDataToBackend({});
  }

  Future<void> sendDataToBackend(Map<String, dynamic> data) async {
    final accessToken = Supabase.instance.client.auth.currentSession?.accessToken;
    if (accessToken == null) return;

    final response = await http.post(
      Uri.parse('http://localhost:5000/home'),
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

  //In the widget, when opening the home page, use sendDataToBackend(map) to send changes to backend
  @override
  Widget build(BuildContext context) {
    return MainScaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Welcome to the Home Page'),
            const SizedBox(height: 20),
          ],
        ),
      ),
      currentIndex: 0,
    );
  }
}
