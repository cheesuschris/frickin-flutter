import 'package:flutter/material.dart';
import 'package:cooking_app/widgets/main_scaffold_with_bottom_navbar.dart';

class SearchPage extends StatefulWidget {
  const SearchPage({super.key});
  @override
  State<SearchPage> createState() => _SearchBarC();
}

class _SearchBarC extends State<SearchPage> {

  @override
  void initState() {
    super.initState();
    sendDataToBackend({});
  }

  Future<void> sendDataToBackend(Map<String, dynamic> data) async {
    final accessToken = Supabase.instance.client.auth.currentSession?.accessToken;
    if (accessToken == null) return;

    final response = await http.post(
      Uri.parse('http://localhost:5000/search'),
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

  //In the widget, when opening the search page, use sendDataToBackend(map) to send changes to backend
  //Implement fuzzy matching search logic (for now, return all. later, return top k results.)
  @override
  Widget build(BuildContext context) {
    return MainScaffold(
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: SearchAnchor(
          builder: (BuildContext context, SearchController controller) {
            return SearchBar(
              controller: controller,
              padding: const WidgetStatePropertyAll<EdgeInsets>(
                EdgeInsets.symmetric(horizontal: 12),
              ),
              onTap: () {
                controller.openView();
              },
              onChanged: (_) {
                controller.openView();
              },
              leading: const Icon(Icons.search),
            );
          },
          suggestionsBuilder:
              (BuildContext context, SearchController controller) {
                return List<ListTile>.generate(5, (int index) {
                  final String item = 'We need searching logic $index';
                  return ListTile(
                    title: Text(item),
                    onTap: () {
                      setState(() {
                        controller.closeView(item);
                      });
                    },
                  );
                });
              },
        ),
      ),
      currentIndex: 1,
    );
  }
}
