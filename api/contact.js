// Vercel Serverless Function: receives the site contact form and forwards it to Telegram.
// Secrets come from Vercel environment variables — never hardcode them here.
//   TELEGRAM_BOT_TOKEN — bot token from @BotFather
//   TELEGRAM_CHAT_ID   — chat id that receives the notifications

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Rate limit: per-IP, in-memory. Survives only as long as the function instance stays warm,
// so it stops a burst from one source but is not a globally consistent limit.
const RATE_MAX = 3;
const RATE_WINDOW_MS = 10 * 60 * 1000; // 10 minutes
const hits = new Map(); // ip -> [timestamps]

function isRateLimited(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  if (recent.length >= RATE_MAX) {
    hits.set(ip, recent);
    return true;
  }
  recent.push(now);
  hits.set(ip, recent);

  if (hits.size > 500) {
    for (const [key, times] of hits) {
      if (!times.some((t) => now - t < RATE_WINDOW_MS)) hits.delete(key);
    }
  }
  return false;
}

function clientIp(req) {
  const fwd = req.headers['x-forwarded-for'];
  if (typeof fwd === 'string' && fwd) return fwd.split(',')[0].trim();
  return (req.socket && req.socket.remoteAddress) || 'unknown';
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }

  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) {
    console.error('Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID');
    return res.status(500).json({ ok: false, error: 'Сервіс тимчасово недоступний' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (e) { body = {}; }
  }
  body = body || {};

  // Honeypot: humans never see this field, so anything in it is a bot.
  // Answer 200 so the bot believes it succeeded and does not retry.
  if (String(body.website || '').trim()) {
    console.warn('Honeypot triggered from', clientIp(req));
    return res.status(200).json({ ok: true });
  }

  const ip = clientIp(req);
  if (isRateLimited(ip)) {
    console.warn('Rate limited:', ip);
    return res.status(429).json({ ok: false, error: 'Забагато спроб. Спробуйте пізніше.' });
  }

  const name = String(body.name || '').trim();
  const contact = String(body.contact || '').trim();
  const message = String(body.message || '').trim();

  if (!name || !contact || !message) {
    return res.status(400).json({ ok: false, error: 'Заповніть усі поля' });
  }
  if (name.length > 100 || contact.length > 200 || message.length > 2000) {
    return res.status(400).json({ ok: false, error: 'Занадто довгий текст' });
  }

  const text =
    '🔔 <b>Нова заявка з сайту Devlly!</b>\n\n' +
    '👤 <b>Ім\'я:</b> ' + esc(name) + '\n' +
    '📬 <b>Контакт:</b> ' + esc(contact) + '\n' +
    '💬 <b>Завдання:</b> ' + esc(message);

  try {
    const tg = await fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'HTML' }),
    });
    const data = await tg.json();
    if (!data.ok) {
      console.error('Telegram API error:', data.description);
      return res.status(502).json({ ok: false, error: 'Не вдалося надіслати повідомлення' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Telegram request failed:', err);
    return res.status(502).json({ ok: false, error: 'Не вдалося надіслати повідомлення' });
  }
};
