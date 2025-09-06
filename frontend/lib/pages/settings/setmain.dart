import 'package:flutter/material.dart';
import 'package:settings_ui/settings_ui.dart';

class Setmain extends StatefulWidget {
  const Setmain({super.key});
  @override
  State<Setmain> createState() => _Setmain();
}

class _Setmain extends State<Setmain> {
  @override
  Widget build(BuildContext context) {
    return SettingsList(
      sections: [
        SettingsSection(
          title: Text("Hello World"),
          tiles: <SettingsTile>[
            SettingsTile.navigation(
              leading: Icon(Icons.language),
              title: Text('Language'),
              value: Text('English'),
            ),
            SettingsTile.navigation(
              leading: Icon(Icons.format_align_center),
              title: Text("Theme?"),
            ),
          ],
        ),
      ],
    );
  }
}
