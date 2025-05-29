import 'package:flutter/material.dart';
import 'package:cooking_app/pages/home.dart';
import 'package:cooking_app/pages/prof.dart';

class navBar extends StatefulWidget {
  const navBar({super.key});

  @override
  State<navBar> createState() => _navBar();
}

class _navBar extends State<navBar> {
  int pageInd = 0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: NavigationBar(
        labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
        selectedIndex: pageInd,
        onDestinationSelected: (int index) {
          setState(() {
            pageInd = index;
          });
        },
        destinations: <Widget>[
          Container(
            child: (ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => HomePage()),
                );
              },
              child: NavigationDestination(
                icon: Icon(Icons.home),
                label: 'home page',
              ),
            )),
          ),
          Container(
            child: (ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => HomePage()),
                );
              },
              child: NavigationDestination(
                icon: Icon(Icons.star),
                label: 'goes to homepage but can be something different',
              ),
            )),
          ),
          Container(
            child: (ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => ProfilePage()),
                );
              },
              child: NavigationDestination(
                icon: Icon(Icons.person),
                label: 'should go to profile page',
              ),
            )),
          ),
        ],
      ),
    );
  }
}
