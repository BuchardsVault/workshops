/* The API is stateless JWT, so the token is the session. Everything the UI
   knows about the signed in user is read back out of the token payload. */

const KEY = 'authToken'

/* Stores the access_token returned by POST /api/auth/login */
export function setToken(token) {
    localStorage.setItem(KEY, token)
}

export function getToken() {
    return localStorage.getItem(KEY)
}

/* Signs out by throwing the token away */
export function clearCurrentUser() {
    localStorage.removeItem(KEY)
}

/* Reads the middle segment of the JWT. The server is what verifies it;
   this is only so the UI knows whose data it is showing. */
function decodeToken(token) {
    try {
        const segment = token.split('.')[1]
        const base64 = segment.replace(/-/g, '+').replace(/_/g, '/')
        const padded = base64 + '='.repeat((4 - (base64.length % 4)) % 4)
        return JSON.parse(atob(padded))
    } catch {
        return null
    }
}

/* Returns { userId, email, role }, or null when there is no usable token.
   An expired token is cleared on the way out so we stop sending it. */
export function getCurrentUser() {
    const token = getToken()
    if (!token) return null

    const payload = decodeToken(token)
    if (!payload?.sub) return null

    /* exp is seconds since the epoch, Date.now() is milliseconds */
    if (payload.exp && payload.exp * 1000 < Date.now()) {
        clearCurrentUser()
        return null
    }

    return {
        userId: Number(payload.sub),
        email: payload.email ?? null,
        role: payload.role ?? 'user',
    }
}
