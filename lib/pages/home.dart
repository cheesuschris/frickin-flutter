import 'package:flutter/material.dart';
import 'package:cooking_app/pages/prof.dart';
import 'package:cooking_app/pages/favorites.dart';
import 'package:cooking_app/pages/landing.dart';
import 'package:cooking_app/pages/search.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green,
        title:  
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              TextButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => LandingPage()));
                },
                child: Text('Home', style: TextStyle(color: Colors.black)),
                style: TextButton.styleFrom(
                  backgroundColor: Colors.white,
                ),
              ),
              TextButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => SearchPage()));
                },
                child: Text('Search', style: TextStyle(color: Colors.black)),
                style: TextButton.styleFrom(
                  backgroundColor: Colors.white,
                ),
              ),
              TextButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => FavoritesPage()));
                },
                child: Text('Favorites', style: TextStyle(color: Colors.black)),
                style: TextButton.styleFrom(
                  backgroundColor: Colors.white,
                ),
              ),
              TextButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => ProfilePage()));
                },
                child: Text('Profile', style: TextStyle(color: Colors.black),),
                style: TextButton.styleFrom(
                  backgroundColor: Colors.white,
                ),
              ),
            ]
          )
      ), 
      body: Container(
        color: Colors.white,
        padding: EdgeInsets.all(20),
        child: Column(
          children: [
            Container(
              alignment: Alignment.center,
              child: ClipOval(
                child: Container(
                  width: 100,
                  height: 100,
                  color: Colors.black,
                ),
              ),
            ),
            Container(
              child: Text('This is where the app goes ig'),
            ),
          ],
        ),
      ),
    );
  }
}
