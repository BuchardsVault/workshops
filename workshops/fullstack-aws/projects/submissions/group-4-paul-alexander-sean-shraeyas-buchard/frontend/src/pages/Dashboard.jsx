import { useEffect, useState } from 'react'
import UserCard from '../components/UserCard'
import { getCurrentUser } from '../currentUser'
import { apiFetch } from '../api'

/* Dashboard for the signed-in user */
function Dashboard() {
    const user = getCurrentUser()
    const [accounts, setAccounts] = useState(null)
    const [error, setError] = useState(null)

    useEffect(() => {
        if (!getCurrentUser()) return

        async function loadAccounts() {
            try {
                /* The token identifies the owner, so there is nothing to pass */
                setAccounts(await apiFetch('/api/accounts/my-accounts'))
            } catch (err) {
                setError(err.message)
            }
        }
        loadAccounts()
    }, [])

    if (!user) return <p className="text-muted-foreground">Not signed in.</p>
    if (error) return <p className="text-destructive">{error}</p>
    if (accounts === null) return <p className="text-muted-foreground">Loading dashboard...</p>

    /* The token carries the email; the display name only comes back on the
       accounts, so fall back to the email for someone with none yet. */
    const name = accounts[0]?.userName ?? user.email

    return (
        <div className="mx-auto max-w-3xl">
            <UserCard user={{ name, email: user.email, accounts }} />
        </div>
    )
}

export default Dashboard
