import AccountCard from './AccountCard'
import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'

/* Creating the user card to present a user and their accounts */
function UserCard({ user }) {
    if (!user) return null

    /* Accounts arrive as a prop from the dashboard, which groups them by owner */
    const accounts = user.accounts ?? []

    /* Sums every balance so the card can show a total across accounts */
    const total = accounts.reduce((sum, acc) => sum + Number(acc.balance), 0)

    /** returns the visual of the user card */
    return (
        <Card className="text-left">
            <CardHeader>
                <CardTitle className="text-2xl">{user.name}</CardTitle>
                {user.email && <CardDescription>{user.email}</CardDescription>}
                <CardAction className="text-right">
                    <p className="text-muted-foreground text-sm">Total balance</p>
                    <p className="text-2xl font-medium tabular-nums">
                        ${total.toFixed(2)}
                    </p>
                </CardAction>
            </CardHeader>
            <CardContent>
                {accounts.length === 0 ? (
                    <p className="text-muted-foreground">No accounts yet</p>
                ) : (
                    <div className="grid gap-4 sm:grid-cols-2">
                        {accounts.map((account) => (
                            <AccountCard key={account.accountId} account={account} />
                        ))}
                    </div>
                )}
            </CardContent>
        </Card>
    )
}

export default UserCard
