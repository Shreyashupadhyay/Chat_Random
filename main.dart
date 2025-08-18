import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

void main() {
  runApp(const StrangerChatApp());
}

class StrangerChatApp extends StatelessWidget {
  const StrangerChatApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Stranger Chat',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const ChatPage(),
    );
  }
}

class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  // ✅ UPDATE THIS FOR YOUR SERVER
  static const String WS_URL = 'ws://10.0.2.2:8000/ws/chat/';
  // For real device on same LAN, use ws://<your-ip>:8000/ws/chat/
  // For production, use wss://<domain>/ws/chat/

  WebSocketChannel? _channel;
  StreamSubscription? _sub;
  final TextEditingController _input = TextEditingController();
  final List<_ChatItem> _items = [];

  // reconnect/backoff
  int _retry = 0;
  Timer? _reconnectTimer;
  bool _manuallyClosed = false;

  String _status = 'Connecting…'; // waiting | connected | disconnected

  @override
  void initState() {
    super.initState();
    _connect();
  }

  void _connect() {
    _manuallyClosed = false;
    setState(() => _status = 'Connecting…');

    try {
      _channel = WebSocketChannel.connect(Uri.parse(WS_URL));
      _sub = _channel!.stream.listen(
        (event) {
          _onMessage(event);
        },
        onError: (e) {
          _onDisconnected(error: e.toString());
        },
        onDone: () {
          _onDisconnected();
        },
        cancelOnError: true,
      );

      // When socket is created, Channels consumer typically immediately sends a JSON
      // like {"status": "waiting"} or a first message. Treat as connected now.
      setState(() => _status = 'Connected');
      _retry = 0; // reset backoff
    } catch (e) {
      _onDisconnected(error: e.toString());
    }
  }

  void _onMessage(dynamic raw) {
    // Expecting JSON from backend like {"message":"..."} or {"status":"waiting"}
    try {
      final data = jsonDecode(raw as String);
      if (data is Map && data.containsKey('status')) {
        final s = data['status']?.toString() ?? '';
        setState(() => _status = s == 'waiting' ? 'Waiting for a stranger…' : s);
      }
      if (data is Map && data.containsKey('message')) {
        final msg = data['message']?.toString() ?? '';
        if (msg.isNotEmpty) {
          setState(() {
            _items.add(_ChatItem(sender: Sender.other, text: msg, ts: DateTime.now()));
          });
        }
      }
    } catch (_) {
      // Fallback: treat as plain text
      setState(() {
        _items.add(_ChatItem(sender: Sender.other, text: raw.toString(), ts: DateTime.now()));
      });
    }
  }

  void _onDisconnected({String? error}) {
    if (_manuallyClosed) return; // do not auto-reconnect after manual close
    setState(() => _status = 'Disconnected');

    _retry = (_retry + 1).clamp(1, 6); // 1..6
    final delay = Duration(seconds: 1 << (_retry - 1)); // 1,2,4,8,16,32
    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(delay, _connect);
  }

  void _send() {
    final text = _input.text.trim();
    if (text.isEmpty || _channel == null) return;
    try {
      // Send as JSON with a message field to align with consumer
      _channel!.sink.add(jsonEncode({"message": text}));
      // Add our own message to UI immediately (won't be echoed back from server)
      setState(() {
        _items.add(_ChatItem(sender: Sender.me, text: text, ts: DateTime.now()));
        _input.clear();
      });
    } catch (_) {}
  }

  void _leave() {
    _manuallyClosed = true;
    _reconnectTimer?.cancel();
    _sub?.cancel();
    _channel?.sink.close();
    setState(() => _status = 'Left the chat');
  }

  @override
  void dispose() {
    _leave();
    _input.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Stranger Chat'),
        actions: [
          IconButton(
            tooltip: 'Leave',
            onPressed: _leave,
            icon: const Icon(Icons.logout),
          )
        ],
      ),
      body: Column(
        children: [
          _StatusBar(status: _status),
          const Divider(height: 1),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              reverse: false,
              itemCount: _items.length,
              itemBuilder: (context, index) {
                final item = _items[index];
                final isMe = item.sender == Sender.me;
                return Align(
                  alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
                    decoration: BoxDecoration(
                      color: isMe ? Theme.of(context).colorScheme.primaryContainer : Theme.of(context).colorScheme.surfaceVariant,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          isMe ? 'You' : 'Stranger',
                          style: Theme.of(context).textTheme.labelSmall,
                        ),
                        const SizedBox(height: 4),
                        Text(item.text),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          const Divider(height: 1),
          SafeArea(
            top: false,
            child: Row(
              children: [
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(12, 10, 6, 12),
                    child: TextField(
                      controller: _input,
                      textInputAction: TextInputAction.send,
                      onSubmitted: (_) => _send(),
                      decoration: const InputDecoration(
                        hintText: 'Type your message…',
                        border: OutlineInputBorder(borderSide: BorderSide.none),
                        filled: true,
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(0, 10, 12, 12),
                  child: IconButton(
                    icon: const Icon(Icons.send),
                    onPressed: _send,
                  ),
                )
              ],
            ),
          )
        ],
      ),
    );
  }
}

class _StatusBar extends StatelessWidget {
  final String status;
  const _StatusBar({required this.status});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      color: Theme.of(context).colorScheme.surface,
      child: Row(
        children: [
          const SizedBox(
            width: 10,
            height: 10,
            child: CircularProgressIndicator(strokeWidth: 2),
          ),
          const SizedBox(width: 8),
          Text(status),
        ],
      ),
    );
  }
}

enum Sender { me, other }

class _ChatItem {
  final Sender sender;
  final String text;
  final DateTime ts;
  _ChatItem({required this.sender, required this.text, required this.ts});
}
