import 'package:flutter/material.dart';
import 'package:cooking_app/pages/prof.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Cooking App'),
        backgroundColor: Colors.green,
      ),
      body: Container(
        color: Colors.white,
        padding: EdgeInsets.all(20),
        child: Column(
          children: [
            Container(
              alignment: Alignment.centerRight,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => ProfilePage()));
                },
                child: Text('Profile'),
              ),
            ),
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
