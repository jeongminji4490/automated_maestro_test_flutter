import 'package:flutter/material.dart';

class Fruit {
  final String name;
  final double price;

  const Fruit({required this.name, required this.price});
}

const _fruits = [
  Fruit(name: 'Apple', price: 1.2),
  Fruit(name: 'Banana', price: 0.5),
  Fruit(name: 'Cherry', price: 3.0),
  Fruit(name: 'Durian', price: 15.0),
  Fruit(name: 'Elderberry', price: 5.5),
  Fruit(name: 'Fig', price: 2.8),
  Fruit(name: 'Grape', price: 2.0),
  Fruit(name: 'Honeydew', price: 4.0),
  Fruit(name: 'Kiwi', price: 1.5),
  Fruit(name: 'Lemon', price: 0.9),
];

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final _searchController = TextEditingController();
  List<Fruit> _displayedFruits = List.of(_fruits);

  void _search() {
    final query = _searchController.text.trim().toLowerCase();
    setState(() {
      _displayedFruits = _fruits
          .where((f) => f.name.toLowerCase().contains(query))
          .toList();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Dashboard')),
      body: Padding(
        padding: const .all(16.0),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    decoration: const InputDecoration(
                      hintText: 'Search fruits...',
                      border: OutlineInputBorder(),
                      isDense: true,
                    ),
                    onSubmitted: (_) => _search(),
                  ),
                ),
                const SizedBox(width: 8),
                FilledButton(onPressed: _search, child: const Text('Search')),
              ],
            ),
            const SizedBox(height: 16),
            Expanded(
              child: ListView.separated(
                itemCount: _displayedFruits.length,
                separatorBuilder: (_, _) => const Divider(),
                itemBuilder: (context, index) {
                  final fruit = _displayedFruits[index];
                  return ListTile(
                    title: Text(fruit.name),
                    trailing: Text(
                      '\$${fruit.price.toStringAsFixed(2)}',
                      style: const TextStyle(fontSize: 16),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
