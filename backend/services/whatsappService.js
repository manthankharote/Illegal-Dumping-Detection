const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

let isReady = false;

// Initialize WhatsApp Client with LocalAuth so session is saved
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    }
});

client.on('qr', (qr) => {
    console.log('[SYSTEM] WhatsApp QR Code generated. Please scan to authenticate:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('[SYSTEM] WhatsApp Client is ready!');
    isReady = true;
});

client.on('authenticated', () => {
    console.log('[SYSTEM] WhatsApp Client authenticated successfully.');
});

client.on('auth_failure', msg => {
    console.error('[ERROR] WhatsApp Authentication failure:', msg);
    isReady = false;
});

client.on('disconnected', (reason) => {
    console.log('[SYSTEM] WhatsApp Client disconnected:', reason);
    isReady = false;
});

// Initialize client immediately
client.initialize();

/**
 * Checks if the WhatsApp client is authenticated and ready to send messages
 * @returns {boolean}
 */
const isWhatsAppReady = () => {
    return isReady;
};

/**
 * Sends a WhatsApp message to a specific phone number
 * @param {string} phoneNumber - The phone number (e.g. "91XXXXXXXXXX")
 * @param {string} message - The message payload
 */
const sendWhatsAppAlert = async (phoneNumber, message) => {
    if (!isReady) {
        console.warn(`[WARNING] Cannot send WhatsApp alert to ${phoneNumber}. Client is not ready.`);
        return;
    }
    try {
        // Ensure phone number format includes country code and @c.us
        const formattedNumber = phoneNumber.includes('@c.us') ? phoneNumber : `${phoneNumber}@c.us`;
        await client.sendMessage(formattedNumber, message);
        console.log(`[SYSTEM] WhatsApp alert sent successfully to ${phoneNumber}`);
    } catch (error) {
        console.error(`[ERROR] Failed to send WhatsApp message to ${phoneNumber}:`, error);
    }
};

module.exports = {
    isWhatsAppReady,
    sendWhatsAppAlert
};
