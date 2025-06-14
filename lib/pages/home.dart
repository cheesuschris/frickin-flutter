import 'package:flutter/material.dart';
import 'package:cooking_app/pages/prof.dart';
import 'package:cooking_app/pages/favorites.dart';
import 'package:cooking_app/pages/landing.dart';
import 'package:cooking_app/pages/search.dart';
import 'package:cooking_app/pages/post.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:math';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

//App selects a random background from unsplash upon opening the app
class _BackgroundRNG extends StatefulWidget {
  final List<Widget> children;
  const _BackgroundRNG({required this.children});

  @override
  _BackgroundRNGState createState() => _BackgroundRNGState();
}

class _BackgroundRNGState extends State<_BackgroundRNG> {
  late Future<String> _imageUrlFuture;

  @override
  void initState() {
    super.initState();
    //Loads the image url BEFORE the build()
    //Goes constructor, createState(), initState(), build()
    _imageUrlFuture = fetchRandomImageUrl('food');
    print("Background image url loaded");
  }

  Future<String> fetchRandomImageUrl(String query) async {
    final apiKey = dotenv.env['PEXELS_API'];
    final url = Uri.parse(
      'https://api.pexels.com/v1/search?query=$query&per_page=30',
    );
    final response = await http.get(url, headers: {'Authorization': apiKey!});

    if (response.statusCode == 200) {
      final json = jsonDecode(response.body);
      final List photos = json['photos'];
      final randomPhoto = photos[Random().nextInt(photos.length)];
      return randomPhoto['src']['original'];
    } else {
      throw Exception('Looks like pexel is ass too');
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<String>(
      future: _imageUrlFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          //loading image
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError || !snapshot.hasData) {
          //smth went wrong, jus display an amber cheese background
          return Container(
            color: Colors.amber,
            child: Column(children: widget.children),
          );
        } else {
          final imageUrl = snapshot.data!;
          return Container(
            decoration: BoxDecoration(
              image: DecorationImage(
                image: NetworkImage(imageUrl),
                fit: BoxFit.cover,
                colorFilter: ColorFilter.mode(
                  Colors.black.withOpacity(0.3),
                  BlendMode.darken,
                ),
              ),
            ),
            padding: const EdgeInsets.all(16),
            child: Column(children: widget.children),
          );
        }
      },
    );
  }
}

class _HomePageState extends State<HomePage> {
  User? get _currentUser => Supabase.instance.client.auth.currentUser;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        child: _BackgroundRNG(
          children: [
            Text(
              'Welcome, chef ${_currentUser?.email ?? "Guest"}!.',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            SizedBox(height: 12),
            Text(
              'Discover and post your favorite recipes and cooks!',
              style: TextStyle(fontSize: 16, color: Colors.white),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.green,
        selectedItemColor: Colors.black,
        unselectedItemColor: Colors.white,
        type: BottomNavigationBarType.fixed,
        showUnselectedLabels: true,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
          BottomNavigationBarItem(icon: Icon(Icons.add), label: 'Post'),
          BottomNavigationBarItem(
            icon: Icon(Icons.favorite),
            label: 'Favorites',
          ),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
        onTap: (int index) {
          switch (index) {
            case 0:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const LandingPage()),
              );
              break;
            case 1:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const SearchPage()),
              );
              break;
            case 2:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const PostPage()),
              );
              break;
            case 3:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const FavoritesPage()),
              );
              break;
            case 4:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const ProfilePage()),
              );
              break;
          }
        },
      ),
    );
  }
}
