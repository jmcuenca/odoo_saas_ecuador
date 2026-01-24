/**
 * SomaTech Utilities - Formatters
 */

/**
 * Format currency in USD
 * @param {number} value - Amount
 * @param {string} currency - Currency code (default: USD)
 * @returns {string} Formatted currency string
 */
export function formatCurrency(value, currency = 'USD') {
    return new Intl.NumberFormat('es-EC', {
        style: 'currency',
        currency,
        minimumFractionDigits: 2,
    }).format(value || 0);
}

/**
 * Format date
 * @param {Date|string} date - Date to format
 * @param {string} format - 'short' | 'long' | 'relative'
 * @returns {string} Formatted date
 */
export function formatDate(date, format = 'short') {
    const d = new Date(date);

    if (format === 'relative') {
        return formatRelativeTime(d);
    }

    const options = format === 'long'
        ? { year: 'numeric', month: 'long', day: 'numeric' }
        : { year: 'numeric', month: '2-digit', day: '2-digit' };

    return new Intl.DateTimeFormat('es-EC', options).format(d);
}

/**
 * Format relative time (e.g., "hace 2 horas")
 */
function formatRelativeTime(date) {
    const now = new Date();
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `hace ${days} día${days > 1 ? 's' : ''}`;
    if (hours > 0) return `hace ${hours} hora${hours > 1 ? 's' : ''}`;
    if (minutes > 0) return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
    return 'ahora mismo';
}

/**
 * Format number with thousands separator
 */
export function formatNumber(value) {
    return new Intl.NumberFormat('es-EC').format(value || 0);
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text, maxLength = 100) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
}
