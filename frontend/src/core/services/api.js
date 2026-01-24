/**
 * SomaTech Services - Base API Client
 *
 * Centralized fetch wrapper with error handling
 */

const API_BASE = '/api';

class ApiClient {
    constructor(baseUrl = API_BASE) {
        this.baseUrl = baseUrl;
    }

    /**
     * GET request
     */
    async get(endpoint, params = {}) {
        const url = new URL(`${this.baseUrl}${endpoint}`, window.location.origin);
        Object.keys(params).forEach(key => {
            if (params[key] !== undefined && params[key] !== null) {
                url.searchParams.append(key, params[key]);
            }
        });
        return this._fetch(url.toString(), { method: 'GET' });
    }

    /**
     * POST request
     */
    async post(endpoint, body = {}) {
        return this._fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
    }

    /**
     * PUT request
     */
    async put(endpoint, body = {}) {
        return this._fetch(`${this.baseUrl}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this._fetch(`${this.baseUrl}${endpoint}`, { method: 'DELETE' });
    }

    /**
     * Internal fetch with error handling
     */
    async _fetch(url, options = {}) {
        const config = {
            ...options,
            headers: {
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await this._parseError(response);
                throw error;
            }

            // Handle empty responses
            const text = await response.text();
            return text ? JSON.parse(text) : null;

        } catch (err) {
            if (err instanceof ApiError) throw err;
            throw new ApiError('Network error', 0, err.message);
        }
    }

    /**
     * Parse error response
     */
    async _parseError(response) {
        let message = 'Request failed';
        let detail = '';

        try {
            const data = await response.json();
            message = data.message || data.detail || data.error || message;
            detail = data.detail || '';
        } catch {
            message = response.statusText || message;
        }

        return new ApiError(message, response.status, detail);
    }
}

/**
 * Custom API Error
 */
export class ApiError extends Error {
    constructor(message, status, detail = '') {
        super(message);
        this.name = 'ApiError';
        this.status = status;
        this.detail = detail;
    }

    get isUnauthorized() {
        return this.status === 401;
    }

    get isNotFound() {
        return this.status === 404;
    }

    get isValidation() {
        return this.status === 422;
    }

    get isServerError() {
        return this.status >= 500;
    }
}

// Export singleton instance
export const api = new ApiClient();
export { ApiClient };
