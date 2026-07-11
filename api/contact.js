// Vercel Serverless Function: receives the site contact form and forwards it to Telegram.
// Secrets come from Vercel environment variables — never hardcode them here.
//   TELEGRAM_BOT_TOKEN — bot token from @BotFather
//   TELEGRAM_CHAT_ID   — chat id that receives the notifications

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

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
